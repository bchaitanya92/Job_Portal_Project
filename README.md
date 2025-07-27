
# 💼 Job Portal - Flask Web Application

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
</p>

<p align="center">
  <strong>A full-featured job portal built with Flask.</strong><br>
  Seamless experience for job seekers and employers, secure authentication, role-based access, and a clean, responsive UI.
</p>

---

## 🚀 Features

### 🔐 Authentication System
- Email verification & password confirmation
- Login with username or email
- Session management via Flask-Login
- CSRF protection for all forms

### 👥 Role-Based Access
- **Job Seekers**: Browse & apply for jobs
- **Employers**: Post, manage & update job listings

### 💼 Job Management
- Employers can post, edit, and delete jobs
- Seekers can filter, view, and apply to jobs

### 🎨 UI & UX
- Responsive design using Bootstrap 5
- Clean layout with intuitive navigation
- Real-time form validation & flash messages

---

## 📁 Project Structure

```
JOB APP/
├── app.py               # Entry point for the Flask app
├── forms.py             # Flask-WTF form definitions
├── models/
│   └── Job.py           # SQLAlchemy models
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── Job_L.html
│   └── ...
├── static/              # Static assets (CSS, JS, Images)
├── utils/
│   └── db.py            # DB config and helper functions
├── instance/            # SQLite database files
├── requirements.txt     # Python package dependencies
└── README.md            # This file
```

---

## ⚙️ Installation Guide

### ✅ Requirements
- Python 3.8+
- `pip` package manager

### 🛠️ Setup Instructions

```bash
# 1. Clone the repository
git clone <repository-url>
cd "JOB APP"

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
# Create a .env file in the root directory:
```

```env
SECRET_KEY=your-secret-key
MAIL_USERNAME=youremail@example.com
MAIL_PASSWORD=your-app-password
```

```bash
# 5. Initialize the database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 6. Run the server
python app.py
```

---

## 🌐 Visit the App

🖥️ Open your browser and go to:  
👉 **http://127.0.0.1:5001**

---

## 🧑‍💻 User Guide

### 👨‍🎓 Job Seekers
- Register using **Job Seeker** role
- Browse job listings
- Apply to jobs instantly
- Manage your profile

### 🧑‍💼 Employers
- Register using **Employer** role
- Post new job listings
- Edit or delete existing jobs
- View applicants

---

## 🔒 Security Features

- Secure password hashing (`werkzeug.security`)
- CSRF protection using Flask-WTF
- Form validation and sanitization
- Role-based access to routes and actions
- Secure session management with Flask-Login

---

## 📡 API Endpoints Overview

| Route                  | Functionality             |
|------------------------|---------------------------|
| `/signup`              | User Registration         |
| `/login`               | User Login                |
| `/logout`              | Logout                    |
| `/profile`             | User Profile              |
| `/Job_L`               | Job Listings              |
| `/submit`              | Post a Job (Employer)     |
| `/apply_job/<id>`      | Apply to a Job            |
| `/update/<id>`         | Update Job (Employer)     |
| `/delete/<id>`         | Delete Job (Employer)     |
| `/contact`             | Contact Form              |
| `/about`               | About Page                |
| `/`                    | Home Page                 |

---

## 🤝 Contributing

Want to improve this project? Contributions are welcome!

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/awesome-feature

# 3. Commit your changes
git commit -m "Add awesome feature"

# 4. Push to your branch
git push origin feature/awesome-feature

# 5. Open a pull request
```

---

## 👨‍🎓 Author

Developed with ❤️ by **B. Chaitanya**

- 🔗 **GitHub**: [bchaitanya92](https://github.com/bchaitanya92)  
- 💼 **LinkedIn**: [BOURISETTI CHAITANYA](https://www.linkedin.com/in/b-chaitanya)

---

## 📃 License

This project is licensed under the [MIT License](./LICENSE). Feel free to use and modify with attribution.

---

## 🛠️ Support

Facing issues or have questions?

📧 Email: [support@jobportal.com](mailto:support@jobportal.com)  
🐞 Or [create an issue](https://github.com/yourrepo/issues) in the repository.
