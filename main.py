import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword123!",
    database="pick_my_movie"
)

cur = conn.cursor()

# READ demo
cur.execute("SELECT title, year FROM movies;")
rows = cur.fetchall()
print("Movies in database:")
for r in rows:
    print(r)

# WRITE demo
cur.execute("""
    INSERT INTO users (username, email, password_hash)
    VALUES (%s, %s, %s)
""", ("test_user", "test@example.com", "hashed_pw_123"))

conn.commit()
print("\nInserted user successfully.")
