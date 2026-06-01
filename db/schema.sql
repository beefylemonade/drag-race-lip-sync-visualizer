-- ENUMS
CREATE TYPE cast_role AS ENUM ('contestant', 'assassin');

CREATE TYPE season_type AS ENUM (
    'regular',
    'all_stars',
    'vs_the_world',
    'global',
    'other'
);

CREATE TYPE lipsync_type AS ENUM ('lipsync_for_your_life', 'lipsync_for_the_win');

CREATE TYPE lipsync_outcome AS ENUM ('win', 'loss');

CREATE TYPE artist_type AS ENUM ('primary', 'featuring');

-- TABLES
-- FRANCHISE
CREATE TABLE
    franchise (
        id SERIAL PRIMARY KEY,
        region VARCHAR(100) NOT NULL,
        short_code VARCHAR(20) NOT NULL UNIQUE
    );

-- SEASON
CREATE TABLE
    season (
        id SERIAL PRIMARY KEY,
        franchise_id INTEGER NOT NULL REFERENCES franchise (id),
        season_type season_type season_number INTEGER NOT NULL,
        episode_count INTEGER,
        premiere_date DATE,
        UNIQUE (franchise_id, season_type, season_number)
    );

-- EPISODE
CREATE TABLE
    episode (
        id SERIAL PRIMARY KEY,
        season_id INTEGER NOT NULL REFERENCES season (id),
        episode_number INTEGER NOT NULL,
        title VARCHAR(200),
        air_date DATE,
        UNIQUE (season_id, episode_number)
    );

-- CONTESTANT
CREATE TABLE
    contestant (
        id SERIAL PRIMARY KEY,
        drag_name VARCHAR(100) NOT NULL,
        redacted BOOLEAN DEFAULT FALSE
    );

-- CONTESTANT_ALIAS
CREATE TABLE
    contestant_alias (
        id SERIAL PRIMARY KEY,
        contestant_id INTEGER NOT NULL REFERENCES contestant (id),
        alias VARCHAR(100) NOT NULL UNIQUE,
        UNIQUE (contestant_id, alias)
    );

-- LIPSYNC
CREATE TABLE
    lipsync (
        id SERIAL PRIMARY KEY,
        episode_id INTEGER NOT NULL REFERENCES episode (id),
        song_id INTEGER REFERENCES song (id),
        lipsync_type lipsync_type NOT NULL,
        order_in_episode SMALLINT NOT NULL DEFAULT 1
    );

-- LIPSYNC_PARTICIPANT
CREATE TABLE
    lipsync_participant (
        id SERIAL PRIMARY KEY,
        lipsync_id INTEGER NOT NULL REFERENCES lipsync (id),
        season_contestant_id INTEGER NOT NULL REFERENCES season_contestant (id),
        outcome lipsync_outcome NOT NULL,
        UNIQUE (lipsync_id, season_contestant_id)
    );

-- ARTIST
CREATE TABLE
    artist (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL UNIQUE
    );

-- SONG
CREATE TABLE
    song (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL
    );

-- SONG_ARTIST
CREATE TABLE
    song_artist (
        id SERIAL PRIMARY KEY,
        song_id INTEGER NOT NULL REFERENCES song (id),
        artist_id INTEGER NOT NULL REFERENCES artist (id),
        role artist_role NOT NULL DEFAULT 'primary',
        UNIQUE (song_id, artist_id)
    );