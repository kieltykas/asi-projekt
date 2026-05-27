DROP TABLE IF EXISTS space_earth_data;

CREATE TABLE space_earth_data (
    timestamp TIMESTAMP PRIMARY KEY,
    city VARCHAR(100),
    temp FLOAT,
    weather_desc VARCHAR(255),
    asteroid_count INT
);
