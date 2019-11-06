CREATE SCHEMA giantbomb;

CREATE TABLE IF NOT EXISTS giantbomb.stage_games (
    id int PRIMARY KEY,
    game_name varchar(255),
    aliases text,
    deck text,
    description text,
    platform text,
    original_age_ratings text
);

CREATE TABLE IF NOT EXISTS giantbomb.stage_releases (
    id int PRIMARY KEY,
    release_name varchar(255),
    game_id int,
    game_name varchar(255),
    platform varchar(255),
    region varchar(255),
    release_date timestamp
);

CREATE TABLE IF NOT EXISTS giantbomb.stage_reviews (
    id int PRIMARY KEY,
    username varchar(255),
    release_name varchar(255),
    game_id int,
    score float(1),
    deck varchar(255),
    description text
);
