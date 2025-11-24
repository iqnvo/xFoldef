from sqlite3 import connect
from typing import Optional
from dataclasses import dataclass
from pandas import DataFrame


@dataclass
class databaseConfig:
    
    databaseName:str = "DatabaseFlSessions.db"
    databaseLogName:str = f"{databaseName}Log.db"
    timeout:int = 10


class loaderDatabase(databaseConfig):

    tables:dict = {
        "session": "Sessions",
        "mac_address": "mac",
        "system": "os"
    }

    def __init__(self, config:Optional[databaseConfig] = None):
        
        self.__config = config or databaseConfig
        self.__connection = None
        self.__cursor = None

        self.configure()
    
    
    def __connect(self):
        if self.__connection is None:
            self.__connection = connect(self.__config.databaseName)
            self.__cursor = self.__connection.cursor()
        
    def addSession(self, ip, mac, system):
        self.__cursor.execute("INSERT INTO Sessions VALUES (?, ?, ?)", (ip, mac, system))
        self.__connection.commit()
    
    
    def sessions(self):
        t = self.tables
        self.__cursor.execute("SELECT * FROM Sessions")
        return DataFrame(self.__cursor.fetchall(), columns=[t["session"], t["mac_address"], t["system"]])
    
    def configure(self):
        self.__connect()
        database = self.__cursor
        database.execute("CREATE TABLE IF NOT EXISTS Sessions(ip TEXT, mac TEXT, system TEXT)")
        self.__connection.commit()
    
    def __enter__(self):
        self.configure()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.__connection is not None:
            self.__connection.commit()
            self.__cursor.close()
            self.__connection.close()
