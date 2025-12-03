import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword123!",
    database="pick_my_movie"
)

cur = conn.cursor()

import tkinter as tk
from tkinter import messagebox

#READ
def show_movies():
    cur.execute("SELECT title, year, imdb_rating FROM movies")
    rows = cur.fetchall()
    text.delete(1.0, tk.END)
    for r in rows:
        text.insert(tk.END, f"{r}\n")

#WRITE
def add_movie():
    title = entry_title.get()
    year = entry_year.get()
    rating = entry_rating.get()

    cur.execute("""
        INSERT INTO movies (title, year, imdb_rating)
        VALUES (%s, %s, %s)
    """, (title, year, rating))

    conn.commit()
    messagebox.showinfo("Success", "Movie added!")

#DELETE
def delete_movie():
    title = entry_title.get()
    cur.execute("DELETE FROM movies WHERE title = %s", (title,))
    conn.commit()
    messagebox.showinfo("Deleted", "Movie deleted")

#UPDATE
def update_rating():
    title = entry_title.get()
    new_rating = entry_rating.get()
    cur.execute("""
        UPDATE movies SET imdb_rating = %s WHERE title = %s
    """, (new_rating, title))
    conn.commit()
    messagebox.showinfo("Updated", "Rating updated")

#FILTER
def filter_results():
    genre = entry_genre.get()
    min_rating = entry_min_rating.get()

    query = """
        SELECT m.title, m.year, m.imdb_rating
        FROM movies m
        JOIN movie_genres mg ON m.movie_id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.genre_id
        WHERE 1=1
    """
    params = []

    if genre:
        query += " AND g.genre_name = %s"
        params.append(genre)

    if min_rating:
        query += " AND m.imdb_rating >= %s"
        params.append(min_rating)

    cur.execute(query, params)
    rows = cur.fetchall()

    text.delete(1.0, tk.END)
    for r in rows:
        text.insert(tk.END, f"{r}\n")

root = tk.Tk()
root.title("Pick My Movie")

# GUI Layout
tk.Label(root, text="Title:").grid(row=0, column=0)
entry_title = tk.Entry(root)
entry_title.grid(row=0, column=1)

tk.Label(root, text="Year:").grid(row=1, column=0)
entry_year = tk.Entry(root)
entry_year.grid(row=1, column=1)

tk.Label(root, text="Rating:").grid(row=2, column=0)
entry_rating = tk.Entry(root)
entry_rating.grid(row=2, column=1)

tk.Label(root, text="Movie ID:").grid(row=3, column=0)
entry_movie_id = tk.Entry(root)
entry_movie_id.grid(row=3, column=1)

tk.Label(root, text="Genre filter:").grid(row=4, column=0)
entry_genre = tk.Entry(root)
entry_genre.grid(row=4, column=1)

tk.Label(root, text="Min rating:").grid(row=5, column=0)
entry_min_rating = tk.Entry(root)
entry_min_rating.grid(row=5, column=1)

tk.Button(root, text="Show All Movies", command=show_movies).grid(row=6, column=0)
tk.Button(root, text="Add Movie", command=add_movie).grid(row=6, column=1)
tk.Button(root, text="Delete Movie", command=delete_movie).grid(row=7, column=0)
tk.Button(root, text="Update Rating", command=update_rating).grid(row=7, column=1)
tk.Button(root, text="Filter", command=filter_results).grid(row=8, column=0, columnspan=2)

text = tk.Text(root, width=60, height=15)
text.grid(row=9, column=0, columnspan=2)

root.mainloop()

