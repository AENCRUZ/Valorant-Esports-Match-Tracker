-- IT 211 Final Project: Valorant Esports Match Tracker (VEMT)
-- Sample Data Insertion Script

USE valorantesportstracker;

-- ==========================================================
-- 1. TEAM TABLE — Sample Records
-- ==========================================================
INSERT INTO team (Team_ID, Team_Name, Coach_Name) VALUES
('T001', 'Rising Phoenix', 'Coach Kimi'),
('T002', 'Vandal Spikers', 'Coach Alex'),
('T003', 'Sentinel Squad', 'Coach Ken'),
('T004', 'Jett Streamers', 'Coach May');

-- ==========================================================
-- 2. TOURNAMENT TABLE — Sample Records
-- ==========================================================
INSERT INTO tournament (Tourn_ID, Tourn_Name, Start_Date, Prize_Pool) VALUES
('VCL001', 'Local City Open', '2023-10-01', '2023-10-05', 15000.00),
('VCR2025', 'Regional Circuit 2025', '2023-11-15', '2023-11-30', 75000.00);

-- ==========================================================
-- 3. PLAYER TABLE — Sample Records
-- ==========================================================
INSERT INTO player (Player_ID, IGN, Real_Name, Team_ID) VALUES
('P001', 'RazeNLoad', 'Michael B.', 'T001'),
('P002', 'Skye-High', 'Sarah D.', 'T001'),
('P003', 'Fade-Main', 'Juan D.', 'T001'),
('P004', 'Viper-Pit', 'Elena V.', 'T001'),
('P005', 'Sova-Recon', 'David C.', 'T001'),
('P006', 'Kayo-Bot', 'Jessica A.', 'T002'),
('P007', 'Chamber-R', 'Brian L.', 'T002'),
('P008', 'Orye-Heal', 'Fatima M.', 'T002'),
('P009', 'Breach-Q', 'Carlo P.', 'T002'),
('P010', 'Yoru-Play', 'Sofia H.', 'T002');

-- ==========================================================
-- 4. MATCH RESULT TABLE — Sample Records
-- NOTE: match_id auto-increments
-- ==========================================================
INSERT INTO matches (Match_ID, Tourn_ID, Team_A_ID, Team_B_ID, Winner_ID, Score_A, Score_B) VALUES
('VCL001', 'T001', 'T002', 'T001', 13, 11),
('VCR2025', 'T003', 'T004', 'T003', 13, 7),

-- T003 vs T002 → Score: 8–13 → Winner must be T002 (corrected)
('VCR2025', 'T003', 'T002', 'T002', 8, 13),

-- Draw or incomplete match (winner unknown)
('VCL001', 'T002', 'T003', NULL, 12, 12);
