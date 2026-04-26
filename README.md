<div align="center">

# 🎯 VEMT — Valorant Esports Match Tracker

*A database-driven desktop app for managing Valorant tournament data*

![Python](https://img.shields.io/badge/Python-f4a7c3?style=flat-square&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-f4a7c3?style=flat-square&logo=mysql&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-f4a7c3?style=flat-square&logo=python&logoColor=white)

</div>

---

## 📌 About

VEMT is an administrative GUI application designed to manage the organizational data for a small-to-mid-size Valorant esports tournament or league. It handles team registration, player rosters, match scheduling, and match results — all backed by a normalized MySQL relational database.

Built as a final project for **IT 211**, this system demonstrates end-to-end integration of database design, SQL, and GUI development in Python.

---

## ✨ Features

| Module | What it does |
|---|---|
| 🛡️ Manage Teams | Add, update, delete, and view registered teams |
| 👤 Manage Players | Manage player rosters and team assignments |
| 🏆 Manage Tournaments | Create and track tournament events and prize pools |
| ⚔️ Record Match Results | Log scores, winners, and match history |
| 📊 Generate Reports | View team standings, player stats, and tournament summaries |

---

## 🛠️ Tech Stack

- **Language:** Python
- **GUI:** Tkinter
- **Database:** MySQL
- **Connector:** `mysql.connector`
- **Design Pattern:** Modular OOP — database logic separated from GUI windows

---

## 🗄️ Database Schema

The database is structured in **3rd Normal Form (3NF)** with 4 core tables:

```
tournament ──< matches >── team ──< player
```

| Table | Purpose | Key Fields |
|---|---|---|
| `team` | Registered teams | `Team_ID`, `Team_Name`, `Coach_Name` |
| `player` | Player rosters | `Player_ID`, `IGN`, `Real_Name`, `Team_ID` |
| `tournament` | Tournament events | `Tourn_ID`, `Tourn_Name`, `Start_Date`, `Prize_Pool` |
| `matches` | Match results | `Match_ID`, `Tourn_ID`, `Team_A_ID`, `Team_B_ID`, `Winner_ID`, `Score_A`, `Score_B` |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- MySQL Server running locally
- `mysql.connector` library

```bash
pip install mysql-connector-python
```

### Setup

1. Clone this repository:
```bash
git clone https://github.com/AENCRUZ/valorant-esports-tracker.git
cd valorant-esports-tracker
```

2. Create the database and tables:
```bash
mysql -u root -p < table_creation.sql
```

3. (Optional) Load sample data:
```bash
mysql -u root -p < insert_sample_data.sql
```

4. Configure your database credentials in `database_manager.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'ValorantEsportsTracker'
}
```

5. Run the app:
```bash
python vem_tracker.py
```

---

## 📁 Project Structure

```
valorant-esports-tracker/
├── vem_tracker.py          # Main application entry point
├── database_manager.py     # Database connection and CRUD operations
├── table_creation.sql      # Schema — run this first
├── insert_sample_data.sql  # Sample data for testing
└── README.md
```

---

## 🔮 Planned Enhancements

- [ ] Advanced JOIN-based report generation
- [ ] User authentication and login system
- [ ] Export reports to CSV or PDF

---

<div align="center">

Made with 🩷 by [Angelyn](https://github.com/AENCRUZ)

</div>
