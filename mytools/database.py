import json
import os
import subprocess
from typing import Dict, List

from pymongo import MongoClient

from .encrypt import BinaryEncryptor, CryptoEncryptor

#  _      ____   _____          _        _____       _______       ____           _____ ______  #
# | |    / __ \ / ____|   /\   | |      |  __ \   /\|__   __|/\   |  _ \   /\    / ____|  ____| #
# | |   | |  | | |       /  \  | |      | |  | | /  \  | |  /  \  | |_) | /  \  | (___ | |__    #
# | |   | |  | | |      / /\ \ | |      | |  | |/ /\ \ | | / /\ \ |  _ < / /\ \  \___ \|  __|   #
# | |___| |__| | |____ / ____ \| |____  | |__| / ____ \| |/ ____ \| |_) / ____ \ ____) | |____  #
# |______\____/ \_____/_/    \_\______| |_____/_/    \_\_/_/    \_\____/_/    \_\_____/|______| #


class LocalDataBase:
    def __init__(
        self,
        client_name: str = "dB",
        vars_name: str = "vars",
        bot_collection: str = "bots",
        binary_keys: int = 14151819154911914,
    ):
        self.binary = BinaryEncryptor(int(binary_keys))
        self.vars_file = f"{client_name}_{vars_name}.json"
        self.bots_file = f"{client_name}_{bot_collection}.json"
        self.git_repo_path = "."
        self._initialize_files()

    # Variable methods
    def setVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        data = self._load_vars()
        user_data = data.setdefault(str(user_id), {var_key: {}})
        user_data[var_key][query_name] = value
        self._save_vars(data)

    def getVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        return self._load_vars().get(str(user_id), {}).get(var_key, {}).get(query_name)

    def removeVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        data = self._load_vars()
        if str(user_id) in data:
            data[str(user_id)][var_key].pop(query_name, None)
            self._save_vars(data)

    def setListVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        data = self._load_vars()
        user_data = data.setdefault(str(user_id), {var_key: {}})
        user_data[var_key].setdefault(query_name, []).append(value)
        self._save_vars(data)

    def getListVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        return self._load_vars().get(str(user_id), {}).get(var_key, {}).get(query_name, [])

    def removeListVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        data = self._load_vars()
        if str(user_id) in data and query_name in data[str(user_id)][var_key]:
            data[str(user_id)][var_key][query_name].remove(value)
            self._save_vars(data)

    def removeAllVars(self, user_id: int):
        data = self._load_vars()
        data.pop(str(user_id), None)
        self._save_vars(data)

    def allVars(self, user_id: int, var_key: str = "variabel"):
        return self._load_vars().get(str(user_id), {}).get(var_key, {})

    # Bot-related methods
    def saveBot(self, user_id: int, api_id: int, api_hash: str, value: str, is_token: bool = False):
        data = self._load_bots()
        field = "bot_token" if is_token else "session_string"
        entry = {
            "user_id": user_id,
            "api_id": self.binary.encrypt(str(api_id)),
            "api_hash": self.binary.encrypt(api_hash),
            field: self.binary.encrypt(value),
        }
        data.append(entry)
        self._save_bots(data)

    def getBots(self, is_token: bool = False) -> List[Dict]:
        field = "bot_token" if is_token else "session_string"
        return [
            {
                "name": str(bot_data["user_id"]),
                "api_id": int(self.binary.decrypt(str(bot_data["api_id"]))),
                "api_hash": self.binary.decrypt(bot_data["api_hash"]),
                field: self.binary.decrypt(bot_data.get(field)),
            }
            for bot_data in self._load_bots()
            if bot_data.get(field)
        ]

    def removeBot(self, user_id: int):
        data = self._load_bots()
        self._save_bots([bot for bot in data if bot["user_id"] != user_id])

    def _load_vars(self) -> dict:
        try:
            with open(self.vars_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_vars(self, data: dict):
        with open(self.vars_file, "w") as f:
            json.dump(data, f, indent=4)

    def _load_bots(self) -> list:
        try:
            with open(self.bots_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_bots(self, data: list):
        with open(self.bots_file, "w") as f:
            json.dump(data, f, indent=4)

    def _initialize_files(self):
        for file in [self.vars_file, self.bots_file]:
            if not os.path.exists(file):
                self._save_vars({}) if file == self.vars_file else self._save_bots([])

    def _git_commit(self, username: str, token: str, message: str = "auto commit backup database"):
        try:
            subprocess.run(["git", "add", self.vars_file, self.bots_file], cwd=self.git_repo_path, check=True)
            subprocess.run(["git", "commit", "-m", message], cwd=self.git_repo_path, check=True)

            subprocess.run(f'echo "{username}:{token}" | git push', cwd=self.git_repo_path, shell=True, check=True)
            print("Backup committed and pushed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during git operations: {e}")


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
        crypto_keys: int = 14151819154911914,
    ):
        self.setup = MongoClient(mongo_url)
        self.data = self.setup[client_name]
        self.crypto = CryptoEncryptor(str(crypto_keys))

    # Variabel methods
    def setVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        update_data = {"$set": {f"{var_key}.{query_name}": value}}
        self.data.vars.update_one({"_id": user_id}, update_data, upsert=True)

    def getVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        result = self.data.vars.find_one({"_id": user_id})
        return result.get(var_key, {}).get(query_name, None) if result else None

    def removeVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        update_data = {"$unset": {f"{var_key}.{query_name}": ""}}
        self.data.vars.update_one({"_id": user_id}, update_data)

    def setListVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        update_data = {"$push": {f"{var_key}.{query_name}": value}}
        self.data.vars.update_one({"_id": user_id}, update_data, upsert=True)

    def getListVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        result = self.data.vars.find_one({"_id": user_id})
        return result.get(var_key, {}).get(query_name, []) if result else []

    def removeListVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        update_data = {"$pull": {f"{var_key}.{query_name}": value}}
        self.data.vars.update_one({"_id": user_id}, update_data)

    def removeAllVars(self, user_id: int, var_key: str = "variabel"):
        update_data = {"$unset": {var_key: ""}}
        self.data.vars.update_one({"_id": user_id}, update_data)

    def allVars(self, user_id: int, var_key: str = "variabel"):
        result = self.data.vars.find_one({"_id": user_id})
        return result.get(var_key, {}) if result else {}

    # Bot-related methods
    def saveBot(self, user_id: int, api_id: int, api_hash: str, value: str, is_token: bool = False):
        update_data = {
            "$set": {
                "api_id": self.crypto.encrypt(str(api_id)),
                "api_hash": self.crypto.encrypt(api_hash),
                "bot_token" if is_token else "session_string": self.crypto.encrypt(value),
            }
        }
        return self.data.bot.update_one({"user_id": user_id}, update_data, upsert=True)

    def getBots(self, is_token: bool = False):
        field = "bot_token" if is_token else "session_string"
        return [
            {
                "name": str(bot_data["user_id"]),
                "api_id": int(self.crypto.decrypt(str(bot_data["api_id"]))),
                "api_hash": self.crypto.decrypt(bot_data["api_hash"]),
                field: self.crypto.decrypt(bot_data.get(field)),
            }
            for bot_data in self.data.bot.find({"user_id": {"$exists": 1}})
        ]

    def removeBot(self, user_id: int):
        return self.data.bot.delete_one({"user_id": user_id})
