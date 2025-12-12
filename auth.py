from tkinter import messagebox
import bcrypt
from db import cur, conn
from audit import log_action, export_audit_log

current_user_id = None


def signup(entry_username, entry_email, entry_password):
    username = entry_username.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    if not username or not email or not password:
        messagebox.showwarning("Error", "All fields required")
        return

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        conn.commit()
        messagebox.showinfo("Success", "User created! Please log in.")
        log_action(current_user_id, "Signed up")
        export_audit_log()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create user: {e}")

def login(entry_username, entry_email, entry_password, frm, search_btn):
    global current_user_id
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    if not username or not password:
        messagebox.showwarning("Error", "Username and password required")
        return

    cur.execute("SELECT user_id, password_hash FROM users WHERE username = %s", (username,))
    row = cur.fetchone()
    if not row:
        messagebox.showerror("Error", "User not found")
        return

    user_id, password_hash = row
    if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        current_user_id = user_id
        messagebox.showinfo("Success", f"Logged in as {username}")
        log_action(current_user_id, "Logged in")
        export_audit_log()
        # Enable search UI after login
        frm.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        search_btn.config(state="normal")
    else:
        messagebox.showerror("Error", "Incorrect password")
