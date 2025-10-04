# Event Management System

A comprehensive web-based Event Management System built with Flask, MySQL, and Bootstrap that streamlines event planning, registration, and management processes.

## 👥 Team Members

- **Ajeet Singh Rawat** - [@ajeetsinghrawat](https://github.com/ajeetsinghrawat)
- **Pratham Arun** - [@Pratham-Arun](https://github.com/Pratham-Arun)
- **Tushar Chaudhary** - [@TusharSRM77](https://github.com/TusharSRM77)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The Event Management System (EMS) is designed to digitize and streamline the entire event planning and execution process. It provides a centralized platform for event organizers, administrators, and attendees to collaborate effectively, reducing manual overhead and improving operational efficiency.

### Problem Statement

Manual event management methods are error-prone, unorganized, and inefficient. The lack of automation in registration, booking, and data tracking causes delays and confusion. This project provides a comprehensive solution for smooth and transparent event handling from creation to registration.

---

## ✨ Features

### Core Features

- **Role-Based Access Control**
  - Admin dashboard with full system access
  - User dashboard for event browsing and registration
  - Secure authentication with encrypted passwords (Bcrypt)

- **Event Management**
  - Create, update, and delete events
  - Real-time event listings
  - Search and filter functionality
  - Event details: name, date, time, location

- **User Management**
  - User registration with validation
  - Secure login system
  - Password reset functionality
  - User profile information

- **Registration System**
  - Easy event registration
  - Duplicate registration prevention
  - View registered attendees
  - Export registration data (CSV)

- **Modern UI/UX**
  - Responsive design for all devices
  - Intuitive navigation
  - Clean and professional interface
  - Real-time flash messages

---

## 🛠️ Technology Stack

### Backend
- **Python 3.x**
- **Flask** - Web framework
- **Flask-MySQLdb** - MySQL database integration
- **Werkzeug** - Password hashing
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5.3** - Responsive UI framework
- **Font Awesome** - Icons
- **JavaScript** - Client-side interactivity

### Database
- **MySQL** - Relational database management

### Security
- **Bcrypt** - Password encryption
- **Session management** - Secure user sessions
- **Environment variables** - Sensitive data protection

---

## 💻 System Requirements

- Python 3.7 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/event-management-system.git
cd event-management-system
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
```
Flask==2.3.0
Flask-MySQLdb==1.0.1
python-dotenv==1.0.0
Werkzeug==2.3.0
mysqlclient==2.1.1
itsdangerous==2.1.2
Faker==18.9.0
```

---

## 🗄️ Database Setup

### 1. Create MySQL Database

```bash
mysql -u root -p
```

### 2. Run Schema File

```sql
source schema.sql
```

Or manually execute:

```sql
CREATE DATABASE event_management;
USE event_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration_number VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100),
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    semester INT,
    year INT
);

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    location VARCHAR(150)
);

CREATE TABLE registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
```

### 3. (Optional) Populate Sample Data

```bash
python populate_sample_data.py
```

This will create:
- 100 sample users
- 10 sample events
- Random registrations

---

## ⚙️ Configuration

### 1. Create `.env` File

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DB=event_management
```

### 2. Update Configuration

Ensure the database credentials match your MySQL installation.

---

## 🚀 Running the Application

### 1. Start the Flask Server

```bash
python app.py
```

### 2. Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

### 3. Default Admin Credentials

```
Email: admin@admin.com
Password: admin123
```

---

## 📖 Usage

### For Administrators

1. **Login** with admin credentials
2. **Create Events** - Add new events with details
3. **Manage Events** - Edit or delete existing events
4. **View Registrations** - Check who registered for each event
5. **Export Data** - Download event data as CSV
6. **View Users** - See all registered users

### For Users

1. **Register** - Create a new account
2. **Login** - Access your dashboard
3. **Browse Events** - View all available events
4. **Register for Events** - Book your spot
5. **Logout** - Securely end your session

### Password Reset

1. Click "Forgot Password" on login page
2. Enter registered email
3. Follow the reset link (displayed in development mode)
4. Set new password

---

## 📁 Project Structure

```
event-management-system/
├── app.py                          # Main Flask application
├── db.py                           # Database configuration
├── schema.sql                      # Database schema
├── populate_sample_data.py         # Sample data generator
├── .env                            # Environment variables (not in repo)
├── .gitignore                      # Git ignore file
├── requirements.txt                # Python dependencies
├── static/
│   └── style.css                   # Custom CSS styles
├── templates/
│   ├── login.html                  # Login page
│   ├── register_user.html          # User registration
│   ├── forgot_password.html        # Password reset request
│   ├── reset_password.html         # Password reset form
│   ├── index.html                  # Admin dashboard
│   ├── dashboard.html              # User dashboard
│   ├── users.html                  # Users list
│   └── view_event_registrations.html # Event registrations view
└── README.md                       # Project documentation
```

---

## 📸 Screenshots

### Login Page
Modern login interface with gradient background and clean form design.

### Admin Dashboard
Comprehensive event management with create, edit, delete, and view functionalities.

### User Dashboard
Browse and register for available events with a clean card-based layout.

### Registration View
View all participants registered for a specific event.

---

## 🔮 Future Enhancements

### Planned Features

1. **Mobile Application Integration**
   - Android/iOS companion apps
   - Push notifications for event updates

2. **Payment Gateway Integration**
   - Razorpay/PayPal/Stripe integration
   - Support for paid events

3. **QR Code Check-In System**
   - Generate unique QR codes for bookings
   - Mobile scanning for event entry

4. **Calendar Synchronization**
   - Google Calendar integration
   - Outlook calendar sync
   - Email reminders

5. **Advanced Analytics**
   - Event attendance reports
   - User engagement metrics
   - Revenue tracking (for paid events)

6. **Enhanced User Features**
   - Event ratings and reviews
   - Social media integration
   - Wishlist functionality

7. **Multi-language Support**
   - Internationalization (i18n)
   - Multiple language options

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Database Normalization

The database follows **Third Normal Form (3NF)**:
- No transitive dependencies
- No partial dependencies
- Ensures data integrity and minimal redundancy

### Entity-Relationship Diagram

**Entities:**
- Users (user_id, registration_number, name, email, password, semester, year)
- Events (event_id, name, date, time, location)
- Registrations (registration_id, event_id, user_id)

**Relationships:**
- One User creates Many Events (Admin)
- Many Users register for Many Events (Many-to-Many)

---

## 🔒 Security Features

- Password hashing using Bcrypt
- Session-based authentication
- SQL injection prevention (parameterized queries)
- XSS protection
- CSRF token support (Flask built-in)
- Environment variable management for sensitive data

---

## 🐛 Known Issues

- Email functionality not implemented (password reset links shown on page in development)
- Limited error handling for network failures
- No rate limiting on API endpoints

---

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [W3Schools - HTML/CSS](https://www.w3schools.com/)
- [GeeksforGeeks - Python Flask](https://www.geeksforgeeks.org/python-flask/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
