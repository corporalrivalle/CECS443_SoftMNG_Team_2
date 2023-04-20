#imports



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
    def __init__(self, floors, spacePerFloor, costPerSpace) -> None:
        self.floors = floors
        self.spacePerFloor = spacePerFloor
        self.capacity = floors*spacePerFloor
        self.originalCap = floors*spacePerFloor
        self.reservedSpace = {}
        self.lot = [] #stores parking Space objects on each floor until the floors are properly made

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
        

def reserveSpace(lot, reservedName): #pass in a parking lot object to reserve a space in
    for floor in lot:
        for space in floor:
            if space.occupied==False:
                space.changeOccupied(reservedName)
                lot.reservedSpaces[reservedName]=space #stores the reserved space in the lot under a dictionary with name as key and object as space
                break
            else:
                pass


#main function
def main():
    #creates a default parking lot
    lotList = []
    newLot = parkingLot(5,20,5) #makes a parking lot that has 5 floors, 20 spaces per floor, 5 dollar cost per space
    lotList.append(newLot)

    print(newLot.floors)
    #first test
    # test_lotCreation(lotList) 
    # Lot creation works!

def test_lotCreation(lotList):
    for lot in lotList:
        print(lot)
        for floor in lot.returnLot():
            print(floor) #prints to console each floor in the lot with parkingSpace objects in a list format
            for space in floor:
                print(space.getCost())


main()