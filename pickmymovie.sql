CREATE DATABASE pick_my_movie;
USE pick_my_movie;

CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    year INT,
    imdb_rating DECIMAL(3,1)
);

CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL
);

CREATE TABLE movie_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

INSERT INTO movies (title, year, imdb_rating)
VALUES
    ('Inception', 2010, 8.8),
    ('The Dark Knight', 2008, 9.0),
    ('Interstellar', 2014, 8.6);

INSERT INTO genres (genre_name)
VALUES ('Action'), ('Sci-Fi'), ('Drama');

INSERT INTO movie_genres (movie_id, genre_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 1);

