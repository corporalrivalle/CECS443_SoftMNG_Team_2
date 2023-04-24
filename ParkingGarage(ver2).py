#imports
import getpass
from datetime import datetime
from pprint import pprint

import pymongo
from bson import DBRef
from pymongo import MongoClient
from pprint import pprint
from Utilities import Utilities



class user:
    
    def __init__(self, name, passw, plate) -> None:
        self.username = name
        self.password = passw
        self.balance = 0.0
        self.carPlate = plate


    def get_username (self):
        return self.username

    def set_username (self, name):
        self.username = name
    
    def set_password  (self, passw):
        self.password = passw

    def change_password (self, passw):
        self.password = passw

    def change_username (self, name):
        self.username = name

    def add_balance(self, ammount):
       self.balance += ammount
    
    def get_balance(self):
        return (self.balance)

    def set_carPlate (self, carPlateNum):
        self.carPlate = carPlateNum







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

    # Clear all currently existing data in employee table
    # player.delete_many({})

    # Creating attributes for userCredentials schema
    userCredentials.create_index([("username", pymongo.ASCENDING)], unique=True)
    userCredentials.create_index([("password", pymongo.ASCENDING)])
    userCredentials.create_index([("email", pymongo.ASCENDING)], unique = True)



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
                        print ("sign up successfully!")
                case 3:
                    print ("Good bye!")
                    leave_login = True
                    leave_parking_garage = True
                case 4:    
                    #used to populate some data. 
                    populate(db, userCredentials)
                
            
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
                        print("1: Reserve")
                        print("2: Add Balance")
                        print("3: See Balance")
                        print("4: log out")
                        print("5: exit program")
                        print("6: run tests (made by Derek)")

                    case 2: #Add Balance
                        print("adding balance")
                    case 3: #See Balance
                        print ("printing balance")
                    
                    case 4: #Log out
                        print ("--------------------------------------------")
                        print ("logging out...")
                        logged_in_username = ""
                        leave_login = False
                        leave_parking_garage = True

                    case 5: # exit program
                        print ("goodbye!")
                        leave_login = True
                        leave_parking_garage = True

                    case 6: #run tests
                        #creates a default parking lot
                        lotList = []
                        newLot = parkingLot("Lot A",5,20,5) #makes a parking lot that has 5 floors, 20 spaces per floor, 5 dollar cost per space
                        lotList.append(newLot)



                        user1 = user("Dat Pham","StrongPassw", "5SHC125")


                        #Tests
                        # test_lotCreation(lotList) 
                        # Passes lot creation test!

                        test_reservation(lotList)
                        #Passes single reservation test!

                        test_reservation_multiple(lotList)
                        #Passes multiple reservation test!

                        test_reservation_redundant(lotList)
                        #Passes redundancy test!

                        test_unreserveByName(lotList, "Derek Zhang")
                        #passes unreserve all test!

                        test_unreserveBySpace(lotList,"Sean Sidwell")
                        #passes specific unreserve test!
                
                if leave_parking_garage == True:
                    break
            if (leave_parking_garage == True) & (leave_login == True):
                break
def print_login_menu():
    print ("--------------------------------------------")
    print ("Welcome to the Automated parking garage. Please login or signup to use our program!")

    print("please select an option")
    print("1: sign in")
    print("2: sign up")
    print("3: exit")
    print("4: populate some default data to the database (used for testing)")


def print_parking_garage_menu(logged_in_username):
    print ("--------------------------------------------")
    print ("Hello", logged_in_username, "! Welcome to the Automated parking garage!")
    print("Please select an option")
    print("1: Reserve")
    print("2: Add Balance")
    print("3: See Balance")
    print("4: log out")
    print("5: exit program")
    print("6: run tests")

def test_divider():
    print("\n==================================================================")

def test_lotCreation(lotList):
    print("TEST: Lot creation:")
    for lot in lotList:
        print(lot)
        for floor in lot.returnLot():
            print(floor) #prints to console each floor in the lot with parkingSpace objects in a list format
            for space in floor:
                print(space.getCost())
    test_divider()

def test_reservation(lotList):
    print("TEST: Single Reservation")
    reserveSpace(lotList[0],"Derek Zhang")
    print(lotList[0].reservedSpace)
    lotList[0].getReserved()
    lotList[0].getInfo()
    test_divider()

def test_reservation_multiple(lotList):
    print("TEST: Multiple Reservations")
    reserveSpace(lotList[0], "Derek Zhang")
    reserveSpace(lotList[0], "Sean Sidwell")
    reserveSpace(lotList[0], "Johnnie Mares")
    print(lotList[0].reservedSpace)
    lotList[0].getReserved()
    lotList[0].getInfo()
    test_divider()

def test_reservation_redundant(lotList):
    print("TEST: Redundant Reservations")
    lotA = lotList[0]
    reserveSpace(lotA,"Derek Zhang")
    reserveSpace(lotA,"Derek Zhang")
    reserveSpace(lotA,"Derek Zhang")
    print(lotA.reservedSpace)
    lotA.getReserved()
    lotA.getInfo()
    test_divider()

def test_unreserveByName(lotList, name):
    print("TEST: Unreserve all by name")
    lotA = lotList[0]
    emptyAllSpace_Name(name, lotA)
    lotA.getReserved()
    lotA.getInfo()
    test_divider()

def test_unreserveBySpace(lotList, name):
    print("TEST: Unreserve by specific space")
    lotA=lotList[0]
    spaceA = lotA.reservedSpace[name][0]
    emptySpace_Obj(spaceA, lotA)
    lotA.getReserved()
    lotA.getInfo()
    test_divider()



def populate (db, userCredentials):

    # inserting default data for user
    userCredentials_result = userCredentials.insert_many([
        {"username": "user1", "password": "passw1", "email": "user.01@gmail.com"},
        {"username": "user2", "password": "passw2", "email": "user.02@gmail.com"},
        {"username": "user3", "password": "passw3", "email": "user.03@gmail.com"},

    ])
    print ("--------------------------------------------")
    print ("Populate successfully")
main()