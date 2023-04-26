import numpy as nps
import pandas as pd
from  termcolor import colored
class permit:
    def __init__(self, floorNum, spotNum, licencePlate):
        self.fn = floorNum
        self.sn = spotNum
        self.lp = licencePlate

def reserve():
    print("choose 1 for onsite or 2 for online?\n")

    choice = int(input())

    match choice:
        case 1:
            print("you have chosen onsite, let me check if we are at capacity...\n")




def capacity(cap, lim):
    if cap >= lim:
        return 1
    else:
        return 0
    

def showGarage(mat,r,c):
    for i in range(r):
            for j in range(c):
                print(mat[i][j], end = " ")
            print("\n")


def reserveSpot(mat):
    print(" enter what floor you want. ex A3")
    a =[]
    a.append((input()))
    if(a[0]=='a'or a[0]=='a'):
            print("first row")
            f = 0
    elif(a[0]=='B' or a[0]=='b'):
            print("first row")
            f = 1
    elif(a[0]=='C' or a[0]=='c'):
            print("first row")
            f = 2
    print("enter number of the spot you want (1-6)")

    spot = int(input())

    mat[f][spot-1] = colored('|_____|', 'red')

    return mat


def main ():


    lot = [ [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0]]
    rows = 3
    cols = 6
    mat = [[0 for _ in range(cols)] for _ in range(rows)]
    cap=0
    limit = 16
    end = 4
    
   # while 1:
    onsite=False
    online = False
    leave = False
    floor = 0
    spot = 0
    lp = " "
  
    for i in mat:
        print('\t'.join(map(str, i)))

    for i in range(rows):
        for j in range(cols):
            mat[i][j] = colored('|_____|', 'blue')
        print()

    showGarage(mat,rows,cols)
    reserveSpot(mat)
    showGarage(mat,rows,cols)
    """
    while(1):
        for i in range(rows):
            for j in range(cols):
                print(mat[i][j], end = " ")
            print("\n")
        print(" enter what floor you want. ex A3")
        a =[]
        a.append((input()))
        if(a[0]=='a'or a[0]=='a'):
            print("first row")
            f = 0
        elif(a[0]=='B' or a[0]=='b'):
            print("first row")
            f = 1
        elif(a[0]=='C' or a[0]=='c'):
            print("first row")
            f = 2
        print("enter number of the spot you want (1-6)")

        spot = int(input())

        mat[f][spot-1] = colored('|_____|', 'red')
        
        
"""
"""
        print ("Welcome to the Automated parking garage.\n")

        print("please select an option\n")
        print("1: purchase onsite permit\n")
        print("2: make Online Reservation\n")
        print("3: cancel request\n")
        my_input = int(input())

        match my_input:
            case 1:
                onsite = True
                print("you have chosen to purchase an a parking permit onsite\n")
                print("let me check if we are at capacity...\n")
                if capacity(cap,limit) > 0:
                    print("there is not sufficent capcity in the structure to allow you to choose a spot, we will choose one for you\n")
                elif capacity(cap,limit) <= 0:
                    print("ok lets find you the perfect spot\n")
                    cap += 1
                else:
                    print("Sorry this lot if full, please try again later, goodbye :)\n")
        
            case 2:
                online = True
                print("you have chosen to make an online reservation\n")
                print("let me check if we are at capacity...\n")
                if capacity(cap,limit) > 0:
                    print("there is not sufficent capcity in the structure to allow you to choose a spot, we will choose one for you\n")
                elif capacity(cap,limit) <= 0:
                    print("ok lets find you the perfect spot\n")
                    cap += 1
                else:
                    print("Sorry this lot if full, please try again later, goodbye :)\n")

            case 3:
                print("you have chosen to cancel your request, goodbye :)")
                leave = True
                
        choice = int(input)
        if onsite == True:
            print("please choose one of the following options\n")
            print("choose a floor")

            match choice:

                case 1:

                    print("")
        elif online == True:
            print("online reservation is true\n")
        elif leave == True:
            online =False
            onsite = False
            break
    

  

    
"""



if __name__ == "__main__":
    main()