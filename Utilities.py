import pymongo
from pymongo import MongoClient
from bson import DBRef

class Utilities:

    # startup - creates the connection and returns the database client."""
    @staticmethod
    def startup():
        # print ("--------------------------------------------")
        # print("Connecting to MongoDB...")
        cluster = "mongodb+srv://adminuser:1234@cluster0.yrp2gy4.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(cluster)
        # I could also have said "db = client.demo_database" to do the same thing.
        db = client.ParkingGarage
        # print("Successful")
        return db