# Job Portal - Flask Application

A modern job portal built with Flask, featuring user authentication, job posting, and application management.

## Features

### 🔐 Authentication System
- **User Registration**: Secure signup with email validation and password confirmation
- **User Login**: Login with username or email
- **Role-based Access**: Separate interfaces for job seekers and employers
- **Session Management**: Secure session handling with Flask-Login
- **CSRF Protection**: Built-in CSRF protection for all forms

### 👥 User Roles
- **Job Seekers**: Can browse and apply for jobs
- **Employers**: Can post, edit, and manage job listings

### 💼 Job Management
- **Job Posting**: Employers can create new job listings
- **Job Browsing**: Users can search and filter jobs
- **Job Applications**: Job seekers can apply for positions
- **Job Management**: Employers can edit and delete their job postings

### 🎨 User Interface
- **Responsive Design**: Modern, mobile-friendly interface
- **Bootstrap Styling**: Clean and professional appearance
- **Form Validation**: Real-time form validation with helpful error messages
- **Flash Messages**: User-friendly notifications for actions

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "JOB APP"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

5. **Initialize the database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and go to `http://127.0.0.1:5001`

## Project Structure

```
JOB APP/
├── app.py                 # Main Flask application
├── forms.py              # Flask-WTF form definitions
├── models/
│   └── Job.py            # Database models (User, JobPortal)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── profile.html      # User profile page
│   ├── contact.html      # Contact form
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   ├── Job_L.html        # Job listings page
│   └── ...
├── static/               # Static files (CSS, JS, images)
├── utils/
│   └── db.py            # Database configuration
├── instance/            # Database files
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Usage

### For Job Seekers
1. **Register**: Create an account with the "Job Seeker" role
2. **Browse Jobs**: View available job listings
3. **Apply**: Click "Apply" on jobs you're interested in
4. **Profile**: Access your profile to view account information

### For Employers
1. **Register**: Create an account with the "Employer" role
2. **Post Jobs**: Use the "Post Job" feature to create new listings
3. **Manage Jobs**: Edit or delete your job postings
4. **View Applications**: Monitor applications for your jobs

## Security Features

- **Password Hashing**: Passwords are securely hashed using Werkzeug
- **CSRF Protection**: All forms are protected against CSRF attacks
- **Session Security**: Secure session management with Flask-Login
- **Input Validation**: Comprehensive form validation and sanitization
- **Role-based Access Control**: Users can only access features appropriate to their role

## API Endpoints

### Authentication
- `GET/POST /signup` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET /profile` - User profile (requires authentication)

### Jobs
- `GET /Job_L` - View job listings
- `GET /job_details` - View specific job details
- `POST /submit` - Submit new job (employers only)
- `POST /apply_job/<id>` - Apply for a job (job seekers only)
- `GET/POST /update/<id>` - Edit job (employers only)
- `POST /delete/<id>` - Delete job (employers only)

### Other
- `GET/POST /contact` - Contact form
- `GET /about` - About page
- `GET /` - Home page

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@jobportal.com or create an issue in the repository. 