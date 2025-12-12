import tkinter as tk

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

def display_results(rows, text, result_limit=None):
    text.config(state="normal")
    text.delete("1.0", tk.END)

    if not rows:
        text.insert(tk.END, "No results found.\n")
    else:
        text.insert(tk.END, f"Showing {len(rows)} result(s) (limited to {result_limit})\n\n")
        for r in rows:
            # assuming your query now selects:
            # movie_id, title, release_year, imdb_rating, director, genres, summary
            movie_id, title, year, rating, director, genres, summary, rotten_tomatoes, platforms = r
            text.insert(tk.END, f"Movie ID              : {movie_id}\n")
            text.insert(tk.END, f"Title                 : {title}\n")
            text.insert(tk.END, f"Year                  : {year}\n")
            text.insert(tk.END, f"Directors             : {director}\n")
            text.insert(tk.END, f"Genres                : {genres}\n")
            text.insert(tk.END, f"IMDb Rating           : {rating}\n")
            text.insert(tk.END, f"Rottem Tomatoes Score : {rotten_tomatoes}\n")
            text.insert(tk.END, f"Summary               : {summary}\n")
            text.insert(tk.END, f"Available on          : {platforms}\n")
            text.insert(tk.END, "-"*80 + "\n")  # separator between movies

    text.config(state="disabled")
