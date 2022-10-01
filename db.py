import sqlite3
from datetime import datetime, timezone

# encapsulate logic????

class GmBotDb:
    logCommandQuery = "INSERT INTO Log (discord_user_id, server_id, discord_name, command, timestamp) VALUES(?, ?, ?, ?, ?)"

    def __init__(self, db_filename: str):
        self.db_connection = sqlite3.connect(db_filename or "gm-bot.db")
        self.db_connection.isolation_level = None
        self.cursor = self.db_connection.cursor()
        self.create_tables()

    def __del__(self):
        self.db_connection.close()

    def create_tables(self):
        try:
            self.cursor.execute("PRAGMA foreign_keys = 1")
            self.cursor.execute("BEGIN")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS server(id INTEGER PRIMARY KEY, name VARCHAR, timezone STRING) STRICT"
            )
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS streak(id INTEGER PRIMARY KEY, discord_user_id VARCHAR, server_id VARCHAR, last_gm_on INTEGER, last_longest_streak_on STRING, current_streak INTEGER, longest_streak STRING) STRICT"
            )
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS log(id INTEGER PRIMARY KEY, discord_user_id VARCHAR, server_id VARCHAR, discord_name VARCHAR, command VARCHAR, timestamp STRING) STRICT"
            )
            self.cursor.execute("COMMIT")
        except:
            self.cursor.execute("ROLLBACK")

    def gmUser(self, update_user_id: str, server_id: str, activating_user_id: str = "", activating_user_discord_name: str= ""):
        self.cursor.execute("SELECT name FROM streak WHERE ")
        try:
            self.cursor.execute("BEGIN")
            self.cursor.execute(GmBotDb.logCommandQuery, (activating_user_id, server_id, activating_user_discord_name, "gm", datetime.now(timezone.utc)))
            self.cursor.execute("COMMIT")
        except:
            self.cursor.execute("ROLLBACK")

    def getUserStats(
        self, update_user_id: str, server_id: str, activating_user_id: str = ""
    ):
        print()

    def getLeaderoard(
        self, limit: int = 10, activating_user_id: str = "", server_id: str = ""
    ):
        print()

    def getCurrent(
        self, limit: int = 10, activating_user_id: str = "", server_id: str = ""
    ):
        print()

    def forceOverwrite(
        self,
        update_user_id: str = "",
        activating_user_id: str = "",
        server_id: str = "",
    ):
        print()
