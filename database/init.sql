-- Vérifiez si la base de données existe, sinon créez-la
CREATE DATABASE IF NOT EXISTS mlops_weather;
USE mlops_weather;

-- Créez la table weather_predictions si elle n'existe pas
CREATE TABLE IF NOT EXISTS weather_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    location VARCHAR(255),
    prediction INT,
    accuracy FLOAT
);

