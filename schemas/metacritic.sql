CREATE SCHEMA metacritic;

CREATE TABLE IF NOT EXISTS metacritic.stage_games (
    id int PRIMARY KEY,
    title varchar(255),
    year int,
    publisher varchar(255),
    genres varchar(255),
    platform varchar(255),
    metascore int,
    avg_userscore float(1),
    no_players varchar(255)
);

CREATE TABLE IF NOT EXISTS metacritic.stage_reviews (
    id int PRIMARY KEY,
    username varchar(255),
    title varchar(255),
    userscore int,
    platform varchar(255),
    comment text
);

-- CREATE TABLE IF NOT EXISTS metacritic.dim_games (
--     id SERIAL PRIMARY KEY,
--     title varchar(255) UNIQUE,
--     first_release int
-- );

-- CREATE TABLE IF NOT EXISTS metacritic.dim_publishers (
--     id SERIAL PRIMARY KEY,
--     name varchar(255) UNIQUE
-- );

-- CREATE TABLE IF NOT EXISTS metacritic.dim_platforms (
--     id SERIAL PRIMARY KEY,
--     name varchar(255) UNIQUE
-- );

-- CREATE TABLE IF NOT EXISTS metacritic.dim_genres (
--     id SERIAL PRIMARY KEY,
--     name varchar(255) UNIQUE
-- );

-- CREATE TABLE IF NOT EXISTS metacritic.dim_users (
--     id SERIAL PRIMARY KEY,
--     username varchar(255) UNIQUE
-- );

-- CREATE TABLE IF NOT EXISTS metacritic.fact_games (
--     id SERIAL PRIMARY KEY,
--     title varchar(255) UNIQUE,
--     first_release int,
--     publisher_id int REFERENCES metacritic.dim_publishers(id)
-- );

-- CREATE TABLE IF NOT EXISTS metacritic.fact_game_ratings (
--     id SERIAL PRIMARY KEY,
--     user_id int REFERENCES metacritic.dim_users(id),
--     game_id int REFERENCES metacritic.dim_games(id),
--     rating int
-- );
