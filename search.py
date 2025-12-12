from db import cur 
from utils import display_results

RESULT_LIMIT = 500

def search_movies(entry_title, entry_genre, entry_min_rating, entry_max_rating, entry_year_max, entry_year_min, entry_director, entry_keyword, text):
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    min_rating = entry_min_rating.get().strip()
    max_rating = entry_max_rating.get().strip()
    year_min = entry_year_min.get().strip()
    year_max = entry_year_max.get().strip()
    director = entry_director.get().strip()
    keyword = entry_keyword.get().strip()

    query = """
        SELECT DISTINCT m.movie_id, m.title, m.release_year, m.imdb_rating, d.director_name AS director, GROUP_CONCAT(DISTINCT g.genre_name SEPARATOR ', ') AS genres, m.summary, MAX(er.score) AS rotten_tomatoes, GROUP_CONCAT(DISTINCT sp.platform_name SEPARATOR ', ') AS platforms

        FROM movies m
        LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.genre_id
        LEFT JOIN directors d ON m.director_id = d.director_id
        LEFT JOIN external_reviews er ON m.movie_id = er.movie_id
        LEFT JOIN external_review_sources ers ON er.source_id = ers.source_id AND LOWER(ers.source_name) = 'rotten tomatoes'
        LEFT JOIN movie_streaming ms ON m.movie_id = ms.movie_id
        LEFT JOIN streaming_platforms sp ON ms.platform_id = sp.platform_id
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
        display_results(rows, text, result_limit=RESULT_LIMIT)
    except Exception as e:
        print("\nFAILED QUERY:\n", query)
        print("PARAMS:", params)
        print("\nERROR:", e)
