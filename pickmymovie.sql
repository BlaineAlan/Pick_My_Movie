CREATE DATABASE pick_my_movie;
USE pick_my_movie;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS movies;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE mpaa_ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    rating_code VARCHAR(20) UNIQUE NOT NULL  -- G, PG, PG-13, R, etc.
);

CREATE TABLE writers (
    writer_id INT AUTO_INCREMENT PRIMARY KEY,
    writer_name VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    release_year INT,
    runtime_minutes INT,
    imdb_rating DECIMAL(3,1),
    num_ratings_k INT,
    budget_millions DECIMAL(12,2),
    gross_us_canada_millions DECIMAL(12,2),
    gross_worldwide_millions DECIMAL(12,2),
    opening_weekend_us_canada_millions DECIMAL(12,2),
    mpaa_rating_id INT,
    director_id INT,
	rt_id VARCHAR(255) UNIQUE,

    FOREIGN KEY (mpaa_rating_id) REFERENCES mpaa_ratings(rating_id),
    FOREIGN KEY (director_id) REFERENCES directors(director_id)
);

CREATE TABLE movie_writers (
    movie_id INT,
    writer_id INT,
    PRIMARY KEY (movie_id, writer_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (writer_id) REFERENCES writers(writer_id)
);

DROP TABLE IF EXISTS genres;
CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS movie_genres;
CREATE TABLE movie_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);


DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS user_reviews;
CREATE TABLE user_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating DECIMAL(3,1) CHECK (rating >= 0 AND rating <= 10),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, movie_id),

    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE
);



DROP TABLE IF EXISTS user_watch_history;
CREATE TABLE user_watch_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS audit_log;
CREATE TABLE audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(100) NOT NULL,
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
);

DROP TABLE IF EXISTS directors;
CREATE TABLE directors (
    director_id INT AUTO_INCREMENT PRIMARY KEY,
    director_name VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS movie_directors;
CREATE TABLE movie_directors (
    movie_id INT NOT NULL,
    director_id INT NOT NULL,
    PRIMARY KEY (movie_id, director_id),

    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE,
    FOREIGN KEY (director_id) REFERENCES directors(director_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS movie_posters;
CREATE TABLE movie_posters (
    poster_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    poster_url VARCHAR(500),
    source_dataset VARCHAR(255),

    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS streaming_platforms;
CREATE TABLE streaming_platforms (
    platform_id INT AUTO_INCREMENT PRIMARY KEY,
    platform_name VARCHAR(100) NOT NULL UNIQUE,
    platform_url VARCHAR(255)
);

DROP TABLE IF EXISTS movie_streaming;
CREATE TABLE movie_streaming (
    movie_id INT NOT NULL,
    platform_id INT NOT NULL,
    PRIMARY KEY (movie_id, platform_id),

    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES streaming_platforms(platform_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS keywords;
CREATE TABLE keywords (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    keyword_name VARCHAR(255) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS movie_keywords;
CREATE TABLE movie_keywords (
    movie_id INT NOT NULL,
    keyword_id INT NOT NULL,
    PRIMARY KEY (movie_id, keyword_id),

    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS user_favorites;
CREATE TABLE user_favorites (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, movie_id),

    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS search_history;
CREATE TABLE search_history (
    search_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    search_query TEXT,
    filters JSON,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE external_review_sources (
    source_id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE external_reviews (
    external_review_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    source_id INT NOT NULL,
    score DECIMAL(4,1), -- e.g. Rotten Tomatoes %, Metacritic score
    review_count INT,

    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (source_id) REFERENCES external_review_sources(source_id)
);

SELECT COUNT(*) FROM movies;
SELECT COUNT(*) FROM genres;
SELECT COUNT(*) FROM movie_genres;
SELECT COUNT(*) FROM writers;
SELECT COUNT(*) FROM movie_writers;
