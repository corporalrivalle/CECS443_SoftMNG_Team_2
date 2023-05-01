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
    - allowws us to print and display arbitrary data that would usable be "ugly" into a more human readable form
 - import pymongo
    - used to connect to our systems mongo database
 - from Utilities import Utilities
     - Utilities.py is used to connect to your mongodb cluster (need to have a mongodb account with a cluster created)
 - from  termcolor import colored
    - used to help our system display the parking garage with colored spots, each color representing a spot status
 - import re
    - the regulare expression operations library, used as our email validator for user sign up
 - import pyfiglet
    - used to make our amazing line art display

# How it works/General Concept:

The Parking Garage is an automated system designed to allow drivers(users) to access the parking structure without the need for human supervision. The garage allows users to pick what floor and spot number they want to use. the system will take note of what spot is reserved by assigning the users information to that spot number. The system takes into account the status of a parking spot on any floor when someone makes a reservation. if a spot is available, the spot is highlighted blue/green(for electric cars). if A spot is already reserved or in use then the spot is highlighted red and the user cannot reserve that spot. When I user is leaving the garage the system will have the user confirm what spot they're are leaving. When correctly entered the spot will be changed back to blue nad the user exits the lot. the System also allows users to create an account and reserve a spot ahead of time. After signing up the user will be allowed to pick a spot to reserve. this is the general implementation of the automated parking garage.

# Individual Features:

- allow a user to sign up for an account 
- allow a user to sign into their account
- exit the program
- reserve a spot by choosing the floor and parking spot
- add/change a license plate to users account to have on file.
- add funds to a users account
- remove a registered license plate from an account
- allow users to see their account details
- allow a user to delete an account
- allow users to change the password to their account
- allows a user to log out of their account

# Features involving Mongo-DB

On the back end we use a Mongo Db to store information about the parking structures as well as the users themselves using the system. The database is split into three separate collections: each item or "Document" in the data base is given its own object ID for reference by mongo-db

## Parking Data Collections:

This database contains information about the parking structure spots. the following files are :
- Floor#: holds the floor number
- Spot#: holds the spot number for the floor
- Reserve_status: boolean value, true if the spot is taken, false if empty
- Reserve_name: holds the name of the user occupying the space, null if empty


## User Credentials Collections:

This collections stores the user credentials stored to validate a users login
- Username: stores the name of the user
- password: stores the users account password
- email: stores the users email.


## User Data Collection:

This collections stores users account information
- username: stores the name of the user
- password: stores the users account password
- email: stores the users email.
- Balance: stores the users balance/ wallet
- Car_plate: stores the car plate registered with the account


# GitHub Link:

https://github.com/corporalrivalle/CECS443_SoftMNG_Team_2




