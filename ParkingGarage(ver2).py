#imports
import getpass
from datetime import datetime
from pprint import pprint

import pymongo
from bson import DBRef
from pymongo import MongoClient
from pprint import pprint
from Utilities import Utilities
from  termcolor import colored
import re
import pyfiglet
from datetime import datetime







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
 
    #Creating a schema
    parkingData = db.parkingData
    # Creating attributes for userCredentials schema
    parkingData.create_index([("floor#", pymongo.ASCENDING)],)
    parkingData.create_index([("spot#", pymongo.ASCENDING)])
    parkingData.create_index([("reserve_status", pymongo.ASCENDING)])
    parkingData.create_index([("reserver_username", pymongo.ASCENDING)])
    parkingData.create_index([("timestamp", pymongo.ASCENDING)])

    # testing(parkingData)
    ascii_banner = pyfiglet.figlet_format("Hello!!")
    print(ascii_banner)

    ascii_banner = pyfiglet.figlet_format("Welcome To The")
    print(ascii_banner)

    ascii_banner = pyfiglet.figlet_format("Automated Parking Garage!!")
    print(ascii_banner)



    logged_in_username = ""
    leave_login = False
    leave_parking_garage = False
    leave_program = False
    while 1:
        if (leave_login == False):
            print_login_menu()

            try:
                my_login_choice = int(input())
                if (my_login_choice < 1) or (my_login_choice > 5):
                    print ("--------------------------------------------")
                    print("Not a valid entry, try again")

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
                        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                        username_input = input("username: ")
                        password_input = input("password: ") 
                        while(1):
                           # try:
                                email_input = input("email: ")
                                if(re.fullmatch(regex,email_input)):
                                    break
                                else:
                                    print("invalid email, please try again")

                           # except:
                            #    print("invalid email format, try again")
                                

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
                        populate(db, userCredentials, userData, parkingData)
                    case 5:
                        delete_existing_data(db, userCredentials, userData, parkingData)
                    

                # if leave_login == True:
                #     break
                if (leave_parking_garage == True) & (leave_login == True):
                    break

            except:
                print ("--------------------------------------------")
                print("Not a valid entry, try again")

            # if login successful! or program is not exit, This is where the user able to login to our app
            #  This is where we can put our parking garage functionalities (reserve, unreserve, add balance, etc) 

            if (leave_parking_garage == False) & (leave_login == True):

                while 1:
                    try:
                        print_parking_garage_menu(logged_in_username)    
                        my_parking_garage_choice = int(input())
                        if (my_parking_garage_choice < 1) or (my_parking_garage_choice > 10):
                            print ("--------------------------------------------")
                            print("Not a valid entry, try again")
                        match my_parking_garage_choice:
                            case 1: #Reserve 
                                rows = 3
                                cols = 6
                                mat = [[0 for _ in range(cols)] for _ in range(rows)]
                            
                                print ("--------------------------------------------")                           
                                # showGarage(mat,rows,cols, parkingData)
                                reserveSpot(mat, parkingData, logged_in_username, userData, rows, cols)
                                # showGarage(mat,rows,cols, parkingData)

                            case 2: # leave Reserve
                                rows = 3
                                cols = 6
                                mat = [[0 for _ in range(cols)] for _ in range(rows)]

                                print ("--------------------------------------------")

                                leavingLot(mat, parkingData, logged_in_username, userData, cols, rows)



                            case 3: #Add Balance
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

                            case 4: #Add A Carplate
                                print ("--------------------------------------------")
                                carPlate_add_input = input("Please enter your new car plate to register: ")
                                for user_data_document in userData.find({}):
                                    # the input car plate has been registered to the database by a different user
                                    if (carPlate_add_input == user_data_document ["car_plate"]) & (logged_in_username != user_data_document["username"]):
                                        print ("--------------------------------------------")
                                        print ("Failed to register car plate!")                               
                                        print ("This car plate has been registered to a different user")
                                        break
                                    # the input carplate has been registered to the database by this user
                                    elif (carPlate_add_input == user_data_document ["car_plate"]) & (logged_in_username == user_data_document["username"]):
                                        print ("--------------------------------------------")
                                        print ("Failed to register car plate!") 
                                        print ("This car plate has been registered to your account")
                                        break

                                    elif (logged_in_username == user_data_document["username"]):
                                        userData.update_one({"username": logged_in_username},
                                                            {"$set": {"car_plate": carPlate_add_input.upper()}})
                                        print ("Adding car plate successfully!")                     
                                        break

                            case 5: #Remove  Registered Carplate
                                leave_remove_registered_carplate = False
                                for userData_document in userData.find({}):
                                    if (userData_document["username"] == logged_in_username):
                                        print ("--------------------------------------------")
                                        print ("The current registered car plate to your account is:", userData_document["car_plate"])
                                        break
                                while 1:     
                                    remove_choice = input("Are you sure you want to remove this car plate? Y/N --> ")

                                    if (remove_choice.upper() == "Y" ):
                                        # Remove carplate
                                        for userData_document in userData.find({}):
                                            if (userData_document["username"] == logged_in_username):
                                                userData.update_one({"username": logged_in_username},
                                                            {"$set": {"car_plate": None}})
                                                print ("--------------------------------------------")
                                                print("Removing successfully")
                                                leave_remove_registered_carplate = True
                                                break
                                        if (leave_remove_registered_carplate == True):
                                            break
                                        #exit case 5
                                    elif (remove_choice.upper() == "N" ):
                                        print ("Redirecting...")
                                        break
                                        #exit case 5
                                        pass
                                    else:
                                        print ("--------------------------------------------")
                                        print ("invalid choice")
                                        #invalid input
                                        pass


                            case 6: #See Account details
                                for user_data_document in userData.find({}):
                                    if (logged_in_username == user_data_document["username"]):
                                        print ("--------------------------------------------")
                                        print ("Your username is: ", user_data_document["username"])
                                        print ("Your password is: ", user_data_document["password"])
                                        print ("Your registered email is: ", user_data_document["email"])
                                        print ("Your current balance is: $", user_data_document["balance"])
                                        print ("Your registered carplate is: ", user_data_document["car_plate"])
                                        user_owned_parking_spot_id = []
                                        for parkingData_document in parkingData.find({}):
                                            if (parkingData_document["reserver_name"] == logged_in_username):
                                                user_owned_parking_spot_id.append(parkingData_document["_id"])
                                        print ("Your currently reserved Spots are: ")

                                        for id in user_owned_parking_spot_id:
                                            for parkingData_document in parkingData.find({}):
                                                if (parkingData_document["_id"] == id):
                                                    if (parkingData_document["floor#"] == 0):
                                                        print ("A", parkingData_document["spot#"]+1)
                                                        break
                                                    elif (parkingData_document["floor#"] == 1):
                                                        print ("B", parkingData_document["spot#"]+1)
                                                        break
                                                    elif (parkingData_document["floor#"] == 2):
                                                        print ("C", parkingData_document["spot#"]+1)
                                                        break
                                        break
                            case 7: #delete account
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
                            
                            case 8:# change password
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

                                            





                            case 9: #Log out
                                print ("--------------------------------------------")
                                print ("logging out...")
                                logged_in_username = ""
                                leave_login = False
                                leave_parking_garage = True

                            case 10: # exit program
                                print ("--------------------------------------------")
                                print ("goodbye!")
                                leave_login = True
                                leave_parking_garage = True
                        if leave_parking_garage == True:
                            break
                    except:
                        print ("--------------------------------------------")
                        print("Not a valid entry, try again" ) 
                        

                    
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
    print("2: Leave Reserve")
    print("3: Add Balance")
    print("4: Add/Change A Carplate")
    print("5: Remove Registered Carplate")
    print("6: See Your Account Details")
    print("7: Delete Account")
    print("8: Change Password")    
    print("9: Log Out")
    print("10: Exit Program")


# delete account? change email?  change password? remove carplate?



def populate (db, userCredentials, userData, parkingData):

    # inserting default data for user
    userCredentials_result = userCredentials.insert_many([
        {"username": "user1", "password": "passw1", "email": "user.01@gmail.com"},
        {"username": "user2", "password": "passw2", "email": "user.02@gmail.com"},
        {"username": "user3", "password": "passw3", "email": "user.03@gmail.com"},

    ])

    userData_result = userData.insert_many( [
        {"username": "user1", "password": "passw1", "email": "user.01@gmail.com", "balance": 10.0, "car_plate": "5EGC547"},
        {"username": "user2", "password": "passw2", "email": "user.02@gmail.com", "balance": 100.0, "car_plate": "4SDE258"},
        {"username": "user3", "password": "passw3", "email": "user.03@gmail.com", "balance": 50.25, "car_plate": None},
    ])

    parkingData_result = parkingData.insert_many( [
        {"floor#": 0, "spot#": 0, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 0, "spot#": 1, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 0, "spot#": 2, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 0, "spot#": 3, "reserve_status": True, "reserver_name": "user2", "timestamp": datetime.strptime("2023-04-29 12:00:00", "%Y-%m-%d %H:%M:%S")},
        {"floor#": 0, "spot#": 4, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 0, "spot#": 5, "reserve_status": False, "reserver_name": None, "timestamp": None},
#(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        {"floor#": 1, "spot#": 0, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 1, "spot#": 1, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 1, "spot#": 2, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 1, "spot#": 3, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 1, "spot#": 4, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 1, "spot#": 5, "reserve_status": False, "reserver_name": None, "timestamp": None},

        {"floor#": 2, "spot#": 0, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 2, "spot#": 1, "reserve_status": True, "reserver_name": "user1", "timestamp": datetime.strptime("2023-04-15 13:27:10", "%Y-%m-%d %H:%M:%S")},
        {"floor#": 2, "spot#": 2, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 2, "spot#": 3, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 2, "spot#": 4, "reserve_status": False, "reserver_name": None, "timestamp": None},
        {"floor#": 2, "spot#": 5, "reserve_status": False, "reserver_name": None, "timestamp": None},
    ])


    ## use to test when parking spot is all resereved
    # parkingData_result = parkingData.insert_many( [
    #     {"floor#": 0, "spot#": 0, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 0, "spot#": 1, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 0, "spot#": 2, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 0, "spot#": 3, "reserve_status": True, "reserver_name": "user2", "timestamp": None},
    #     {"floor#": 0, "spot#": 4, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 0, "spot#": 5, "reserve_status": True, "reserver_name": None, "timestamp": None},

    #     {"floor#": 1, "spot#": 0, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 1, "spot#": 1, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 1, "spot#": 2, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 1, "spot#": 3, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 1, "spot#": 4, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 1, "spot#": 5, "reserve_status": True, "reserver_name": None, "timestamp": None},

    #     {"floor#": 2, "spot#": 0, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 2, "spot#": 1, "reserve_status": True, "reserver_name": "user1", "timestamp": None},
    #     {"floor#": 2, "spot#": 2, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 2, "spot#": 3, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 2, "spot#": 4, "reserve_status": True, "reserver_name": None, "timestamp": None},
    #     {"floor#": 2, "spot#": 5, "reserve_status": True, "reserver_name": None, "timestamp": None},
    # ])


    print ("--------------------------------------------")
    print ("Populate successfully")

def delete_existing_data(db, userCredentials, userData, parkingData):
    # Clear all currently existing data in all table
    userCredentials.delete_many({})
    userData.delete_many({})
    parkingData.delete_many({})
    print ("--------------------------------------------")
    print ("Delete successfully")

def showGarage(mat,r,c, parkingData):
    unavailable_parking_counter = 0
    max_parking_spot = 18

    for parkingData_document in parkingData.find({}):
        if ( (parkingData_document["floor#"] == 0) or (parkingData_document["floor#"] == 1) or (parkingData_document["floor#"] == 2) ) and ( (parkingData_document["spot#"] == 0) or (parkingData_document["spot#"] == 1) ) and  (parkingData_document["reserve_status"] == False):
            mat[parkingData_document["floor#"]] [parkingData_document["spot#"]] = colored('|_____|', 'green') #electric parking

        elif ( (parkingData_document["floor#"] == 0) or (parkingData_document["floor#"] == 1) or (parkingData_document["floor#"] == 2) ) and ( (parkingData_document["spot#"] != 0) or (parkingData_document["spot#"] != 1) ) and  (parkingData_document["reserve_status"] == False):
            mat[parkingData_document["floor#"]] [parkingData_document["spot#"]] = colored('|_____|', 'blue') #regular parking 

        else:
            mat[parkingData_document["floor#"]] [parkingData_document["spot#"]] = colored('|_____|', 'red') #reserved parking
            unavailable_parking_counter += 1



    for i in range(r):
        if ( i == 0):
            print ("Floor A")
        elif ( i == 1):
            print ("Floor B")
        elif ( i == 2):
            print ("Floor C")
        for j in range(c):
            print(mat[i][j], end = " ")
        print("\n")

    print ("Available parking spot: ", max_parking_spot - unavailable_parking_counter)


def parking_is_full (mat, parkingData):
    max_parking_spot = 18
    reserved_counter = 0
    for parkingData_document in parkingData.find({}):
        if (parkingData_document['reserve_status'] == True ):
            reserved_counter += 1
    
    if (reserved_counter == max_parking_spot):
        return True # Parking Garage is  full
    else: 
        return False
    
def reserveSpot(mat, parkingData, logged_in_username, userData, rows, cols):

    if (parking_is_full(mat, parkingData) == False):

        for userData_document in userData.find({}):
            if (userData_document ["username"] == logged_in_username):
                if (userData_document["car_plate"] != None):
                    showGarage(mat, rows,cols , parkingData)
                    leave_reserveSpot = False
                    a =[]
                    input1 = False
                    input2 = False
                    while(input1 == False):
                        print ("--------------------------------------------")
                        floor_name = input("Please enter what floor you want. ex A, B or C  --> ")
                        if (floor_name.upper() == 'A')  or (floor_name.upper() == 'B')  or (floor_name.upper() == 'C'):
                            a.append(floor_name)
                            if(a[0]=='A'or a[0]=='a'):
                                    print ("--------------------------------------------")
                                    print("You Selected A floor")
                                    floor_input = 0
                                    input1 = True
                            elif(a[0]=='B' or a[0]=='b'):
                                    print ("--------------------------------------------")
                                    print("You Selected B floor")
                                    floor_input = 1
                                    input1=True
                            elif(a[0]=='C' or a[0]=='c'):
                                    print ("--------------------------------------------")
                                    print("You Selected C Floor")
                                    floor_input = 2
                                    input1=True
                        else: 
                            print ("invalid input")




                    print ("--------------------------------------------")
                    while(input2 == False):
                        
                        try:
                            spot_input=[]
                            spot_input = int(input("Please enter spot number you want to reserve (1-6) --> "))
                            if(spot_input > cols or spot_input <1 ):
                                print("invalid spot number, please try again")
                            else:
                                print ("You selected parking Slot ", floor_name.upper(), spot_input )
                                input2 = True
                        except:
                            print("not a number, try again")






                    for parkingData_document in parkingData.find({}):
                        
                        if (parkingData_document["floor#"] == floor_input) and (parkingData_document["spot#"] == spot_input-1) and (parkingData_document["reserver_name"] == None):

                            for user_data_document in userData.find({}):
                                if (logged_in_username == user_data_document["username"]):                        
                                    
                                    parkingData.update_one({"_id": parkingData_document["_id"]},
                                        {"$set": {"reserve_status": True}},)
                                    parkingData.update_one({"_id": parkingData_document["_id"]},
                                        {"$set": {"reserver_name": logged_in_username}},)
                                    parkingData.update_one({"_id": parkingData_document["_id"]},
                                        {"$set": {"timestamp": datetime.now()}},)
                                    break
                            print ("--------------------------------------------")
                            print ("Reserve successfully")
                            break
                        elif (parkingData_document["floor#"] == floor_input) and (parkingData_document["spot#"] == spot_input-1) and (parkingData_document["reserver_name"] == logged_in_username):
                            print ("--------------------------------------------")
                            print ("This current parking spot has been reserved by you")
                            print ("Redirecting...")
                            leave_reserveSpot = True
                        elif (parkingData_document["floor#"] == floor_input) and (parkingData_document["spot#"] == spot_input-1) and (parkingData_document["reserver_name"] != logged_in_username):
                            print ("--------------------------------------------")
                            print ("This current parking spot has been reserved by someone")
                            print ("Redirecting...")
                            leave_reserveSpot= True

                    if (leave_reserveSpot == True):
                        return mat





                    showGarage(mat, rows,cols , parkingData)
                else:
                    print ("--------------------------------------------")
                    print ("Your account does not have a car plate registered yet!\nPlease register a car plate to be able to reserve\n Redirecting...")
                    break
    else:
        print ("--------------------------------------------")
        print ("Sorry, our parking garage is now full! You can reserve once a parking spot is available \nRedirecting...")

    return mat

def leavingLot(mat, parkingData, logged_in_username, userData, cols, rows):
    unreserved_checker = False   
    for parkingData_document in parkingData.find({}):

        if (parkingData_document["reserver_name"] == logged_in_username):
            unreserved_checker = True
            break

    
    if (unreserved_checker == True):
        showGarage(mat,rows,cols, parkingData)
        a =[]
        input1 = False
        input2 = False
        while(input1 == False):
            floor_name = input("Please enter what floor you are leaving. ex A, B or C  --> ")

            if (floor_name.upper() == 'A')  or (floor_name.upper() == 'B')  or (floor_name.upper() == 'C'):
                a.append(floor_name)
                if(a[0]=='A'or a[0]=='a'):
                        print ("--------------------------------------------")
                        print("You Selected A floor")
                        floor_name = 0
                        input1 = True
                elif(a[0]=='B' or a[0]=='b'):
                        print ("--------------------------------------------")
                        print("You Selected B floor")
                        floor_name = 1
                        input1=True
                elif(a[0]=='C' or a[0]=='c'):
                        print ("--------------------------------------------")
                        print("You Selected C Floor")
                        floor_name = 2
                        input1=True

            else: 
                print ("invalid input")




        print ("--------------------------------------------")
        while(input2 == False):
            
            
                spot_input2=[]
                spot_input2 = int(input("Please enter spot number you want to leave (1-6) --> "))
                if(spot_input2 > cols or spot_input2 <1 ):
                    print("invalid spot number, please try again")
                else:
                    print ("--------------------------------------------")
                    print ("You selected parking Slot ", a[0].upper(), spot_input2 )
                    input2 = True
            




        for parkingData_document in parkingData.find({}):

            if (parkingData_document["floor#"] == floor_name) and (parkingData_document["spot#"] == spot_input2-1) and (parkingData_document["reserver_name"] == logged_in_username) and (parkingData_document["reserve_status"] == True):
                for userData_document in userData.find({}):
                    if (userData_document["username"] == logged_in_username):

                        if (userData_document["balance"] >= parking_cost_calculator(parkingData_document["timestamp"])):
                            
                            parkingData.update_one({"_id": parkingData_document["_id"]},
                                {"$set": {"reserve_status": False}},)
                            parkingData.update_one({"_id": parkingData_document["_id"]},
                                {"$set": {"reserver_name": None}},)
                            
                            
                            userBalance = userData_document["balance"]
                            parkingCost = parking_cost_calculator(parkingData_document["timestamp"])
                            
                            print ("Your parking cost : ", parkingCost )
                            print ("Your current balance: ", userData_document["balance"])
                            updated_balance = userBalance - parkingCost 
                        
                            userData.update_one({"_id": userData_document["_id"]},
                                            {"$set": {"balance": updated_balance}})

                            print ("--------------------------------------------")
                            print ("Unreserve successfully")
                            print ("Your remaining balance: ", updated_balance, "\n Redirecting...")
                            print ("--------------------------------------------")
                            break
                        else: 
                            print ("--------------------------------------------")
                            print ("Insufficent fund to reserve, please add more money to your balance")
                            print ("Payment for the parking spot: " , parking_cost_calculator(parkingData_document["timestamp"]) )
                            print ("Your current balance: ", userData_document["balance"])
                            print (" Redirecting...")
                            print ("--------------------------------------------")
                            break


            elif (parkingData_document["floor#"] == floor_name) and (parkingData_document["spot#"] == spot_input2-1) and (parkingData_document["reserver_name"] != logged_in_username) and (parkingData_document["reserve_status"] == True) and (parkingData_document["reserver_name"] != None):
                print ("--------------------------------------------")
                print ("You cannot leave reserve a spot that is not own by you! \n Redirecting...")
                print ("--------------------------------------------")
                break

            elif (parkingData_document["floor#"] == floor_name) and (parkingData_document["spot#"] == spot_input2-1) and (parkingData_document["reserver_name"] == None) and (parkingData_document["reserve_status"] == False):
                print ("--------------------------------------------")
                print ("You cannot leave reserve a spot that has not been reserved by anyone! \n Redirecting... ")
                print ("--------------------------------------------")
                break
        showGarage(mat,rows,cols, parkingData)

    else:
        print ("--------------------------------------------")
        print ("Can't unreserve because you have not reserve a spot yet \n Redirecting...")
        # break


    return mat
def parking_cost_calculator (start_time):

    elapsed_time_in_seconds = (datetime.now() - start_time).total_seconds()
    elapsed_time_hours = elapsed_time_in_seconds/3600
    if (elapsed_time_hours <= 12):
        return 10.0
    
    elif (elapsed_time_hours > 12) and (elapsed_time_hours < 24):
        return 15.0
    
    else: 
        return 20.0

main()