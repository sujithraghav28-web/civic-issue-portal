import sqlite3
from datetime import datetime
import pandas as pd

DB_FILE = "civic_portal.db"

def get_connection():
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            ticket_id TEXT PRIMARY KEY,
            citizen_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            ward_no TEXT NOT NULL,
            issue_category TEXT NOT NULL,
            description TEXT NOT NULL,
            location_landmark TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            admin_notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def generate_ticket_id():
    """Generates a unique ticket ID based on timestamp."""
    now = datetime.now()
    return f"TKT-{now.strftime('%Y%m%d%H%M%S')}"

def create_complaint(name, phone, ward, category, description, landmark):
    """Inserts a new civic complaint into the database."""
    ticket_id = generate_ticket_id()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints (
            ticket_id, citizen_name, phone_number, ward_no,
            issue_category, description, location_landmark
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, name, phone, ward, category, description, landmark))
    conn.commit()
    conn.close()
    return ticket_id

def get_all_complaints_df():
    """Fetches all complaints as a Pandas DataFrame for dashboard analytics."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM complaints ORDER BY created_at DESC", conn)
    conn.close()
    return df

def get_complaint_by_ticket(ticket_id):
    """Fetches status details for a specific ticket ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE ticket_id = ?", (ticket_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_complaint_status(ticket_id, new_status, admin_notes=""):
    """Updates status and timestamp when an officer resolves or updates a complaint."""
    conn = get_connection()
    cursor = conn.cursor()
    resolved_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if new_status == 'Resolved' else None
    
    cursor.execute("""
        UPDATE complaints
        SET status = ?, admin_notes = ?, resolved_at = COALESCE(?, resolved_at)
        WHERE ticket_id = ?
    """, (new_status, admin_notes, resolved_at, ticket_id))
    
    conn.commit()
    conn.close()

# Initialize DB automatically when db.py is imported
init_db()
