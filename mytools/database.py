import os
import shutil
import sqlite3
import subprocess
from datetime import datetime

import pytz
from pymongo import MongoClient

from .encrypt import BinaryEncryptor

#  _      ____   _____          _        _____       _______       ____           _____ ______  #
# | |    / __ \ / ____|   /\   | |      |  __ \   /\|__   __|/\   |  _ \   /\    / ____|  ____| #
# | |   | |  | | |       /  \  | |      | |  | | /  \  | |  /  \  | |_) | /  \  | (___ | |__    #
# | |   | |  | | |      / /\ \ | |      | |  | |/ /\ \ | | / /\ \ |  _ < / /\ \  \___ \|  __|   #
# | |___| |__| | |____ / ____ \| |____  | |__| / ____ \| |/ ____ \| |_) / ____ \ ____) | |____  #
# |______\____/ \_____/_/    \_\______| |_____/_/    \_\_/_/    \_\____/_/    \_\_____/|______| #


class LocalDataBase:
    def __init__(
        self,
        bot_db_path: str = "mytoolsBot.db",
        vars_db_path: str = "mytoolsVars.db",
        backup_dir: str = "mytoolsBackup",
    ):
        self.bot_db_path = bot_db_path
        self.vars_db_path = vars_db_path
        self.backup_dir = backup_dir
        self.timezone = pytz.timezone("Asia/Jakarta")

        os.makedirs(self.backup_dir, exist_ok=True)

        self.bot_conn = sqlite3.connect(self.bot_db_path)
        self.vars_conn = sqlite3.connect(self.vars_db_path)

        self.bot_cursor = self.bot_conn.cursor()
        self.vars_cursor = self.vars_conn.cursor()

        self.init_git_repo()

        self.bot_cursor.execute(
            """CREATE TABLE IF NOT EXISTS bot (
                                   user_id INTEGER PRIMARY KEY,
                                   api_id TEXT,
                                   api_hash TEXT,
                                   bot_token TEXT,
                                   session_string TEXT)"""
        )

        self.vars_cursor.execute(
            """CREATE TABLE IF NOT EXISTS vars (
                                    user_id INTEGER,
                                    var_key TEXT,
                                    query_name TEXT,
                                    value TEXT,
                                    PRIMARY KEY (user_id, var_key, query_name))"""
        )

    def init_git_repo(self):
        if not os.path.exists(os.path.join(self.backup_dir, ".git")):
            subprocess.run(["git", "init"], cwd=self.backup_dir)
            subprocess.run(["git", "config", "user.name", "dependabot[bot]"], cwd=self.backup_dir)
            subprocess.run(
                ["git", "config", "user.email", "49699333+dependabot[bot]@users.noreply.github.com"], cwd=self.backup_dir
            )

    def backup_database(self):
        timestamp = datetime.now(self.timezone).strftime("%Y%m%d_%H%M%S")
        bot_backup_path = os.path.join(self.backup_dir, f"bot_backup_{timestamp}.db")
        vars_backup_path = os.path.join(self.backup_dir, f"vars_backup_{timestamp}.db")

        shutil.copy2(self.bot_db_path, bot_backup_path)
        shutil.copy2(self.vars_db_path, vars_backup_path)

        self.commit_to_git(bot_backup_path)
        self.commit_to_git(vars_backup_path)

    def commit_to_git(self, backup_path):
        subprocess.run(["git", "add", backup_path], cwd=self.backup_dir)
        commit_message = f"Backup database on {datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], cwd=self.backup_dir)

    # Variabel methods
    def setVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        self.vars_cursor.execute(
            """INSERT OR REPLACE INTO vars (user_id, var_key, query_name, value)
                                    VALUES (?, ?, ?, ?)""",
            (user_id, var_key, query_name, value),
        )
        self.vars_conn.commit()
        self.backup_database()

    def getVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        self.vars_cursor.execute(
            """SELECT value FROM vars WHERE user_id = ? AND var_key = ? AND query_name = ?""", (user_id, var_key, query_name)
        )
        result = self.vars_cursor.fetchone()
        return result[0] if result else None

    def removeVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        self.vars_cursor.execute(
            """DELETE FROM vars WHERE user_id = ? AND var_key = ? AND query_name = ?""", (user_id, var_key, query_name)
        )
        self.vars_conn.commit()
        self.backup_database()

    # Bot-related methods
    def saveBot(self, user_id: int, api_id: str, api_hash: str, value: str, is_token: bool = True):
        field = "bot_token" if is_token else "session_string"
        self.bot_cursor.execute(
            f"""INSERT OR REPLACE INTO bot (user_id, api_id, api_hash, {field})
                                   VALUES (?, ?, ?, ?)""",
            (user_id, api_id, api_hash, value),
        )
        self.bot_conn.commit()
        self.backup_database()

    def getBots(self, is_token: bool = True):
        field = "bot_token" if is_token else "session_string"
        self.bot_cursor.execute(f"""SELECT user_id, api_id, api_hash, {field} FROM bot WHERE {field} IS NOT NULL""")
        return [
            {"user_id": bot_data[0], "api_id": bot_data[1], "api_hash": bot_data[2], field: bot_data[3]}
            for bot_data in self.bot_cursor.fetchall()
        ]

    def removeBot(self, user_id: int):
        self.bot_cursor.execute("""DELETE FROM bot WHERE user_id = ?""", (user_id,))
        self.bot_conn.commit()
        self.backup_database()


#  __  __  ____  _   _  _____  ____    _____       _______       ____           _____ ______  #
# |  \/  |/ __ \| \ | |/ ____|/ __ \  |  __ \   /\|__   __|/\   |  _ \   /\    / ____|  ____| #
# | \  / | |  | |  \| | |  __| |  | | | |  | | /  \  | |  /  \  | |_) | /  \  | (___ | |__    #
# | |\/| | |  | | . ` | | |_ | |  | | | |  | |/ /\ \ | | / /\ \ |  _ < / /\ \  \___ \|  __|   #
# | |  | | |__| | |\  | |__| | |__| | | |__| / ____ \| |/ ____ \| |_) / ____ \ ____) | |____  #
# |_|  |_|\____/|_| \_|\_____|\____/  |_____/_/    \_\_/_/    \_\____/_/    \_\_____/|______| #


class MongoDataBase:
    def __init__(
        self,
        mongo_url: str,
        client_name: str = "mytoolsID",
        vars_name: str = "myDbTools",
        bot_collection: str = "myBots",
        binary_keys: int = 14151819154911914,
    ):
        self.setup = MongoClient(mongo_url)
        self.data = self.setup[client_name]
        self.vars = self.data[vars_name]
        self.bot = self.data[bot_collection]
        self.binary = BinaryEncryptor(binary_keys)

    # Variabel methods
    def setVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        update_data = {"$set": {f"{var_key}.{query_name}": value}}
        self.vars.update_one({"_id": user_id}, update_data, upsert=True)

    def getVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        result = self.vars.find_one({"_id": user_id})
        return result.get(var_key, {}).get(query_name, None) if result else None

    def removeVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        update_data = {"$unset": {f"{var_key}.{query_name}": ""}}
        self.vars.update_one({"_id": user_id}, update_data)

    def setListVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        update_data = {"$push": {f"{var_key}.{query_name}": value}}
        self.vars.update_one({"_id": user_id}, update_data, upsert=True)

    def getListVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        result = self.vars.find_one({"_id": user_id})
        return result.get(var_key, {}).get(query_name, []) if result else []

    def removeListVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        update_data = {"$pull": {f"{var_key}.{query_name}": value}}
        self.vars.update_one({"_id": user_id}, update_data)

    def removeAllVars(self, user_id: int, var_key: str = "variabel"):
        update_data = {"$unset": {var_key: ""}}
        self.vars.update_one({"_id": user_id}, update_data)

    def allVars(self, user_id: int, var_key: str = "variabel"):
        result = self.vars.find_one({"_id": user_id})
        return result.get(var_key, {}) if result else {}

    # Bot-related methods
    def saveBot(self, user_id: int, api_id: int, api_hash: str, value: str, is_token: bool = False):
        update_data = {
            "$set": {
                "api_id": self.binary.encrypt(api_id),
                "api_hash": self.binary.encrypt(api_hash),
                "bot_token" if is_token else "session_string": self.binary.encrypt(value),
            }
        }
        return self.bot.update_one({"user_id": user_id}, update_data, upsert=True)

    def getBots(self, is_token: bool = False):
        field = "bot_token" if is_token else "session_string"
        return [
            {
                "name": str(bot_data["user_id"]),
                "api_id": self.binary.decrypt(bot_data["api_id"]),
                "api_hash": self.binary.decrypt(bot_data["api_hash"]),
                field: self.binary.decrypt(bot_data.get(field)),
            }
            for bot_data in self.bot.find({"user_id": {"$exists": 1}})
        ]

    def removeBot(self, user_id: int):
        return self.bot.delete_one({"user_id": user_id})
