-- Vérifiez si la base de données existe, sinon créez-la
CREATE DATABASE IF NOT EXISTS mlops_weather;
USE mlops_weather;

-- Créez la table weather_predictions si elle n'existe pas
CREATE TABLE IF NOT EXISTS weather_predictions (
    ville VARCHAR(100),
    date DATE,
    prediction VARCHAR(100),
    proba FLOAT,
    PRIMARY KEY (ville, date),
    CONSTRAINT unique_ville_date UNIQUE (ville, date)
);

-- Créez la table weather_scraped si elle n'existe pas
CREATE TABLE IF NOT EXISTS weather_scraped  (
    ville VARCHAR(100),
    date DATE,
    Latitude FLOAT,
    Longitude FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    rain FLOAT,
    evap FLOAT,
    sun FLOAT,
    wind_dir VARCHAR(3),
    wind_speed FLOAT,
    9am_temp FLOAT,
    9am_rh FLOAT,
    9am_cld FLOAT,
    9am_wind_dir VARCHAR(3),
    9am_wind_speed FLOAT,
    9am_pression FLOAT,
    3pm_temp FLOAT,
    3pm_rh FLOAT,
    3pm_cld FLOAT,
    3pm_wind_dir VARCHAR(3),
    3pm_wind_speed FLOAT,
    3pm_pression FLOAT,
    PRIMARY KEY (ville, date),
    CONSTRAINT unique_ville_date UNIQUE (ville, date)
);
