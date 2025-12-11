import mysql.connector
#import pandas as pd
import requests
import time
#from _mysql_connector import errorcode
#import tkinter as tk
#from tkinter import messagebox

API_KEY = "73ff9e0c"
API_URL = "http://www.omdbapi.com/"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword123!",
    database="pick_my_movie"
)

cur = conn.cursor(dictionary=True)

# Get all movies missing IMDB IDs
cur.execute("SELECT movie_id, title, release_year FROM movies WHERE imdb_id IS NULL")
movies = cur.fetchall()

print(f"Found {len(movies)} movies missing IMDb ID.")

not_found = []

for m in movies:
    params = {
        "t": m["title"],
        "y": m["release_year"],
        "apikey": API_KEY
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    # OMDb returns {"Response":"False","Error":"Movie not found!"}
    if data.get("Response") == "False":
        print(f"❌ Not found: {m['title']} ({m['release_year']})")
        not_found.append(m)
        continue

    imdb_id = data.get("imdbID")

    if imdb_id:
        cur.execute(
            "UPDATE movies SET imdb_id = %s WHERE movie_id = %s",
            (imdb_id, m["movie_id"])
        )
        conn.commit()
        print(f"✔ Updated {m['title']} → {imdb_id}")

    # Be nice to the API (free tier is rate-limited)
    time.sleep(0.25)

print("\nDone! Movies not found:")
for m in not_found:
    print(f"{m['title']} ({m['release_year']})")

cur.close()
conn.close()

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




# #READ
# def show_movies():
#     cur.execute("SELECT title, year, imdb_rating FROM movies")
#     rows = cur.fetchall()
#     text.delete(1.0, tk.END)
#     for r in rows:
#         text.insert(tk.END, f"{r}\n")

# #WRITE
# def add_movie():
#     title = entry_title.get()
#     year = entry_year.get()
#     rating = entry_rating.get()

#     cur.execute("""
#         INSERT INTO movies (title, year, imdb_rating)
#         VALUES (%s, %s, %s)
#     """, (title, year, rating))

#     conn.commit()
#     messagebox.showinfo("Success", "Movie added!")

# #DELETE
# def delete_movie():
#     title = entry_title.get()
#     cur.execute("DELETE FROM movies WHERE title = %s", (title,))
#     conn.commit()
#     messagebox.showinfo("Deleted", "Movie deleted")

# #UPDATE
# def update_rating():
#     title = entry_title.get()
#     new_rating = entry_rating.get()
#     cur.execute("""
#         UPDATE movies SET imdb_rating = %s WHERE title = %s
#     """, (new_rating, title))
#     conn.commit()
#     messagebox.showinfo("Updated", "Rating updated")

# #FILTER
# def filter_results():
#     genre = entry_genre.get()
#     min_rating = entry_min_rating.get()

#     query = """
#         SELECT m.title, m.year, m.imdb_rating
#         FROM movies m
#         JOIN movie_genres mg ON m.movie_id = mg.movie_id
#         JOIN genres g ON mg.genre_id = g.genre_id
#         WHERE 1=1
#     """
#     params = []

#     if genre:
#         query += " AND g.genre_name = %s"
#         params.append(genre)

#     if min_rating:
#         query += " AND m.imdb_rating >= %s"
#         params.append(min_rating)

#     cur.execute(query, params)
#     rows = cur.fetchall()

#     text.delete(1.0, tk.END)
#     for r in rows:
#         text.insert(tk.END, f"{r}\n")

# root = tk.Tk()
# root.title("Pick My Movie")

# # GUI Layout
# tk.Label(root, text="Title:").grid(row=0, column=0)
# entry_title = tk.Entry(root)
# entry_title.grid(row=0, column=1)

# tk.Label(root, text="Year:").grid(row=1, column=0)
# entry_year = tk.Entry(root)
# entry_year.grid(row=1, column=1)

# tk.Label(root, text="Rating:").grid(row=2, column=0)
# entry_rating = tk.Entry(root)
# entry_rating.grid(row=2, column=1)

# tk.Label(root, text="Movie ID:").grid(row=3, column=0)
# entry_movie_id = tk.Entry(root)
# entry_movie_id.grid(row=3, column=1)

# tk.Label(root, text="Genre filter:").grid(row=4, column=0)
# entry_genre = tk.Entry(root)
# entry_genre.grid(row=4, column=1)

# tk.Label(root, text="Min rating:").grid(row=5, column=0)
# entry_min_rating = tk.Entry(root)
# entry_min_rating.grid(row=5, column=1)

# tk.Button(root, text="Show All Movies", command=show_movies).grid(row=6, column=0)
# tk.Button(root, text="Add Movie", command=add_movie).grid(row=6, column=1)
# tk.Button(root, text="Delete Movie", command=delete_movie).grid(row=7, column=0)
# tk.Button(root, text="Update Rating", command=update_rating).grid(row=7, column=1)
# tk.Button(root, text="Filter", command=filter_results).grid(row=8, column=0, columnspan=2)

# text = tk.Text(root, width=60, height=15)
# text.grid(row=9, column=0, columnspan=2)

# root.mainloop()

