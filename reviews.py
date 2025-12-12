from tkinter import messagebox
import tkinter as tk
from db import cur, conn 
from audit import log_action, export_audit_log 
import auth
from utils import display_results

RESULT_LIMIT = 500

def submit_review_manual(current_user_id, entry_review_movie_id, entry_review_rating, text_review):
    if auth.current_user_id is None:
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
        """, (auth.current_user_id, movie_id, rating_val, review_text_val, rating_val, review_text_val))
        conn.commit()
        messagebox.showinfo("Success", "Review submitted!")
        log_action(auth.current_user_id, "submit_review", {"movie_id": movie_id, "rating": rating_val})
        export_audit_log()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save review: {e}")

# ---------------------------
# Delete Review
# ---------------------------
def delete_review(current_user_id, entry_delete_movie_id, text):
    if auth.current_user_id is None:
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
        """, (auth.current_user_id, movie_id))
        conn.commit()

        if cur.rowcount == 0:
            messagebox.showinfo("Info", "No review found for this movie.")
        else:
            messagebox.showinfo("Success", "Review deleted successfully!")
            log_action(auth.current_user_id, "delete_review", {"movie_id": movie_id})
            export_audit_log()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete review: {e}")




# ---------------------------
# My Reviews
# ---------------------------
def show_my_reviews(text):
    if auth.current_user_id is None:
        messagebox.showerror("Error", "You must be logged in to view your reviews.")
        return

    try:
        cur.execute("""
            SELECT m.movie_id, m.title, r.rating, r.review_text, r.created_at
            FROM user_reviews r
            JOIN movies m ON r.movie_id = m.movie_id
            WHERE r.user_id = %s
            ORDER BY r.created_at DESC
        """, (auth.current_user_id,))
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


def recommend_movies(text):
    if auth.current_user_id is None:
        messagebox.showerror("Error", "You must be logged in to see recommendations.")
        return

    query = """
        SELECT DISTINCT m2.movie_id, m2.title, m2.release_year, m2.imdb_rating,
               d2.director_name AS director,
               GROUP_CONCAT(DISTINCT g2.genre_name SEPARATOR ', ') AS genres,
               m2.summary,
               MAX(er.score) AS rotten_tomatoes,
               GROUP_CONCAT(DISTINCT sp.platform_name SEPARATOR ', ') AS platforms
        FROM user_reviews ur
        JOIN movies m1 ON ur.movie_id = m1.movie_id
        JOIN movie_genres mg1 ON m1.movie_id = mg1.movie_id
        JOIN genres g1 ON mg1.genre_id = g1.genre_id
        JOIN movie_genres mg2 ON g1.genre_id = mg2.genre_id
        JOIN movies m2 ON mg2.movie_id = m2.movie_id
        LEFT JOIN movie_genres g2mg ON m2.movie_id = g2mg.movie_id
        LEFT JOIN genres g2 ON g2mg.genre_id = g2.genre_id
        LEFT JOIN directors d2 ON m2.director_id = d2.director_id
        LEFT JOIN external_reviews er ON m2.movie_id = er.movie_id
        LEFT JOIN external_review_sources ers ON er.source_id = ers.source_id AND LOWER(ers.source_name) = 'rotten tomatoes'
        LEFT JOIN movie_streaming ms ON m2.movie_id = ms.movie_id
        LEFT JOIN streaming_platforms sp ON ms.platform_id = sp.platform_id
        WHERE ur.user_id = %s
          AND ur.rating >= 8
          AND m2.movie_id NOT IN (
              SELECT movie_id FROM user_reviews WHERE user_id = %s
          )
        GROUP BY m2.movie_id
        ORDER BY COUNT(DISTINCT g1.genre_id) DESC, m2.imdb_rating DESC
        LIMIT 20;
    """

    try:
        cur.execute(query, (auth.current_user_id, auth.current_user_id))
        rows = cur.fetchall()
        display_results(rows, text, result_limit=RESULT_LIMIT)
        log_action(auth.current_user_id, "view_recommendations")
        export_audit_log()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch recommendations: {e}")

