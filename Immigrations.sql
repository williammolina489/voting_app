-- 001_create_candidates.sql
CREATE DATABASE IF NOT EXISTS voting_db;
USE voting_db;

CREATE TABLE IF NOT EXISTS candidates (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
party VARCHAR(100) NOT NULL
);

-- 002_create_votes.sql
CREATE TABLE IF NOT EXISTS votes (
id INT AUTO_INCREMENT PRIMARY KEY,
candidate_id INT NOT NULL,
FOREIGN KEY (candidate_id) REFERENCES candidates(id)
ON DELETE CASCADE
);

USE voting_db;

-- List all tables in the database
SHOW TABLES;

-- View the column definitions for the candidates table
DESCRIBE candidates;

-- View the column definitions for the votes table
DESCRIBE votes;
