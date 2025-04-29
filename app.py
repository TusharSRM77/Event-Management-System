from flask import Flask, render_template, request, redirect, Response, flash, session, url_for, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
import MySQLdb
from MySQLdb.cursors import DictCursor
import os
import re
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_fallback_secret_key')

# Database Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)


def validate_event_input(name, date, time, location):
    errors = []
    
    if not name or len(name.strip()) == 0:
        errors.append("Event name is required")
    elif len(name) > 100:
        errors.append("Event name must be less than 100 characters")
    
    try:
        datetime.strptime(date, '%Y-%m-%d')  # Validate date format
    except ValueError:
        errors.append("Invalid date format. Please use YYYY-MM-DD")
    
    try:
        datetime.strptime(time, '%H:%M')  # Validate time format
    except ValueError:
        errors.append("Invalid time format. Please use HH:MM")
    
    if location and len(location) > 150:
        errors.append("Location must be less than 150 characters")
    
    return errors

def validate_registration_input(name, email):
    """Validate registration input fields."""
    errors = []
    
    # Name validation
    if not name or len(name) < 2:
        errors.append("Name must be at least 2 characters long.")
    
    # Email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        errors.append("Invalid email format.")
    
    return errors

# Authentication Routes
@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        registration_number = request.form['registration_number']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        semester = request.form.get('semester')
        year = request.form.get('year')
        
        # Convert empty strings to None for optional fields
        semester = int(semester) if semester else None
        year = int(year) if year else None

        if not registration_number or not email or not password:
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('register_user'))

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (registration_number, name, email, password, semester, year) VALUES (%s, %s, %s, %s, %s, %s)",
                (registration_number, name, email, hashed_password, semester, year)
            )
            mysql.connection.commit()
            cur.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('register_user'))

    return render_template('register_user.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']

        # Check for hardcoded admin credentials
        if email == 'admin@admin.com' and password_input == 'admin123':
            session['logged_in'] = True
            session['email'] = email    
            return redirect(url_for('index'))

        # Check in the database for normal user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password_input):
            session['logged_in'] = True
            session['email'] = user['email']
            session['name'] = user['name']
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
from itsdangerous import URLSafeTimedSerializer

# Add these routes to your existing Flask app

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Check if email exists in database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            token = generate_token(email)
            reset_url = url_for('reset_password', token=token, _external=True)
            
            # In development: Show the link on the page
           
            return render_template('forgot_password.html', reset_link=reset_url)
        
        flash('No account found with that email address.', 'danger')
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_token(token)
    if not email:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('forgot_password'))
    
    # Verify user exists
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        else:
            try:
                hashed_password = generate_password_hash(password)
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "UPDATE users SET password = %s WHERE email = %s",
                    (hashed_password, email)
                )
                mysql.connection.commit()
                cursor.close()
                flash('Password updated successfully! You can now login.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Error updating password: {str(e)}', 'danger')
    
    return render_template('reset_password.html', token=token)

def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=expiration
        )
        return email
    except Exception as e:
        print(f"Token verification failed: {str(e)}")
        return None
# Event Routes
@app.route('/admin')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM events ORDER BY date")
        events = cur.fetchall()
        cur.close()
        return render_template('index.html', events=events)
    except Exception as e:
        flash(f"Error fetching events: {str(e)}", 'error')
        return render_template('index.html', events=[])

@app.route('/add', methods=['POST'])
def add_event():
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    location = request.form['location']

    input_errors = validate_event_input(name, date, time, location)
    if input_errors:
        for error in input_errors:
            flash(error, 'error')
        return redirect('/admin')

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events (name, date, time, location) VALUES (%s, %s, %s, %s)", 
                   (name, date, time, location))
        mysql.connection.commit()
        cur.close()
        flash("Event added successfully!", 'success')
    except Exception as e:
        flash(f"Error adding event: {str(e)}", 'error')
    
    return redirect('/admin')

@app.route('/update', methods=['POST'])
def update_event():
    event_id = request.form['id']
    name = request.form['name']
    date = request.form['date']
    location = request.form['location']

    try:
        cursor = mysql.connection.cursor()
        query = "UPDATE events SET name=%s, date=%s, location=%s WHERE id=%s"
        cursor.execute(query, (name, date, location, event_id))
        mysql.connection.commit()
        cursor.close()
        flash("Event updated successfully!", 'success')
    except Exception as e:
        flash(f"Error updating event: {str(e)}", 'error')
        
    return redirect(url_for('index'))

@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
        mysql.connection.commit()
        cur.close()
        flash("Event deleted successfully!", 'success')
    except Exception as e:
        flash(f"Error deleting event: {str(e)}", 'error')
    
    return redirect('/admin')

# Registration Routes
@app.route('/register', methods=['POST'])
def register():
    event_id = request.form['event_id']
    name = request.form['name']
    email = request.form['email']

    input_errors = validate_registration_input(name, email)
    if input_errors:
        for error in input_errors:
            flash(error, 'error')
        return redirect('/')

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO registrations (event_id, name, email) VALUES (%s, %s, %s)", 
                    (event_id, name, email))
        mysql.connection.commit()
        cur.close()
        flash("Registration successful!", 'success')
    except Exception as e:
        flash(f"Error registering for event: {str(e)}", 'error')
    
    return redirect('/')

@app.route('/register_event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    try:
        cur = mysql.connection.cursor()

        # Check if already registered
        cur.execute("SELECT * FROM registrations WHERE event_id = %s AND email = %s", 
                    (event_id, session['email']))
        if cur.fetchone():
            flash("You have already registered for this event.", "warning")
            return redirect(url_for('user_dashboard'))

        cur.execute(
            "INSERT INTO registrations (event_id, name, email) VALUES (%s, %s, %s)",
            (event_id, session['name'], session['email'])
        )
        mysql.connection.commit()
        cur.close()
        flash("Successfully registered for the event!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    
    return redirect(url_for('user_dashboard'))

@app.route('/view_registration/<int:event_id>')

def view_event_registrations(event_id):
    try:
        cur = mysql.connection.cursor()

        # Get event details
        cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cur.fetchone()

        if not event:
            flash("Event not found.", "warning")
            return redirect(url_for('index'))

        # Fetch registrations for the event
        cur.execute("""
            SELECT registrations.id, registrations.name, registrations.email
            FROM registrations
            WHERE registrations.event_id = %s
        """, (event_id,))
        registrations = cur.fetchall()
        cur.close()

        return render_template("view_event_registrations.html", event=event, registrations=registrations)
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('index'))

# User and Admin Dashboards
@app.route('/dashboard')

def user_dashboard():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM events ORDER BY date, time")
        events = cur.fetchall()
        cur.close()
        return render_template('dashboard.html', events=events)
        flash(f"Error fetching events:", 'danger')
        return redirect('/')

@app.route("/users")

def view_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users ORDER BY id")
        users = cur.fetchall()
        cur.close()
        
        if not users:
            flash("No users found.", "warning")
        
        return render_template("users.html", users=users)
    except Exception as e:
        flash(f"Error fetching users: {str(e)}", 'error')
        return redirect('/')

# Data Export
@app.route('/export')

def export():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM events ORDER BY date")
        events = cur.fetchall()
        cur.close()

        output = []
        output.append(['ID', 'Name', 'Date', 'Location'])
        for event in events:
            output.append([event[0], event[1], event[2], event[3]])

        csv_output = '\n'.join([','.join(map(str, row)) for row in output])

        return Response(
            csv_output, 
            mimetype="text/csv", 
            headers={"Content-Disposition": "attachment;filename=events.csv"}
        )
    except Exception as e:
        flash(f"Error exporting events: {str(e)}", 'error')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)