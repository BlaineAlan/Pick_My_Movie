import mysql.connector
#import pandas as pd
# import requests
# import time
# #from _mysql_connector import errorcode
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import csv


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword123!",
    database="pick_my_movie"
)
cur = conn.cursor()



# API_KEY = "73ff9e0c"
# API_URL = "http://www.omdbapi.com/"

# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="NewPassword123!",
#     database="pick_my_movie"
# )

# cur = conn.cursor(dictionary=True)

# # Get all movies missing IMDB IDs
# cur.execute("SELECT movie_id, title, release_year FROM movies WHERE imdb_id IS NULL")
# movies = cur.fetchall()

# print(f"Found {len(movies)} movies missing IMDb ID.")

# not_found = []

# for m in movies:
#     params = {
#         "t": m["title"],
#         "y": m["release_year"],
#         "apikey": API_KEY
#     }

#     response = requests.get(API_URL, params=params)
#     data = response.json()

#     # OMDb returns {"Response":"False","Error":"Movie not found!"}
#     if data.get("Response") == "False":
#         print(f"❌ Not found: {m['title']} ({m['release_year']})")
#         not_found.append(m)
#         continue

#     imdb_id = data.get("imdbID")

#     if imdb_id:
#         cur.execute(
#             "UPDATE movies SET imdb_id = %s WHERE movie_id = %s",
#             (imdb_id, m["movie_id"])
#         )
#         conn.commit()
#         print(f"✔ Updated {m['title']} → {imdb_id}")

#     # Be nice to the API (free tier is rate-limited)
#     time.sleep(0.25)

# print("\nDone! Movies not found:")
# for m in not_found:
#     print(f"{m['title']} ({m['release_year']})")

# cur.close()
# conn.close()

# CSV_PATH = 'IMDbMovies-Clean.csv'

# try:
#     cur = conn.cursor(buffered=True)
#     print("connected to database")
# except mysql.connector.Error as err:
#     print("Database connection error:", err)
#     exit()


# #LOAD CSV
# df = pd.read_csv(CSV_PATH)

# df.fillna('', inplace=True)



# # -----------------------------
# # 1. MPAA RATINGS
# # -----------------------------
# ratings = df['Motion Picture Rating'].unique()
# rating_map = {}

# for r in ratings:
#     if r.strip() == '':
#         continue
#     cur.execute("INSERT IGNORE INTO mpaa_ratings (rating_code) VALUES (%s)", (r,))
#     conn.commit()
#     cur.execute("SELECT rating_id FROM mpaa_ratings WHERE rating_code=%s", (r,))
#     rating_map[r] = cur.fetchone()[0]

# print("MPAA ratings loaded.")

# # -----------------------------
# # 2. GENRES
# # -----------------------------
# all_genres = set()
# for g in df['Main Genres']:
#     for genre in g.split(','):
#         genre = genre.strip()
#         if genre:
#             all_genres.add(genre)

# genre_map = {}
# for genre in all_genres:
#     cur.execute("INSERT IGNORE INTO genres (genre_name) VALUES (%s)", (genre,))
#     conn.commit()
#     cur.execute("SELECT genre_id FROM genres WHERE genre_name=%s", (genre,))
#     genre_map[genre] = cur.fetchone()[0]

# print("Genres loaded.")

# # -----------------------------
# # 3. DIRECTORS
# # -----------------------------
# all_directors = df['Director'].unique()
# director_map = {}

# for d in all_directors:
#     d = d.strip()
#     if not d:
#         continue
#     cur.execute("INSERT IGNORE INTO directors (director_name) VALUES (%s)", (d,))
#     conn.commit()
#     cur.execute("SELECT director_id FROM directors WHERE director_name=%s", (d,))
#     result = cur.fetchone()
#     if result:
#         director_map[d] = result[0]

# print("Directors loaded.")

# # -----------------------------
# # 4. WRITERS
# # -----------------------------
# all_writers = set()
# for w_list in df['Writer']:
#     for w in w_list.split(','):
#         w = w.strip()
#         if w:
#             all_writers.add(w)

# writer_map = {}
# for w in all_writers:
#     cur.execute("INSERT IGNORE INTO writers (writer_name) VALUES (%s)", (w,))
#     conn.commit()
#     cur.execute("SELECT writer_id FROM writers WHERE writer_name=%s", (w,))
#     writer_map[w] = cur.fetchone()[0]

# print("Writers loaded.")

# # -----------------------------
# # 5. MOVIES + Junction Tables
# # -----------------------------

# def safe_float(val):
#     try:
#         return float(val)
#     except (ValueError, TypeError):
#         return None

# for idx, row in df.iterrows():
#     title = row['Title']
#     summary = row['Summary']
#     year = int(row['Release Year']) if row['Release Year'] else None
#     runtime = safe_float(row['Runtime (Minutes)']) if row['Runtime (Minutes)'] else None
#     imdb_rating = safe_float(row['Rating (Out of 10)']) if row['Rating (Out of 10)'] else None
#     num_ratings = safe_float(row['Number of Ratings (in thousands)']) if row['Number of Ratings (in thousands)'] else None
#     budget = safe_float(row['Budget (in millions)']) if row['Budget (in millions)'] else None
#     gross_us = safe_float(row['Gross in US & Canada (in millions)']) if row['Gross in US & Canada (in millions)'] else None
#     gross_world = safe_float(row['Gross worldwide (in millions)']) if row['Gross worldwide (in millions)'] else None
#     opening_weekend = safe_float(row['Opening Weekend in US & Canada']) if row['Opening Weekend in US & Canada'] else None
#     rating_id = rating_map.get(row['Motion Picture Rating'], None)
#     director_id = director_map.get(row['Director'], None)

#     # Insert movie
#     cur.execute("""
#         INSERT INTO movies
#         (title, summary, release_year, runtime_minutes, imdb_rating, num_ratings_k,
#          budget_millions, gross_us_canada_millions, gross_worldwide_millions, 
#          opening_weekend_us_canada_millions, mpaa_rating_id, director_id)
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#     """, (title, summary, year, runtime, imdb_rating, num_ratings, budget,
#           gross_us, gross_world, opening_weekend, rating_id, director_id))
#     conn.commit()

#     cur.execute("SELECT movie_id FROM movies WHERE title=%s", (title,))
#     movie_id = cur.fetchone()[0]

#     # Insert genres
#     for g in row['Main Genres'].split(','):
#         g = g.strip()
#         if g:
#             cur.execute("INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, genre_map[g]))
#     conn.commit()

#     # Insert writers
#     for w in row['Writer'].split(','):
#         w = w.strip()
#         if w:
#             cur.execute("INSERT IGNORE INTO movie_writers (movie_id, writer_id) VALUES (%s, %s)", (movie_id, writer_map[w]))
#     conn.commit()

# print("Movies, genres, and writers loaded successfully.")
# conn.close()

current_user_id = None

# --------------------------
# Login / Signup functions
# --------------------------
import bcrypt

def signup():
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

def login():
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


# ---------------------------
# Leave Review
# ---------------------------
def submit_review_manual():
    if current_user_id is None:
        messagebox.showerror("Error", "You must be logged in to leave a review.")
        return

    movie_id = entry_review_movie_id.get().strip()
    rating = entry_review_rating.get().strip()
    review_text_val = text_review.get("1.0", tk.END).strip()

    if not movie_id or not rating:
        messagebox.showwarning("Error", "Movie ID and rating are required")
        return

    try:
        rating_val = float(rating)
        if rating_val < 0 or rating_val > 10:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Rating must be a number between 0 and 10.")
        return

    try:
        cur.execute("""
            INSERT INTO user_reviews (user_id, movie_id, rating, review_text)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE rating=%s, review_text=%s
        """, (current_user_id, movie_id, rating_val, review_text_val, rating_val, review_text_val))
        conn.commit()
        messagebox.showinfo("Success", "Review submitted!")
        log_action(current_user_id, "submit_review", {"movie_id": movie_id, "rating": rating_val})
        export_audit_log()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save review: {e}")

# ---------------------------
# Delete Review
# ---------------------------
def delete_review():
    if current_user_id is None:
        messagebox.showerror("Error", "You must be logged in to delete a review.")
        return

    movie_id = entry_delete_movie_id.get().strip()
    if not movie_id:
        messagebox.showwarning("Error", "Movie ID required to delete review.")
        return

    try:
        cur.execute("""
            DELETE FROM user_reviews
            WHERE user_id = %s AND movie_id = %s
        """, (current_user_id, movie_id))
        conn.commit()

        if cur.rowcount == 0:
            messagebox.showinfo("Info", "No review found for this movie.")
        else:
            messagebox.showinfo("Success", "Review deleted successfully!")
            log_action(current_user_id, "delete_review", {"movie_id": movie_id})
            export_audit_log()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete review: {e}")

def log_action(user_id, action_type, metadata=None):
    """Insert an action into the audit_log table."""
    try:
        cur.execute("""
            INSERT INTO audit_log (user_id, action_type, metadata)
            VALUES (%s, %s, %s)
        """, (user_id, action_type, json.dumps(metadata) if metadata else None))
        conn.commit()
    except Exception as e:
        print(f"Failed to log action: {e}")


def export_audit_log(filename="audit_log.csv"):
    cur.execute("SELECT * FROM audit_log ORDER BY action_timestamp ASC")
    rows = cur.fetchall()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([i[0] for i in cur.description])  # column headers
        writer.writerows(rows)
    print(f"Audit log exported to {filename}")



# ---------------------------
# My Reviews
# ---------------------------
def show_my_reviews():
    if current_user_id is None:
        messagebox.showerror("Error", "You must be logged in to view your reviews.")
        return

    try:
        cur.execute("""
            SELECT m.movie_id, m.title, r.rating, r.review_text, r.created_at
            FROM user_reviews r
            JOIN movies m ON r.movie_id = m.movie_id
            WHERE r.user_id = %s
            ORDER BY r.created_at DESC
        """, (current_user_id,))
        rows = cur.fetchall()

        text.config(state="normal")
        text.delete("1.0", tk.END)

        if not rows:
            text.insert(tk.END, "You have not submitted any reviews yet.\n")
        else:
            for movie_id, title, rating, review_text_val, created_at in rows:
                text.insert(tk.END, f"Movie ID: {movie_id}\nMovie: {title}\nRating: {rating}\nReview: {review_text_val}\nDate: {created_at}\n")
                text.insert(tk.END, "-"*80 + "\n")
        text.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch your reviews: {e}")



RESULT_LIMIT = 500

#READ
def safe_float(s):
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def safe_int(s):
    if s == "":
        return None
    try:
        return int(s)
    except ValueError:
        return None

def display_results(rows):
    text.config(state="normal")
    text.delete("1.0", tk.END)

    if not rows:
        text.insert(tk.END, "No results found.\n")
    else:
        text.insert(tk.END, f"Showing {len(rows)} result(s) (limited to {RESULT_LIMIT})\n\n")
        for r in rows:
            # assuming your query now selects:
            # movie_id, title, release_year, imdb_rating, director, genres, summary
            movie_id, title, year, rating, director, genres, summary = r
            text.insert(tk.END, f"Movie ID : {movie_id}\n")
            text.insert(tk.END, f"Title    : {title}\n")
            text.insert(tk.END, f"Year     : {year}\n")
            text.insert(tk.END, f"Directors: {director}\n")
            text.insert(tk.END, f"Genres   : {genres}\n")
            text.insert(tk.END, f"Rating   : {rating}\n")
            text.insert(tk.END, f"Summary  : {summary}\n")
            text.insert(tk.END, "-"*80 + "\n")  # separator between movies

    text.config(state="disabled")


def search_movies():
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    min_rating = entry_min_rating.get().strip()
    max_rating = entry_max_rating.get().strip()
    year_min = entry_year_min.get().strip()
    year_max = entry_year_max.get().strip()
    director = entry_director.get().strip()
    keyword = entry_keyword.get().strip()

    query = """
        SELECT DISTINCT m.movie_id, m.title, m.release_year, m.imdb_rating, d.director_name AS director, GROUP_CONCAT(DISTINCT g.genre_name SEPARATOR ', ') AS genres, m.summary
        FROM movies m
        LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.genre_id
        LEFT JOIN directors d ON m.director_id = d.director_id
        WHERE 1=1
    """

    params = []

    if title:
        query += " AND LOWER(m.title) LIKE LOWER(%s)"
        params.append(f"%{title}%")

    if genre:
        query += """
        AND EXISTS (
            SELECT 1
            FROM movie_genres mg2
            JOIN genres g2 ON mg2.genre_id = g2.genre_id
            WHERE mg2.movie_id = m.movie_id
            AND LOWER(g2.genre_name) = LOWER(%s)
        )
        """
        params.append(genre)

    if min_rating:
        query += " AND m.imdb_rating >= %s"
        params.append(min_rating)

    if max_rating:
        query += " AND m.imdb_rating <= %s"
        params.append(max_rating)

    if year_min:
        query += " AND m.release_year >= %s"
        params.append(year_min)

    if year_max:
        query += " AND m.release_year <= %s"
        params.append(year_max)

    if director:
        query += " AND LOWER(d.director_name) LIKE LOWER(%s)"
        params.append(f"%{director}%")

    if keyword:
        query += " AND LOWER(m.summary) LIKE LOWER(%s)"
        params.append(f"%{keyword}%")

    query += " GROUP BY m.movie_id ORDER BY m.title ASC LIMIT 500;"

    try:
        cur.execute(query, params)
        rows = cur.fetchall()
        display_results(rows)
    except Exception as e:
        print("\nFAILED QUERY:\n", query)
        print("PARAMS:", params)
        print("\nERROR:", e)


# ---------------------------
# Tkinter UI
# ---------------------------
root = tk.Tk()
root.title("Pick My Movie")

frm = ttk.Frame(root, padding=8)

auth_frame = ttk.LabelFrame(root, text="Login / Sign Up")
auth_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

ttk.Label(auth_frame, text="Username:").grid(row=0, column=0, sticky="e")
entry_username = ttk.Entry(auth_frame, width=25)
entry_username.grid(row=0, column=1, padx=4, pady=2)

ttk.Label(auth_frame, text="Email (Sign up):").grid(row=1, column=0, sticky="e")
entry_email = ttk.Entry(auth_frame, width=25)
entry_email.grid(row=1, column=1, padx=4, pady=2)

ttk.Label(auth_frame, text="Password:").grid(row=2, column=0, sticky="e")
entry_password = ttk.Entry(auth_frame, width=25, show="*")
entry_password.grid(row=2, column=1, padx=4, pady=2)

ttk.Button(auth_frame, text="Login", command=login).grid(row=3, column=0, pady=4)
ttk.Button(auth_frame, text="Sign Up", command=signup).grid(row=3, column=1, pady=4)

frm.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

review_frame = ttk.LabelFrame(frm, text="Leave a Review")
review_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=8)


ttk.Label(review_frame, text="Movie ID:").grid(row=0, column=0, sticky="e")
entry_review_movie_id = ttk.Entry(review_frame, width=10)
entry_review_movie_id.grid(row=0, column=1, sticky="w", padx=4, pady=2)

ttk.Label(review_frame, text="Rating:").grid(row=0, column=2, sticky="e")
entry_review_rating = ttk.Entry(review_frame, width=5)
entry_review_rating.grid(row=0, column=3, sticky="w", padx=4, pady=2)

ttk.Label(review_frame, text="Review:").grid(row=1, column=0, sticky="ne")
text_review = tk.Text(review_frame, width=60, height=4)
text_review.grid(row=1, column=1, columnspan=3, sticky="w", padx=4, pady=2)

ttk.Button(review_frame, text="Submit Review", command=submit_review_manual).grid(row=2, column=0, columnspan=4, pady=4)

# Button to see all your reviews
ttk.Button(frm, text="My Reviews", command=show_my_reviews).grid(row=9, column=0, columnspan=2, pady=4)

delete_frame = ttk.LabelFrame(frm, text="Delete a Review")
delete_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=8)

ttk.Label(delete_frame, text="Movie ID:").grid(row=0, column=0, sticky="e")
entry_delete_movie_id = ttk.Entry(delete_frame, width=10)
entry_delete_movie_id.grid(row=0, column=1, sticky="w", padx=4, pady=2)

ttk.Button(delete_frame, text="Delete Review", command=delete_review).grid(row=0, column=2, padx=4, pady=2)


# Row 0: Title
tk.Label(frm, text="Title:").grid(row=0, column=0, sticky="e")
entry_title = ttk.Entry(frm, width=40)
entry_title.grid(row=0, column=1, sticky="w", padx=4, pady=2)

# Row 1: Genre
ttk.Label(frm, text="Genre:").grid(row=1, column=0, sticky="e")
entry_genre = ttk.Entry(frm, width=25)
entry_genre.grid(row=1, column=1, sticky="w", padx=4, pady=2)

# Row 2: Director
ttk.Label(frm, text="Director:").grid(row=2, column=0, sticky="e")
entry_director = ttk.Entry(frm, width=30)
entry_director.grid(row=2, column=1, sticky="w", padx=4, pady=2)

# Row 3: Keyword
ttk.Label(frm, text="Keyword:").grid(row=3, column=0, sticky="e")
entry_keyword = ttk.Entry(frm, width=30)
entry_keyword.grid(row=3, column=1, sticky="w", padx=4, pady=2)

# Row 4: Ratings
ratings_frame = ttk.Frame(frm)
ratings_frame.grid(row=4, column=1, sticky="w", padx=4, pady=2)
ttk.Label(frm, text="Min Rating:").grid(row=4, column=0, sticky="e")
entry_min_rating = ttk.Entry(ratings_frame, width=8)
entry_min_rating.grid(row=0, column=0, padx=(0, 8))
ttk.Label(ratings_frame, text="Max Rating:").grid(row=0, column=1, sticky="e")
entry_max_rating = ttk.Entry(ratings_frame, width=8)
entry_max_rating.grid(row=0, column=2)

# Row 5: Years
years_frame = ttk.Frame(frm)
years_frame.grid(row=5, column=1, sticky="w", padx=4, pady=2)
ttk.Label(frm, text="Year From:").grid(row=5, column=0, sticky="e")
entry_year_min = ttk.Entry(years_frame, width=10)
entry_year_min.grid(row=0, column=0, padx=(0, 8))
ttk.Label(years_frame, text="Year To:").grid(row=0, column=1, sticky="e")
entry_year_max = ttk.Entry(years_frame, width=10)
entry_year_max.grid(row=0, column=2)

# Row 6: Search button
search_btn = ttk.Button(frm, text="Search", command=search_movies)
search_btn.grid(row=6, column=0, columnspan=2, pady=(8, 4))

# Row 7: Results text with scrollbar
results_frame = ttk.Frame(frm)
results_frame.grid(row=7, column=0, columnspan=2, sticky="nsew")
frm.rowconfigure(7, weight=1)
frm.columnconfigure(1, weight=1)

text = tk.Text(results_frame, width=90, height=20, state="disabled", wrap="none")
text.grid(row=0, column=0, sticky="nsew")

vscroll = ttk.Scrollbar(results_frame, orient="vertical", command=text.yview)
vscroll.grid(row=0, column=1, sticky="ns")
text['yscrollcommand'] = vscroll.set

hscroll = ttk.Scrollbar(results_frame, orient="horizontal", command=text.xview)
hscroll.grid(row=1, column=0, sticky="ew")
text['xscrollcommand'] = hscroll.set

results_frame.rowconfigure(0, weight=1)
results_frame.columnconfigure(0, weight=1)

# Allow Enter key to trigger search
root.bind('<Return>', lambda evt: search_movies())

# Start UI
root.geometry("900x600")
root.mainloop()

# Close DB resources when app exits (optional)
try:
    if cur:
        cur.close()
    if conn:
        conn.close()
except Exception:
    pass