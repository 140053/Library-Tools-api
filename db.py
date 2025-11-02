import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read("config.ini")
db_conf = config["mysql"]

class Database:
    @staticmethod
    def connect():
        return mysql.connector.connect(
            host=db_conf.get("host"),
            user=db_conf.get("user"),
            password=db_conf.get("password"),
            database=db_conf.get("database"),
            port=db_conf.getint("port", 3306),
            auth_plugin=db_conf.get("auth_plugin", None)
        )
