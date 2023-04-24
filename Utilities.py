import getpass
import pymongo
from pymongo import MongoClient
from bson import DBRef

class Utilities:

    # startup - creates the connection and returns the database client."""
    @staticmethod
    def startup():
        print ("--------------------------------------------")
        print("Connecting to atlast...")
        #password = getpass.getpass(prompt='MongoDB password --> ')
        cluster = "YOUR MONGODB CONNECTION STRING"
        client = MongoClient(cluster)
        # I could also have said "db = client.demo_database" to do the same thing.
        db = client.YOURDATABASENAME
        print("Successful")
        return db