import os
from flask import Flask, flash, jsonify, render_template, request, redirect, session, url_for
from datetime import datetime
from flask_migrate import Migrate
from flask_session import Session
from models.Job import User, JobPortal, Application
from utils.db import db
from sqlalchemy import or_
from werkzeug.exceptions import NotFound
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import SignupForm, LoginForm, ContactForm, JobForm
from data_processor import process_job_data, get_jobs_by_page, get_total_pages
from werkzeug.utils import secure_filename
import pandas as pd




app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bchaitanya7174@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'gast ozbh ilzx mpqx'     # Replace with your app password
app.config['MAIL_DEFAULT_SENDER'] = 'bchaitanya7174@gmail.com'

app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)

db.init_app(app)

Session(app)

mail = Mail(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize database with proper error handling
def init_database():
    with app.app_context():
        try:
            # Drop all tables and recreate them
            db.drop_all()
            db.create_all()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")
            # Try to create tables if they don't exist
            try:
                db.create_all()
                print("Database tables created successfully!")
            except Exception as e2:
                print(f"Error creating tables: {e2}")

# Initialize database
init_database()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/infoviz')
def Infoviz():
    # Your logic for the Infoviz route
    return render_template('infoviz.html')  # Or whatever page you want to display


# Home Page
@app.route('/index')
def index():
    return render_template('index.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Create email content
        email_body = f"""
        New contact form submission:
        
        Name: {form.name.data}
        Email: {form.email.data}
        Subject: {form.subject.data}
        Message:
        {form.message.data}
        """
        
        try:
            # Create and send email
            msg = Message(
                subject=f"Job Portal Contact: {form.subject.data}",
                recipients=['bchaitanya7174@example.com'],  # Replace with your personal email
                body=email_body
            )
            mail.send(msg)
            
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            flash('An error occurred while sending your message. Please try again.', 'error')
            print(f"Error sending email: {str(e)}")
    
    return render_template('contact.html', form=form)

@app.route('/single-blog')
@login_required
def single_blog():
    if not current_user.is_admin:
        flash('Only employers can post jobs.', 'error')
        return redirect(url_for('Job_L'))
    return render_template('single-blog.html')

@app.route('/Job_L', methods=['GET', 'POST'])
def Job_L():
    try:
        # Load jobs from database (user-posted jobs)
        db_jobs = JobPortal.query.all()
        db_job_dicts = []
        for job in db_jobs:
            db_job_dicts.append({
                'id': job.id,
                'Company': job.company,
                'Company Score': job.company_score,
                'Job Title': job.job_title,
                'Location': job.location,
                'Date': job.date.strftime('%Y-%m-%d'),
                'Salary': job.salary,
                'provider_name': job.provider.username if job.provider else None,
                'provider_email': job.provider.email if job.provider else None
            })

        # Load and process CSV jobs
        csv_file_path = 'SE salaries final.csv'
        csv_jobs = process_job_data(csv_file_path)
        for job in csv_jobs:
            job['provider_name'] = 'B. Chaitanya'
            job['provider_email'] = 'bchaitanya7174@gmail.com'

        # Merge both lists
        all_jobs = db_job_dicts + csv_jobs

        # Apply filters (if any)
        filtered_jobs = filter_jobs(all_jobs, request.args)

        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = 12
        jobs = get_jobs_by_page(filtered_jobs, page, per_page)
        total_pages = get_total_pages(filtered_jobs, per_page)

        # Sort by date if requested
        sort_date = request.args.get('sort_date', 'desc')
        def parse_date(job):
            from datetime import datetime
            try:
                return datetime.strptime(job['Date'], '%Y-%m-%d')
            except Exception:
                return datetime.min
        jobs = sorted(jobs, key=parse_date, reverse=(sort_date == 'desc'))

        return render_template('Job_L.html', 
                             jobs=jobs, 
                             current_page=page, 
                             total_pages=total_pages,
                             total_jobs=len(filtered_jobs))
    except Exception as e:
        flash("An error occurred while loading jobs.", "error")
        print(f"Error loading jobs: {e}")
        return render_template('Job_L.html', jobs=[], current_page=1, total_pages=1, total_jobs=0)

def filter_jobs(jobs, filters):
    """Advanced filter jobs based on user criteria"""
    filtered = jobs
    # Filter by location
    if filters.get('location'):
        location_filter = filters['location'].lower()
        filtered = [job for job in filtered if location_filter in job['Location'].lower()]
    # Filter by job title
    if filters.get('job_title'):
        title_filter = filters['job_title'].lower()
        filtered = [job for job in filtered if title_filter in job['Job Title'].lower()]
    # Filter by company
    if filters.get('company'):
        company_filter = filters['company'].lower()
        filtered = [job for job in filtered if company_filter in job['Company'].lower()]
    # Filter by salary range
    if filters.get('salary_range'):
        salary_range = filters['salary_range']
        filtered = [job for job in filtered if check_salary_range(str(job['Salary']), salary_range)]
    # Filter by provider
    if filters.get('provider_name'):
        provider_filter = filters['provider_name'].lower()
        filtered = [job for job in filtered if provider_filter in (job.get('provider_name') or '').lower()]
    return filtered

def check_salary_range(salary_str, range_filter):
    """Check if salary falls within the specified range"""
    try:
        # Extract numeric values from salary string
        import re
        numbers = re.findall(r'\$(\d+)', salary_str)
        if not numbers:
            return True  # If we can't parse salary, show the job
        
        # Get the minimum salary from the range
        min_salary = min([int(num) for num in numbers])
        
        if range_filter == '0-50000':
            return min_salary <= 50000
        elif range_filter == '50000-100000':
            return 50000 <= min_salary <= 100000
        elif range_filter == '100000-150000':
            return 100000 <= min_salary <= 150000
        elif range_filter == '150000+':
            return min_salary >= 150000
        
        return True
    except:
        return True  # If parsing fails, show the job

@app.route('/view_job_details/<int:id>')
def view_job_details(id):
    try:
        # Load CSV data and find the specific job
        csv_file_path = 'SE salaries final.csv'
        all_jobs = process_job_data(csv_file_path)
        
        # Find the job by ID
        job = None
        for j in all_jobs:
            if j['id'] == id:
                job = j
                break
        
        if not job:
            flash('Job not found!', 'error')
            return redirect(url_for('Job_L'))
        
        return render_template('view_details.html', job=job)
    except Exception as e:
        flash('An error occurred while loading job details.', 'error')
        return redirect(url_for('Job_L'))

@app.route('/apply_job_page/<int:id>')
@login_required
def apply_job_page(id):
    if current_user.role != 'user':
        flash('Only job seekers can apply for jobs.', 'error')
        return redirect(url_for('Job_L'))
    
    try:
        # Load CSV data and find the specific job
        csv_file_path = 'SE salaries final.csv'
        all_jobs = process_job_data(csv_file_path)
        
        # Find the job by ID
        job = None
        for j in all_jobs:
            if j['id'] == id:
                job = j
                break
        
        if not job:
            flash('Job not found!', 'error')
            return redirect(url_for('Job_L'))
        
        return render_template('apply_job.html', job=job)
    except Exception as e:
        flash('An error occurred while loading job application.', 'error')
        return redirect(url_for('Job_L'))

@app.route('/submit_application/<int:job_id>', methods=['POST'])
@login_required
def submit_application(job_id):
    if current_user.role != 'user':
        flash('Only job seekers can apply for jobs.', 'error')
        return redirect(url_for('Job_L'))
    try:
        # Get form data
        message = request.form.get('message', '').strip()
        resume_file = request.files.get('resume')
        # Validate required fields
        if not message:
            flash('Please provide a message with your application.', 'error')
            return redirect(url_for('apply_job_page', id=job_id))
        # Handle resume upload
        resume_link = None
        if resume_file and resume_file.filename:
            filename = secure_filename(f"{current_user.username}_{job_id}_{resume_file.filename}")
            resume_path = os.path.join('static', 'Doc', filename)
            abs_resume_path = os.path.join(app.root_path, resume_path)
            os.makedirs(os.path.dirname(abs_resume_path), exist_ok=True)
            resume_file.save(abs_resume_path)
            resume_link = '/' + resume_path.replace('\\', '/')
        # Save application record
        application = Application(job_id=job_id, seeker_id=current_user.id, resume_link=resume_link)
        db.session.add(application)
        db.session.commit()
        # Email notifications
        job = JobPortal.query.get(job_id)
        provider_email = job.provider.email if job and job.provider else 'bchaitanya7174@gmail.com'
        seeker_email = current_user.email
        # Email to provider
        try:
            msg = Message(
                subject=f"New Application for {job.job_title if job else 'Job'}",
                recipients=[provider_email],
                body=f"A new application has been submitted by {current_user.username} for your job posting."
            )
            mail.send(msg)
        except Exception as e:
            print(f"Error sending provider email: {e}")
        # Email to seeker
        try:
            msg = Message(
                subject=f"Application Received: {job.job_title if job else 'Job'}",
                recipients=[seeker_email],
                body=f"Your application for {job.job_title if job else 'the job'} has been received."
            )
            mail.send(msg)
        except Exception as e:
            print(f"Error sending seeker email: {e}")
        flash('Applied for the job', 'success')
        return redirect(url_for('Job_L'))
    except Exception as e:
        flash('An error occurred while submitting your application.', 'error')
        db.session.rollback()
        return redirect(url_for('Job_L'))

# Upload CV Page
@app.route('/upload_cv', methods=['GET', 'POST'])
def upload_cv():
    return render_template('upload_cv.html')

# Manipulate Jobs (View All for Admin)
@app.route('/manipulate')
@login_required
def manipulate():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('Job_L'))
    job = JobPortal.query.all()
    return render_template('manipulate.html', job=job)

# Submit New Job
@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Input validation
        required_fields = ['company', 'job_title', 'location', 'date']
        form_data = request.form.to_dict()
        
        for field in required_fields:
            if not form_data.get(field):
                raise ValueError(f"{field} is required")
        
        # Type conversion and validation
        company_score = float(form_data.get('company_score', 0))  # Default to 0 if missing
        salary = int(form_data.get('salary', 0))  # Default to 0 if missing
        date_obj = datetime.strptime(form_data['date'], '%Y-%m-%d').date()
        provider_id = current_user.id if hasattr(current_user, 'id') else None

        job = JobPortal(
            company=form_data['company'],
            company_score=company_score,
            job_title=form_data['job_title'],
            location=form_data['location'],
            date=date_obj,
            salary=salary,
            provider_id=provider_id
        )

        db.session.add(job)
        db.session.commit()
        flash("Job submitted successfully!", "success")
        
    except ValueError as e:
        flash(f"Invalid input: {str(e)}", "error")
        db.session.rollback()
    except Exception as e:
        flash(f"Error submitting job: {str(e)}", "error")
        db.session.rollback()
    
    return redirect('/Job_L')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    try:
        job = JobPortal.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                # Validate required fields
                required_fields = ['company', 'job_title', 'location', 'date', 'salary', 'company_score']
                for field in required_fields:
                    if not request.form.get(field):
                        raise ValueError(f"{field} is required")
                
                # Validate and convert company score
                company_score = float(request.form['company_score'])
                if not 0 <= company_score <= 5:
                    raise ValueError("Company score must be between 0 and 5")
                
                # Validate and convert salary
                salary = int(request.form['salary'])
                if salary <= 0:
                    raise ValueError("Salary must be a positive number")
                
                # Validate and convert date
                try:
                    date_obj = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError("Invalid date format")
                
                # Update job fields
                job.company = request.form['company'].strip()
                job.company_score = company_score
                job.job_title = request.form['job_title'].strip()
                job.location = request.form['location'].strip()
                job.date = date_obj
                job.salary = salary
                
                # Commit changes
                db.session.commit()
                flash('Job updated successfully!', 'success')
                return redirect(url_for('Job_L'))
                
            except ValueError as e:
                flash(f'Validation error: {str(e)}', 'error')
                db.session.rollback()
            except Exception as e:
                flash(f'Error updating job: {str(e)}', 'error')
                db.session.rollback()
            
            return render_template('update.html', job=job)
        
        # GET request - show the form
        return render_template('update.html', job=job)
        
    except NotFound:
        flash('Job not found!', 'error')
        return redirect(url_for('Job_L'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('Job_L'))

# About Page
@app.route('/update')
def update():
    return render_template('update.html')

# Delete Job
@app.route('/delete/<int:id>', methods=['POST', 'DELETE'])
def delete(id):
    try:
        job = JobPortal.query.get_or_404(id)
        db.session.delete(job)
        db.session.commit()
        flash("Job deleted successfully!", "success")
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        flash(f"Error deleting job: {str(e)}", "error")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/apply_job/<int:id>', methods=['POST'])
@login_required
def apply_job(id):
    job = JobPortal.query.get_or_404(id)
    if current_user.is_admin:
        flash("Employers cannot apply for jobs.", "error")
        return redirect(url_for('Job_L'))

    flash(f"Application submitted for the job: {job.job_title}", "success")
    return redirect(url_for('view_job_details', id=id))

@app.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        sort_by = request.args.get('sort_by')
        order = request.args.get('order', 'desc')
        job_title = request.args.get('job_title', '')

        query = JobPortal.query

        if job_title:
            query = query.filter(JobPortal.job_title.ilike(f'%{job_title}%'))

        if sort_by:
            sort_column = getattr(JobPortal, sort_by)
            if order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(JobPortal.date.desc())

        jobs = query.all()
        return jsonify([{
            'id': job.id,
            'job_title': job.job_title,
            'company': job.company,
            'location': job.location,
            'salary': job.salary,
            'date': job.date.strftime('%Y-%m-%d'),
            'company_score': job.company_score
        } for job in jobs])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/set_role/<role>')
def set_role(role):
    if role in ['user', 'admin']:
        session['role'] = role
        session.modified = True  # Ensure session updates are saved
        return redirect(url_for('Job_L'))
    return redirect(url_for('home'))


# Assuming you have a `User` model and `db` for database handling
# and `User` has fields like username, email, password, role.

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignupForm()
    if form.validate_on_submit():
        try:
            # Check if user already exists
            existing_user = User.query.filter(
                (User.username == form.username.data.strip()) | 
                (User.email == form.email.data.strip())
            ).first()
            
            if existing_user:
                if existing_user.username == form.username.data.strip():
                    flash('Username already exists. Please choose a different one.', 'error')
                else:
                    flash('Email already registered. Please use a different email.', 'error')
                return render_template('signup.html', form=form)
            
            # Create new user
            new_user = User(
                username=form.username.data.strip(),
                email=form.email.data.strip(),
                password=form.password.data,
                role=form.role.data
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during signup: {str(e)}', 'error')
            print(f"Signup error: {e}")
    
    return render_template('signup.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Find user by username or email
            user = User.query.filter(
                (User.username == form.username_or_email.data) | (User.email == form.username_or_email.data)
            ).first()

            if user and user.check_password(form.password.data):
                login_user(user, remember=True)
                flash(f'Welcome back, {user.username}!', 'success')
                
                # Redirect to next page if specified
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('index'))
            else:
                flash('Invalid username/email or password.', 'error')
                
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'error')
            print(f"Login error: {e}")
    
    return render_template('login.html', form=form)



@app.route('/profile')
@login_required
def profile():
    from datetime import datetime
    current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    return render_template('profile.html', user=current_user, current_time=current_time)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        print(f"Edit profile POST request received")
        print(f"Form data: {request.form}")
        try:
            # Get form data
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"New password provided: {bool(new_password)}")
            print(f"Current password provided: {bool(current_password)}")
            
            # Validate required fields
            if not username or not email:
                flash('Username and email are required.', 'error')
                return render_template('edit_profile.html', user=current_user)
            
            # Check if username or email already exists (excluding current user)
            existing_user = User.query.filter(
                (User.username == username) & (User.id != current_user.id)
            ).first()
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('edit_profile.html', user=current_user)
            
            existing_email = User.query.filter(
                (User.email == email) & (User.id != current_user.id)
            ).first()
            if existing_email:
                flash('Email already registered. Please use a different email.', 'error')
                return render_template('edit_profile.html', user=current_user)
            
            # Update basic info
            current_user.username = username
            current_user.email = email
            
            # Handle password change if provided
            if new_password:
                if not current_user.check_password(current_password):
                    flash('Current password is incorrect.', 'error')
                    return render_template('edit_profile.html', user=current_user)
                
                if new_password != confirm_password:
                    flash('New passwords do not match.', 'error')
                    return render_template('edit_profile.html', user=current_user)
                
                if len(new_password) < 6:
                    flash('New password must be at least 6 characters long.', 'error')
                    return render_template('edit_profile.html', user=current_user)
                
                current_user.set_password(new_password)
            
            # Save changes
            db.session.commit()
            print("Profile updated successfully!")
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Profile update error: {e}")
            flash(f'An error occurred while updating your profile: {str(e)}', 'error')
    
    return render_template('edit_profile.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/provider_dashboard')
@login_required
def provider_dashboard():
    if current_user.role != 'admin':
        flash('Only job providers can access the dashboard.', 'error')
        return redirect(url_for('Job_L'))
    jobs = JobPortal.query.filter_by(provider_id=current_user.id).all()
    job_applicants = {}
    for job in jobs:
        applicants = []
        for app in job.applications:
            seeker = app.seeker
            applicants.append({
                'name': seeker.username,
                'email': seeker.email,
                'profile_link': url_for('profile', _external=True),
                'resume_link': app.resume_link
            })
        job_applicants[job.id] = applicants
    return render_template('provider_dashboard.html', jobs=jobs, job_applicants=job_applicants)

@app.route('/import_csv', methods=['GET', 'POST'])
@login_required
def import_csv():
    if current_user.role != 'admin':
        flash('Only job providers can import jobs.', 'error')
        return redirect(url_for('Job_L'))
    if request.method == 'POST':
        file = request.files.get('csv_file')
        if not file:
            flash('No file uploaded.', 'error')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        df = pd.read_csv(file)
        # Find or create the static provider
        provider = User.query.filter_by(email='bchaitanya7174@gmail.com').first()
        if not provider:
            provider = User(username='B. Chaitanya', email='bchaitanya7174@gmail.com', password='defaultpassword', role='admin')
            db.session.add(provider)
            db.session.commit()
        for _, row in df.iterrows():
            job = JobPortal(
                company=row.get('Company', 'Unknown Company'),
                company_score=float(row.get('Company Score', 0)),
                job_title=row.get('Job Title', 'Unknown Position'),
                location=row.get('Location', 'Unknown'),
                date=datetime.now().date(),
                salary=int(row.get('Salary', 0)),
                provider_id=provider.id
            )
            db.session.add(job)
        db.session.commit()
        flash('Jobs imported successfully!', 'success')
        return redirect(url_for('Job_L'))
    return render_template('import_csv.html')

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    )
