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

    # testing(parkingData)

    logged_in_username = ""
    leave_login = False
    leave_parking_garage = False
    leave_program = False
    while 1:
        if (leave_login == False):
            print_login_menu()

            try:
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
                        populate(db, userCredentials, userData, parkingData)
                    case 5:
                        delete_existing_data(db, userCredentials, userData, parkingData)
                    
                
                # if leave_login == True:
                #     break
                if (leave_parking_garage == True) & (leave_login == True):
                    break

            except:
                print("not a valid entry, try again")

            # if login successful! or program is not exit, This is where the user able to login to our app
            #  This is where we can put our parking garage functionalities (reserve, add balance, etc) 

            if (leave_parking_garage == False) & (leave_login == True):

                while 1:
                    try:
                        print_parking_garage_menu(logged_in_username)    
                        my_parking_garage_choice = int(input())

                        match my_parking_garage_choice:
                            case 1: #Reserve 
                                print("1: Reserving")
                                rows = 3
                                cols = 6
                                mat = [[0 for _ in range(cols)] for _ in range(rows)]
                            
                            
                                # for parkingData_document in parkingData.find({}):
                                #     if (parkingData_document["reserve_status"] == False):
                                #         mat[parkingData_document["floor#"]] [parkingData_document["spot#"]] = colored('|_____|', 'blue');
                                #     else:
                                #         mat[parkingData_document["floor#"]] [parkingData_document["spot#"]] = colored('|_____|', 'red');
                                
                                showGarage(mat,rows,cols, parkingData)
                                reserveSpot(mat, parkingData, logged_in_username, userData, cols)
                                showGarage(mat,rows,cols, parkingData)

                            case 2: # leave Reserve
                                #call leave reserve function here
                                rows = 3
                                cols = 6
                                mat = [[0 for _ in range(cols)] for _ in range(rows)]
                                showGarage(mat,rows,cols, parkingData)
                                leavingLot(mat, parkingData, logged_in_username, userData, cols)
                                showGarage(mat,rows,cols, parkingData)


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

                            case 5: #See Account details
                                for user_data_document in userData.find({}):
                                    if (logged_in_username == user_data_document["username"]):
                                        print ("--------------------------------------------")
                                        print ("Your username is: ", user_data_document["username"])
                                        print ("Your password is: ", user_data_document["password"])
                                        print ("Your registered email is: ", user_data_document["email"])
                                        print ("Your current balance is: $", user_data_document["balance"])
                                        print ("Your registered carplate is: ", user_data_document["car_plate"])
                                        user_owned_parking_spot = []
                                        for parkingData_document in parkingData.find({}):
                                            if (parkingData_document["reserver_name"] == logged_in_username):
                                                user_owned_parking_spot.append(parkingData_document["_id"])
                                        print ("Your currently reserved Spots are: ")
                                        for i in user_owned_parking_spot:
                                            print (i)
                                        break
                            case 6: #delete account
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
                            
                            case 7:# change password
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

                                            





                            case 8: #Log out
                                print ("--------------------------------------------")
                                print ("logging out...")
                                logged_in_username = ""
                                leave_login = False
                                leave_parking_garage = True

                            case 9: # exit program
                                print ("goodbye!")
                                leave_login = True
                                leave_parking_garage = True

                    except:
                        print("invalid entry, try again" ) 
                        
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
    print("2: Leave Reserve")
    print("3: Add Balance")
    print("4: Add/Change A Carplate")
    print("5: See Your Account Details")
    print("6: Delete Account")
    print("7: Change Password")    
    print("8: Log Out")
    print("9: Exit Program")


# delete account? change email?  change password? remove carplate?



def populate (db, userCredentials, userData, parkingData):

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

    parkingData_result = parkingData.insert_many( [
        {"floor#": 0, "spot#": 0, "reserve_status": False, "reserver_name": None},
        {"floor#": 0, "spot#": 1, "reserve_status": False, "reserver_name": None},
        {"floor#": 0, "spot#": 2, "reserve_status": False, "reserver_name": None},
        {"floor#": 0, "spot#": 3, "reserve_status": True, "reserver_name": "user2"},
        {"floor#": 0, "spot#": 4, "reserve_status": False, "reserver_name": None},
        {"floor#": 0, "spot#": 5, "reserve_status": False, "reserver_name": None},

        {"floor#": 1, "spot#": 0, "reserve_status": False, "reserver_name": None},
        {"floor#": 1, "spot#": 1, "reserve_status": False, "reserver_name": None},
        {"floor#": 1, "spot#": 2, "reserve_status": False, "reserver_name": None},
        {"floor#": 1, "spot#": 3, "reserve_status": False, "reserver_name": None},
        {"floor#": 1, "spot#": 4, "reserve_status": False, "reserver_name": None},
        {"floor#": 1, "spot#": 5, "reserve_status": False, "reserver_name": None},

        {"floor#": 2, "spot#": 0, "reserve_status": False, "reserver_name": None},
        {"floor#": 2, "spot#": 1, "reserve_status": True, "reserver_name": "user1"},
        {"floor#": 2, "spot#": 2, "reserve_status": False, "reserver_name": None},
        {"floor#": 2, "spot#": 3, "reserve_status": False, "reserver_name": None},
        {"floor#": 2, "spot#": 4, "reserve_status": False, "reserver_name": None},
        {"floor#": 2, "spot#": 5, "reserve_status": False, "reserver_name": None},


    ])
    print ("--------------------------------------------")
    print ("Populate successfully")

def delete_existing_data(db, userCredentials, userData, parkingData):
    # Clear all currently existing data in all table table
    userCredentials.delete_many({})
    userData.delete_many({})
    parkingData.delete_many({})
    print ("--------------------------------------------")
    print ("Delete successfully")

def showGarage(mat,r,c, parkingData):
    for parkingData_document in parkingData.find({}):
        if (parkingData_document["reserve_status"] == False):
            mat[parkingData_document["floor#"]] [parkingData_document["spot#"]] = colored('|_____|', 'blue');
        else:
            mat[parkingData_document["floor#"]] [parkingData_document["spot#"]] = colored('|_____|', 'red');
    
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


def reserveSpot(mat, parkingData, logged_in_username, userData, cols):

    leave_reserveSpot = False
    a =[]
    input1 = False
    input2 = False
    while(input1 == False):
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
            if(spot_input > cols-1 or spot_input <1 ):
                print("invalid spot number, please try again")
            else:
                print ("You selected parking Slot ", floor_name.upper(), spot_input )
                input2 = True
        except:
             print("not a number, try again")






    for parkingData_document in parkingData.find({}):
         
         if (parkingData_document["floor#"] == floor_input) and (parkingData_document["spot#"] == spot_input-1) and (parkingData_document["reserver_name"] == None):

            for user_data_document in userData.find({}):
                if (logged_in_username == user_data_document["username"]) and (user_data_document["balance"] >= 10.0):                        
                    updated_balance = user_data_document["balance"] - 10.0
                    userData.update_one({"username": logged_in_username},
                        {"$set": {"balance": float(updated_balance)}})
                    parkingData.update_one({"_id": parkingData_document["_id"]},
                        {"$set": {"reserve_status": True}},)
                    parkingData.update_one({"_id": parkingData_document["_id"]},
                        {"$set": {"reserver_name": logged_in_username}},)
                    print ("--------------------------------------------")
                    print ("The selected parking Slot will cost $10.0...")
                    break

                elif ((logged_in_username == user_data_document["username"]) and (user_data_document["balance"] < 10.0)):
                    print ("--------------------------------------------")
                    print ("Insufficent fund to reserve, please add more money to your balance")
                    print ("Redirecting...")
                    leave_reserveSpot = True
                    break
            if (leave_reserveSpot == True):
                return mat


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




    for user_data_document in userData.find({}):
        if (logged_in_username == user_data_document["username"]):  
            print ("Your remaining balance is: $", user_data_document["balance"])
            print ("--------------------------------------------")
            break





    return mat

def leavingLot(mat, parkingData, logged_in_username, userData, cols):
    print(" You are now leaving the parking structure")
    print("please enter your floor number")
    leave_reserveSpot = True
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
            if(spot_input2 > cols-1 or spot_input2 <1 ):
                print("invalid spot number, please try again")
            else:
                print ("You selected parking Slot ", a[0].upper(), spot_input2 )
                input2 = True
        
    print("not a number, try again")



    for parkingData_document in parkingData.find({}):

        if (parkingData_document["floor#"] == floor_name) and (parkingData_document["spot#"] == spot_input2-1) and (parkingData_document["reserver_name"] == logged_in_username):

            for user_data_document in userData.find({}):
                parkingData.update_one({"_id": parkingData_document["_id"]},
                {"$set": {"reserve_status": False}},)
                parkingData.update_one({"_id": parkingData_document["_id"]},
                {"$set": {"reserver_name": None}},)

    if (leave_reserveSpot == True):
                return mat


main()