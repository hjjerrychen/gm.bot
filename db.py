import sqlite3


class GmBotDb:
    createStreakTableQuery = "CREATE TABLE IF NOT EXISTS streak(id TEXT PRIMARY KEY, discord_user_id TEXT, discord_username TEXT, discord_server_id TEXT, discord_server_name TEXT, current_count INTEGER, last_gm_on TEXT, longest_streak INTEGER, last_longest_streak_on TEXT) STRICT"
    getStreakQuery = "SELECT current_count, last_gm_on, longest_streak, last_longest_streak_on, discord_username, discord_server_name FROM streak WHERE id = ?"
    newUserQuery = "INSERT INTO streak VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    updateUserQuery = "UPDATE streak SET current_count = ?, last_gm_on = ?, longest_streak = ?, last_longest_streak_on = ?, discord_username = ?, discord_server_name = ? WHERE id = ?"
    topUsersQuery = "SELECT discord_username, current_count, longest_streak FROM streak WHERE discord_server_id = ? ORDER BY longest_streak LIMIT ?"

    def __init__(self, db_filename: str = "gm-bot.db"):
        self.db_connection = sqlite3.connect(db_filename)
        self.db_connection.isolation_level = None
        self.cursor = self.db_connection.cursor()
        self.create_tables()

    def __del__(self):
        self.db_connection.close()

    def create_tables(self):
        self.cursor.execute("PRAGMA foreign_keys = 1")
        self.cursor.execute(GmBotDb.createStreakTableQuery)

    def getStreak(self, key: int):
        return self.cursor.execute(GmBotDb.getStreakQuery, (key,)).fetchone()

    def newUser(self, data):
        self.cursor.execute(GmBotDb.newUserQuery, data)

    def updateUser(self, data):
        self.cursor.execute(GmBotDb.updateUserQuery, data)
    
    def getTopUsers(self, discord_server_id: str, limit: int = 10):
        return self.cursor.execute(GmBotDb.topUsersQuery, (discord_server_id, limit))

