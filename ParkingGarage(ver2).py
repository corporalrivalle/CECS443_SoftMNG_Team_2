#imports
import getpass
from datetime import datetime
from pprint import pprint

import pymongo
from bson import DBRef
from pymongo import MongoClient
from pprint import pprint
from Utilities import Utilities










#class definitions
class parkingSpace:
    def __init__(self) -> None:
        self.occupied = False #attribute to see if it is occupied
        self.cost = 10 #sets a default cost
        self.occupiedName=""
    
    def changeOccupied(self, name): #allows each space to flag whether its occupied or not
        self.occupied = not self.occupied
        self.occupiedName = name

    def setCost(self, newcost): #allows prices to change within each lot (and to change from default)
        self.cost = newcost
    
    def getOccupied(self):
        return self.occupied, self.occupiedName
    
    def getCost(self):
        return self.cost

class parkingLot: 
    def __init__(self, lotName,floors, spacePerFloor, costPerSpace) -> None:
        self.lotName = lotName
        self.floors = floors
        self.spacePerFloor = spacePerFloor
        self.capacity = floors*spacePerFloor
        self.originalCap = floors*spacePerFloor
        self.reservedSpace = {} #dictionary of currently reserved spaces
        self.lot = [] #stores parking Space objects on each floor (nested list)
        self.netProfit = 0

        for floor in range(floors): #creates a double nested list that holds values for each floor (we are assuming floors are identical)
            floorlot = []
            for spaces in range(spacePerFloor):
                newSpace = parkingSpace()
                newSpace.setCost(costPerSpace)
                floorlot.append(newSpace)
            self.lot.append(floorlot)

    def returnLot(self):
        return self.lot
    
    def incrementCapacity(self):
        if self.capacity==self.originalCap:
            print("Error! The lot is already empty!")
            return False #allows for checking if function worked
        else:
            self.capacity+=1
            return True
    
    def decrementCapacity(self):
        if self.capacity<=0:
            print("Error! The lot is at capacity!")
            return False #allows for chechking if function worked
        else:
            self.capacity-=1
            return True
    
    def getReserved(self):
        print(self.lotName)
        for key in self.reservedSpace:
            if self.reservedSpace[key]==[]:
                pass
            else:
                print(key,"|", self.reservedSpace[key])
    
    def getInfo(self):
        print("Total money earned by this lot:",self.netProfit)
        print("Amount of open spaces currently available:",self.capacity)
        

def reserveSpace(lot, reservedName): #pass in a parking lot object to reserve a space in
    for floor in lot.lot:
        for space in floor:
            if space.occupied==False:
                space.changeOccupied(reservedName)
                if reservedName in lot.reservedSpace.keys():
                    lot.reservedSpace[reservedName].append(space) #stores the reserved space in the lot under a dictionary with name as key and object as space
                else:
                    lot.reservedSpace[reservedName]=[space]
                lot.netProfit += space.getCost()
                lot.decrementCapacity()
                return
            else:
                pass

#empties all reservations under a specific name (must pass in a specific lot)
def emptyAllSpace_Name(name, lot):
    if name not in lot.reservedSpace.keys():
        print("Name not found! Please try again.")
    else:
        while lot.reservedSpace[name] != []:
            space = lot.reservedSpace[name][0]
            # print(space,":")
            space.changeOccupied("")
            lot.reservedSpace[name].remove(space)
            lot.incrementCapacity()
        print(lot.lotName,"has been cleared of all reserved spaces under the name",name)

def emptySpace_Obj(space, lot):
    success=False
    for key in lot.reservedSpace.keys():
        if space in lot.reservedSpace[key]:
            success = True
            space.changeOccupied("")
            lot.reservedSpace[key].remove(space)
            lot.incrementCapacity()
            print("Space has been removed from",key,"'s reservations.")
            return
    if not success:
        print("An error occured. Please check inputs and try again!")


#main function
def main():

    db = Utilities.startup()

    #Creating a schema
    userCredentials = db.userCredentials
    # Creating attributes for userCredentials schema
    userCredentials.create_index([("username", pymongo.ASCENDING)], unique=True)
    userCredentials.create_index([("password", pymongo.ASCENDING)])
    userCredentials.create_index([("email", pymongo.ASCENDING)], unique = True)


    #Creating a schema
    userData = db.userData
    # Creating attributes for userCredentials schema
    userData.create_index([("username", pymongo.ASCENDING)], unique=True)
    userData.create_index([("password", pymongo.ASCENDING)])
    userData.create_index([("email", pymongo.ASCENDING)], unique = True)
    userData.create_index([("balance", pymongo.ASCENDING)])
    userData.create_index([("car_plate", pymongo.ASCENDING)])
 




    logged_in_username = ""
    leave_login = False
    leave_parking_garage = False
    leave_program = False
    while 1:
        if (leave_login == False):
            print_login_menu()


            my_login_choice = int(input())


            match my_login_choice:
                case 1:
                    credentials_validator = False
                    print ("--------------------------------------------")
                    print ("Please enter your credentials")
                    username_input = input("username: ")
                    password_input = input("password: ")

                    # going through each userCredential in mongoDB to try to find a match
                    for userCredentials_document in userCredentials.find({}):
                        if ((userCredentials_document["username"] == str(username_input)) & 
                            (userCredentials_document["password"] == str(password_input))):
                            credentials_validator = True
                            break
                    if (credentials_validator == False):
                        print ("--------------------------------------------")
                        print ("invalid username or password!!")
                    else: 
                        print ("--------------------------------------------")
                        print ("Login Successfully!")
                        logged_in_username = str(username_input)
                        leave_login = True
                        leave_parking_garage = False

                case 2:
                    print ("--------------------------------------------")
                    print ("Please enter the fields below") 
                    username_input = input("username: ")
                    password_input = input("password: ") 
                    email_input = input("email: ")

                    username_validator = False
                    email_validator = False
                    for userCredentials_document in userCredentials.find({}):
                        # look for any existing username or email in the database
                        if ((userCredentials_document["username"] == str(username_input))):
                            username_validator = True
                        if  (userCredentials_document["email"] == str(email_input)):
                            email_validator = True

                    print ("--------------------------------------------")
                    if (username_validator == True):
                        print ("username has been used! Failed to signup!")
                    if (email_validator == True):
                        print ("email has been used! Failed to signup!")
                    if (username_validator == False & email_validator == False):
                        userCredentials.insert_one({"username": username_input, "password": password_input, "email": email_input})
                        userData.insert_one( {"username": username_input, "password": password_input, "email": email_input, "balance": 0.0, "car_plate": None})
                        print ("sign up successfully!")
                case 3:
                    print ("Good bye!")
                    leave_login = True
                    leave_parking_garage = True
                case 4:    
                    #used to populate some data. 
                    populate(db, userCredentials, userData)
                case 5:
                    delete_existing_data(db, userCredentials, userData)
                
            
            # if leave_login == True:
            #     break
            if (leave_parking_garage == True) & (leave_login == True):
                break



        # if login successful! or program is not exit, This is where the user able to login to our app
        #  This is where we can put our parking garage functionalities (reserve, add balance, etc) 

        if (leave_parking_garage == False) & (leave_login == True):

            while 1:

                print_parking_garage_menu(logged_in_username)    
                my_parking_garage_choice = int(input())

                match my_parking_garage_choice:
                    case 1: #Reserve 
                        print("1: Reserving")

                    case 2: #Add Balance
                        print ("--------------------------------------------")
                        updated_balance = 0.0
                        ammount_add_input = float(input("Enter your amount: $"))

                        for user_data_document in userData.find({}):
                            if (logged_in_username == user_data_document["username"]):                        
                                updated_balance = user_data_document["balance"] + float(ammount_add_input)
                                userData.update_one({"username": logged_in_username},
                                                     {"$set": {"balance": float(updated_balance)}})
                                print ("Adding balance successfully!")
                                break

                        for user_data_document in userData.find({}):
                            if (logged_in_username == user_data_document["username"]):  
                                print ("Your new balance is: $", user_data_document["balance"])
                                break

                    case 3: #Add A Carplate
                        print ("--------------------------------------------")
                        updated_balance = 0.0
                        carPlate_add_input = input("Please enter your new car plate to register: ")
                        for user_data_document in userData.find({}):
                            # the input car plate has been registered to the database by a different user
                            if (carPlate_add_input == user_data_document ["car_plate"]) & (logged_in_username != user_data_document["username"]):
                                print ("--------------------------------------------")
                                print ("Failed to register!")                               
                                print ("This car plate has been registered to a different user")
                                break
                            # the input carplate has been registered to the database by this user
                            elif (carPlate_add_input == user_data_document ["car_plate"]) & (logged_in_username == user_data_document["username"]):
                                print ("--------------------------------------------")
                                print ("Failed to register!") 
                                print ("This car plate has been registered to your account")
                                break

                            elif (logged_in_username == user_data_document["username"]):
                                userData.update_one({"username": logged_in_username},
                                                     {"$set": {"car_plate": carPlate_add_input}})
                                print ("Adding car plate successfully!")                     
                                break

                    case 4: #See Account details
                        for user_data_document in userData.find({}):
                            if (logged_in_username == user_data_document["username"]):
                                print ("--------------------------------------------")
                                print ("Your username is: ", user_data_document["username"])
                                print ("Your password is: ", user_data_document["password"])
                                print ("Your registered email is: ", user_data_document["email"])
                                print ("Your current balance is: $", user_data_document["balance"])
                                print ("Your registered carplate is: ", user_data_document["car_plate"])
 
                                break
                    case 5: #delete account
                        print ("--------------------------------------------")
                        delete_input = input("Are you sure you want to delete this account? Y/N: ")
                        exit_delete_account = False
                        while 1:

                            if (delete_input == "y") or (delete_input == "Y"):
                                #delete account
                                for userData_document in userData.find({}):
                                    if (userData_document["username"] == logged_in_username):
                                        db.userData.delete_one({"username": userData_document["username"]})
                                        db.userCredentials.delete_one({"username": userData_document["username"]})
                                        print ("--------------------------------------------")
                                        print ("Deletion successfully!")
                                        exit_delete_account = True
                                        logged_in_username = ""
                                        leave_login = False
                                        leave_parking_garage = True
                                        print ("Redirecting back to signin/signup menu...")
                                        break
                                pass
                            elif (delete_input == "n") or (delete_input == "N"):
                                #redirect to parking garage menu
                                exit_delete_account = True
                                print ("--------------------------------------------")
                                print ("Redirecting back to parking garage menu...")
                                pass
                            else: 
                                print ("invalid input")
                                delete_input = input("Are you sure you want to delete this account? Y/N: ")

                            if (exit_delete_account == True):
                                break
                    
                    case 6:# change password
                        print ("--------------------------------------------")
                        old_pass_input = input("Please enter your current password or exit: ")

                        exit_pass_change = False
                        while 1: 
                            if ( old_pass_input == "exit"):
                                print ("--------------------------------------------")
                                print ("Redirecting to parking garage menu....")
                                break
                            for userData_document in userData.find({}):
                                if (userData_document["password"] == old_pass_input):
                                    print ("--------------------------------------------")
                                    print ("Success")
                                    new_pass_input = input("Please enter your new password: ")
                                    userData.update_one({"username": logged_in_username},
                                                     {"$set": {"password": new_pass_input}})
                                    for userCredentials_document in userCredentials.find({}):
                                        userCredentials.update_one({"username": logged_in_username},
                                                     {"$set": {"password": new_pass_input}})
                                        break
                                    print ("Password changed")
                                    exit_pass_change = True
                                    print ("--------------------------------------------")
                                    print ("Redirecting to parking garage menu....")
                                    break
                            if (exit_pass_change == True) :
                                break 
                            print ("--------------------------------------------")
                            print ("invalid password")
                            old_pass_input = input("Please enter your current password or exit: ")

                                    





                    case 7: #Log out
                        print ("--------------------------------------------")
                        print ("logging out...")
                        logged_in_username = ""
                        leave_login = False
                        leave_parking_garage = True

                    case 8: # exit program
                        print ("goodbye!")
                        leave_login = True
                        leave_parking_garage = True

                
                if leave_parking_garage == True:
                    break
            if (leave_parking_garage == True) & (leave_login == True):
                break
def print_login_menu():
    print ("--------------------------------------------")
    print ("Welcome to the Automated parking garage. Please login or signup to use our program!")

    print("please select an option")
    print("1: Sign In")
    print("2: Sign Up")
    print("3: Exit")
    print("4: populate some default data to the database (used for testing)")
    print("5: delete existing data in the database (used for testing)")


def print_parking_garage_menu(logged_in_username):
    print ("--------------------------------------------")
    print ("Hello", logged_in_username, "! Welcome to the Automated parking garage!")
    print("Please select an option")
    print("1: Reserve")
    print("2: Add Balance")
    print("3: Add/Change A Carplate")
    print("4: See Your Account Details")
    print("5: Delete Account")
    print("6: Change Password")    
    print("7: Log Out")
    print("8: Exit Program")


# delete account? change email?  change password? remove carplate?



def populate (db, userCredentials, userData):

    # inserting default data for user
    userCredentials_result = userCredentials.insert_many([
        {"username": "user1", "password": "passw1", "email": "user.01@gmail.com"},
        {"username": "user2", "password": "passw2", "email": "user.02@gmail.com"},
        {"username": "user3", "password": "passw3", "email": "user.03@gmail.com"},

    ])

    userData_result = userData.insert_many( [
        {"username": "user1", "password": "passw1", "email": "user.01@gmail.com", "balance": 10.0, "car_plate": None},
        {"username": "user2", "password": "passw2", "email": "user.02@gmail.com", "balance": 100.0, "car_plate": None},
        {"username": "user3", "password": "passw3", "email": "user.03@gmail.com", "balance": 50.25, "car_plate": "4SDE258"},
    ])
    print ("--------------------------------------------")
    print ("Populate successfully")

def delete_existing_data(db, userCredentials, userData):
    # Clear all currently existing data in all table table
    userCredentials.delete_many({})
    userData.delete_many({})
    print ("--------------------------------------------")
    print ("Delete successfully")
main()