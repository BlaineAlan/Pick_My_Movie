import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from auth import login, signup , current_user_id
from reviews import submit_review_manual, delete_review, show_my_reviews, recommend_movies
from search import search_movies 
from db import cur, conn


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

ttk.Button(auth_frame, text="Login", command=lambda: login(entry_username, entry_email, entry_password, frm, search_btn)).grid(row=3, column=0, pady=4)
ttk.Button(auth_frame, text="Sign Up", command=lambda: signup(entry_username, entry_email, entry_password)).grid(row=3, column=1, pady=4)

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

ttk.Button(review_frame, text="Submit Review", command=lambda: submit_review_manual(current_user_id, entry_review_movie_id, entry_review_rating, text_review)).grid(row=2, column=0, columnspan=4, pady=4)

# Button to see all your reviews
ttk.Button(frm, text="My Reviews", command=lambda: show_my_reviews(text)).grid(row=9, column=0, columnspan=2, pady=4)

delete_frame = ttk.LabelFrame(frm, text="Delete a Review")
delete_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=8)

ttk.Label(delete_frame, text="Movie ID:").grid(row=0, column=0, sticky="e")
entry_delete_movie_id = ttk.Entry(delete_frame, width=10)
entry_delete_movie_id.grid(row=0, column=1, sticky="w", padx=4, pady=2)

ttk.Button(delete_frame, text="Delete Review", command=lambda: delete_review(current_user_id, entry_delete_movie_id, text)).grid(row=0, column=2, padx=4, pady=2)


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
search_btn = ttk.Button(frm, text="Search", command=lambda: search_movies(entry_title, entry_genre, entry_min_rating, entry_max_rating, entry_year_max, entry_year_min, entry_director, entry_keyword, text))
search_btn.grid(row=6, column=0, columnspan=2, pady=(8, 4))
ttk.Button(frm, text="Recommended", command=lambda: recommend_movies(text)).grid(row=6, column=1, pady=(8, 4), sticky="w")


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