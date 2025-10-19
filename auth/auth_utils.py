import sqlite3
import bcrypt
from datetime import datetime
from auth.password_validator import PasswordValidator

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(name, email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    current_time = datetime.now().isoformat()
    
    try:
        cursor.execute("""
            INSERT INTO users (name, email, password, updated_at) 
            VALUES (?, ?, ?, ?)
        """, (name, email, hashed_pw, current_time))
        conn.commit()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        return False, "Email already registered"
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result and check_password(password, result[1]):
        user = {"name": result[0], "email": email}
        return True, user
    return False, None

def check_user(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True , result[4]
    return False , None

def reset_password(email, new_password):
    hashed_pw = hash_password(new_password)
    current_time = datetime.now().isoformat()
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return False, "User with this email does not exist."

        cursor.execute("UPDATE users SET password = ? , updated_at = ? WHERE email = ?", (hashed_pw, current_time, email))
        conn.commit()
        conn.close()
        return True, "Password updated successfully."
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"

def verify_token_count(email, token_updated_at):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT updated_at FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False, "User with this email does not exist."

        db_updated_at = result[0]

        if str(db_updated_at) != str(token_updated_at):
            conn.close()
            return False, "Reset link is no longer valid (token outdated)."

        conn.close()
        return True, None

    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}"