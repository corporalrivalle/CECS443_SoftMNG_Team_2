# CECS443_SoftMNG_Team_2

ParkingGarage.py is the main file written by Johnnie Mares 

ParkingGarageMain.py is the refactored file written by Derek Zhang
 - Updated sections for this segment can be found in the branch "main-refactor" 

ParkingGarage(ver2).py and Utilities.py are the files written by Dat Pham

 - ParkingGarage(ver2).py is the whole program.
 - need to run "pip install pymongo" in the terminal to download pymongo

 # Libraries:
 - from datetime import datetime
    - usd to implement all the time related features of the product.
 - from pprint import pprint
    - allowws us to print and display arbitrary dta that would useable be "ugly" into a more human readable form
 - import pymongo
    - used to connect to our systems mongo database
 - from bson import DBRef
    - second library used to interct with our backend mongo database
 - from pymongo import MongoClient
    - thrid library used to have out system connect to our mongo DB
 - from Utilities import Utilities
     - Utilities.py is used to connect to your mongodb cluster (need to have a mongodb account with a cluster created)
 - from  termcolor import colored
    - used to help our system display the parking garage with colored spots, each color representing a spot status
 - import re
    - the regulare expression operations library, used as our email validator for user sign up
 - import pyfiglet
    - used to make our amazing line art display

# How it works:

The Parking Garage is an automated system designed to


