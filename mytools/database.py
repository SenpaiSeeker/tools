from typing import Union

from pymongo import MongoClient

from .encrypt import BinaryEncryptor


class DataBase:
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
    def saveBot(self, user_id: int, api_id: Union(str, int), api_hash: str, value: str, is_token: bool = False):
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
