-- ========= DATA WAREHOUSE TABLES =========

-- Tabela de filmes
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    genres VARCHAR(255)
);

-- Tabela de usuários
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    age INT,
    country VARCHAR(100)
);

-- Tabela de avaliações
CREATE TABLE ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INT,
    movie_title VARCHAR(255),
    rating REAL,
    rated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ========= DATA MART VIEWS =========

-- Visão: Top 10 filmes com melhor média de avaliação (com pelo menos 2 avaliações)
CREATE OR REPLACE VIEW vw_top_10_movies AS
SELECT
    movie_title,
    AVG(rating) as average_rating,
    COUNT(rating_id) as number_of_ratings
FROM ratings
GROUP BY movie_title
HAVING COUNT(rating_id) >= 1
ORDER BY average_rating DESC, number_of_ratings DESC
LIMIT 10;

-- Visão: Número de avaliações por país
CREATE OR REPLACE VIEW vw_ratings_by_country AS
SELECT
    u.country,
    COUNT(r.rating_id) AS number_of_ratings
FROM ratings r
JOIN users u ON r.user_id = u.user_id
GROUP BY u.country
ORDER BY number_of_ratings DESC;