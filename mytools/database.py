import json
import os

from pymongo import MongoClient

from .encrypt import CryptoEncryptor

#  _      ____   _____          _        _____       _______       ____           _____ ______  #
# | |    / __ \ / ____|   /\   | |      |  __ \   /\|__   __|/\   |  _ \   /\    / ____|  ____| #
# | |   | |  | | |       /  \  | |      | |  | | /  \  | |  /  \  | |_) | /  \  | (___ | |__    #
# | |   | |  | | |      / /\ \ | |      | |  | |/ /\ \ | | / /\ \ |  _ < / /\ \  \___ \|  __|   #
# | |___| |__| | |____ / ____ \| |____  | |__| / ____ \| |/ ____ \| |_) / ____ \ ____) | |____  #
# |______\____/ \_____/_/    \_\______| |_____/_/    \_\_/_/    \_\____/_/    \_\_____/|______| #


class LocalDataBase:
    def __init__(
        self,
        client_name: str = "mytoolsID",
        vars_name: str = "myVars",
        bot_collection: str = "myBots",
        crypto_keys: int = 14151819154911914,
    ):
        self.crypto = CryptoEncryptor(str(crypto_keys))
        self.vars_file = f"{client_name}_{vars_name}.json"
        self.bots_file = f"{client_name}_{bot_collection}.json"
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
            "api_id": self.crypto.encrypt(str(api_id)),
            "api_hash": self.crypto.encrypt(api_hash),
            field: self.crypto.encrypt(value),
        }
        data.append(entry)
        self._save_bots(data)

    def getBots(self, is_token: bool = False):
        field = "bot_token" if is_token else "session_string"
        return [
            {
                "name": str(bot_data["user_id"]),
                "api_id": int(self.crypto.decrypt(str(bot_data["api_id"]))),
                "api_hash": self.crypto.decrypt(bot_data["api_hash"]),
                field: self.crypto.decrypt(bot_data.get(field)),
            }
            for bot_data in self._load_bots()
        ]

    def removeBot(self, user_id: int):
        data = self._load_bots()
        self._save_bots([bot for bot in data if bot["user_id"] != user_id])

    def _load_vars(self):
        with open(self.vars_file, "r") as f:
            return json.load(f)

    def _save_vars(self, data):
        with open(self.vars_file, "w") as f:
            json.dump(data, f, indent=4)

    def _load_bots(self):
        with open(self.bots_file, "r") as f:
            return json.load(f)

    def _save_bots(self, data):
        with open(self.bots_file, "w") as f:
            json.dump(data, f, indent=4)

    def _initialize_files(self):
        for file in [self.vars_file, self.bots_file]:
            if not os.path.exists(file):
                self._save_vars({}) if file == self.vars_file else self._save_bots([])


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
        crypto_keys: int = 14151819154911914,
    ):
        self.setup = MongoClient(mongo_url)
        self.data = self.setup[client_name]
        self.vars = self.data[vars_name]
        self.bot = self.data[bot_collection]
        self.crypto = CryptoEncryptor(str(crypto_keys))

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
                "api_id": self.crypto.encrypt(str(api_id)),
                "api_hash": self.crypto.encrypt(api_hash),
                "bot_token" if is_token else "session_string": self.crypto.encrypt(value),
            }
        }
        return self.bot.update_one({"user_id": user_id}, update_data, upsert=True)

    def getBots(self, is_token: bool = False):
        field = "bot_token" if is_token else "session_string"
        return [
            {
                "name": str(bot_data["user_id"]),
                "api_id": int(self.crypto.decrypt(str(bot_data["api_id"]))),
                "api_hash": self.crypto.decrypt(bot_data["api_hash"]),
                field: self.crypto.decrypt(bot_data.get(field)),
            }
            for bot_data in self.bot.find({"user_id": {"$exists": 1}})
        ]

    def removeBot(self, user_id: int):
        return self.bot.delete_one({"user_id": user_id})
