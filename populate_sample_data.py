import os
from faker import Faker
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import MySQLdb

# Load environment variables
load_dotenv()

# Initialize Faker
fake = Faker()

# Database connection
db = MySQLdb.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DB')
)

cursor = db.cursor()

def create_sample_users(num_users=100):
    """Generate and insert sample users into the database"""
    try:
        # Clear existing users (except admin)
        cursor.execute("DELETE FROM users WHERE email != 'admin@admin.com'")
        
        # Insert admin user if not exists
        cursor.execute("SELECT * FROM users WHERE email = 'admin@admin.com'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (registration_number, name, email, password, semester, year) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                ("ADMIN001", "Admin User", "admin@admin.com", 
                 generate_password_hash("admin123"), None, None)
            )
        
        # Generate sample users
        for i in range(1, num_users + 1):
            reg_number = f"STD{str(i).zfill(3)}"
            name = fake.name()
            email = f"user{i}@example.com"
            password = generate_password_hash(f"password{i}")
            semester = random.randint(1, 2)
            year = 1
            
            cursor.execute(
                "INSERT INTO users (registration_number, name, email, password, semester, year) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (reg_number, name, email, password, semester, year)
            )
        
        db.commit()
        print(f"Successfully inserted {num_users} sample users.")
    except Exception as e:
        db.rollback()
        print(f"Error creating users: {e}")

def create_sample_events(num_events=10):
    """Generate and insert sample events into the database"""
    try:
        # Clear existing events
        cursor.execute("DELETE FROM events")
        
        # Sample event names
        event_names = [
            "Tech Symposium 2023",
            "Annual Cultural Fest",
            "Coding Competition",
            "Alumni Meet",
            "Career Fair",
            "Sports Day",
            "Science Exhibition",
            "Literary Fest",
            "Startup Pitch",
            "Music Concert",
            "Art Workshop",
            "Debate Championship",
            "Hackathon",
            "Robotics Competition",
            "Theater Performance"
        ]
        
        # Generate sample events
        for i in range(1, num_events + 1):
            name = random.choice(event_names)
            # Ensure unique event names
            event_names.remove(name)
            
            date = (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
            time = f"{random.randint(9, 18)}:{random.choice(['00', '30'])}"
            location = random.choice([
                "Main Auditorium",
                "Sports Complex",
                "Block A Seminar Hall",
                "Open Air Theater",
                "Computer Lab 3",
                "Library Conference Room",
                "Admin Building Hall"
            ])
            
            cursor.execute(
                "INSERT INTO events (name, date, time, location) "
                "VALUES (%s, %s, %s, %s)",
                (name, date, time, location)
            )
        
        db.commit()
        print(f"Successfully inserted {num_events} sample events.")
    except Exception as e:
        db.rollback()
        print(f"Error creating events: {e}")

def create_sample_registrations():
    """Create sample registrations for events"""
    try:
        # Clear existing registrations
        cursor.execute("DELETE FROM registrations")
        
        # Get all user emails
        cursor.execute("SELECT email FROM users WHERE email != 'admin@admin.com'")
        user_emails = [row[0] for row in cursor.fetchall()]
        
        # Get all event IDs
        cursor.execute("SELECT id FROM events")
        event_ids = [row[0] for row in cursor.fetchall()]
        
        # Create registrations
        for event_id in event_ids:
            # Each event will have between 5 and 20 registrations
            num_registrations = random.randint(5, 20)
            registrants = random.sample(user_emails, min(num_registrations, len(user_emails)))
            
            for email in registrants:
                cursor.execute("SELECT name FROM users WHERE email = %s", (email,))
                name = cursor.fetchone()[0]
                
                cursor.execute(
                    "INSERT INTO registrations (event_id, name, email) "
                    "VALUES (%s, %s, %s)",
                    (event_id, name, email)
                )
        
        db.commit()
        print("Successfully created sample registrations.")
    except Exception as e:
        db.rollback()
        print(f"Error creating registrations: {e}")

if __name__ == '__main__':
    print("Starting to populate sample data...")
    
    create_sample_users(100)
    create_sample_events(10)
    create_sample_registrations()
    
    cursor.close()
    db.close()
    print("Sample data population completed.")