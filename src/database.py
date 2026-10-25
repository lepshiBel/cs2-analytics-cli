import sqlite3
import os
from typing import List
from src.models import Match

#Manages SQLite database operations for player match statistics
class DatabaseManager:
    def __init__(self, db_name: str = "data/cs2_stats.db"):
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.db_path = db_name
        self._init_db()

    #Initialize database table for matches if it does not exist
    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_matches (
                    match_id TEXT PRIMARY KEY,
                    date TEXT,
                    map_name TEXT,
                    kills INTEGER,
                    deaths INTEGER,
                    assists INTEGER,
                    result TEXT
                )
            """)
            conn.commit()

    #Save a list of matches into the database
    def save_matches(self, matches: List[Match]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for match in matches:
                cursor.execute("""
                    INSERT OR IGNORE INTO api_matches (match_id, date, map_name, kills, deaths, assists, result)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (match.match_id, match.date, match.map_name, match.kills, match.deaths, match.assists, match.result))
            conn.commit()

    #Load all matches from the database and convert them to Match objects
    def load_matches(self) -> List[Match]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT match_id, date, map_name, kills, deaths, assists, result FROM api_matches")
            rows = cursor.fetchall()

        matches = []
        for row in rows:
            matches.append(Match(
                match_id=row[0],
                date=row[1],
                map_name=row[2],
                kills=row[3],
                deaths=row[4],
                assists=row[5],
                result=row[6]
            ))
        return matches

    #Clear all API match records from the database
    def clear_database(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM api_matches")
            conn.commit()
    
