-- IT 211 Final Project: Valorant Esports Match Tracker (VEMT)
-- Database: valorantesportstracker
-- Author: Angelyn A. Cruzat
-- Date: 2025-11-26

-- ==========================================================
-- 1. CREATE DATABASE
-- ==========================================================
CREATE DATABASE IF NOT EXISTS valorantesportstracker;
USE valorantesportstracker;

-- ==========================================================
-- 2. TEAM TABLE
-- Stores basic information about esports teams.
-- ==========================================================
CREATE TABLE IF NOT EXISTS team (
    Team_ID VARCHAR(10) PRIMARY KEY,
    Team_Name VARCHAR(50) NOT NULL UNIQUE,
    Coach_Name VARCHAR(50)
);

-- ==========================================================
-- 3. PLAYER TABLE
-- Stores player information and links them to a team.
-- ==========================================================
CREATE TABLE IF NOT EXISTS player (
    Player_ID VARCHAR(10) PRIMARY KEY,
    IGN VARCHAR(50) NOT NULL UNIQUE, -- In-Game Name
    Real_Name VARCHAR(100),
    Team_ID VARCHAR(10),

    -- Foreign key linking the player to a team
    FOREIGN KEY (Team_ID) REFERENCES team(Team_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ==========================================================
-- 4. TOURNAMENT TABLE
-- Stores information about tournaments or events.
-- ==========================================================
CREATE TABLE IF NOT EXISTS tournament (
    Tourn_ID VARCHAR(10) PRIMARY KEY,
    Tourn_Name VARCHAR(100) NOT NULL,
    Start_Date DATE NOT NULL,
    Prize_Pool DECIMAL(10,2) -- Currency amount
);

-- ==========================================================
-- 5. MATCHES TABLE
-- Stores match results and links two teams to a tournament.
-- ==========================================================
CREATE TABLE IF NOT EXISTS matches (
    Match_ID INT AUTO_INCREMENT PRIMARY KEY,
    Tourn_ID VARCHAR(10) NOT NULL,
    Team_A_ID VARCHAR(10) NOT NULL,
    Team_B_ID VARCHAR(10) NOT NULL,
    Winner_ID VARCHAR(10), -- NULL if draw or not yet completed
    Score_A INT NOT NULL,
    Score_B INT NOT NULL,

    -- Foreign key: tournament
    FOREIGN KEY (Tourn_ID) REFERENCES tournament(Tournament_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    -- Foreign key: team A
    FOREIGN KEY (Team_A_ID) REFERENCES team(Team_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    -- Foreign key: team B
    FOREIGN KEY (Team_B_ID) REFERENCES team(Team_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    -- Foreign key: winner team
    FOREIGN KEY (Winner_ID) REFERENCES team(Team_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
