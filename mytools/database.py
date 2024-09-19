from pymongo import MongoClient

class DataBase:
    def __init__(self, mongo_url: str, client_name: str = "mytoolsID", vars_name: str = "dBmyToolsID"):
        self.setup = MongoClient(mongo_url)
        self.data = self.setup[client_name]
        self.vars = self.data[vars_name]

    def setVars(self, user_id: int, query_name: str, value: str, var_key: str = "variabel"):
        update_data = {"$set": {f"{var_key}.{query_name}": value}}
        self.vars.update_one({"_id": user_id}, update_data, upsert=True)

    def getVars(self, user_id: int, query_name: str, var_key: str = "variabel"):
        result = self.vars.find_one({"_id": user_id})
        return result.get(var_key, {}).get(query_name, None) if result else None

    def allVars(self, user_id: int, var_key: str = "variabel"):
        result = self.vars.find_one({"_id": user_id})
        return result.get(var_key, {}) if result else {}

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
