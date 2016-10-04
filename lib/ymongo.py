import pymongo
import yfinance

from pymongo import MongoClient


class YMongo():
    

    def __init__(self, database, collection, user=None, password=None, hostname="localHost", port=27017):
        """
		Initializes connection to the MongoDb Database
        
        Parameters
        ----------
        collection : str
        database : str
        user : str, optional
        password: str, optional
        hostname: str, optional
            default: "localHost"
        port: int, optional
            default:27017
        """
        if user and password:
            db_uri = "mongodb://{user}:{pwd}@{host}:{port}".format(user=username,
                                                                    pwd=password,
                                                                    host=hostname,
                                                                    port=str(port))

        else:
            db_uri = "mongodb://{host}:{port}".format(host=hostname, port=str(port))

        self.db_conn = MongoClient(db_uri)
        self.collection = self.db_conn.get_database(database).get_collection(collection)

    def __str__(self):
        return str(self.db_conn)

    def __repr__(self):
        return str(self.db_conn)

    def __enter__(self):
        return self.collection

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                print("Database error: can't connect")
                raise exc_type
        finally:
            self.db_conn.close()