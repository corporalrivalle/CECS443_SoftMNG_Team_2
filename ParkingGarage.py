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

def leavingLot(mat):
    print(" You are now leaving the parking structure")
    print("please enter your floor number")
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
    print("please enter the number of the spot you are leaving (1-6)")

    spot = int(input())

    mat[f][spot-1] = colored('|_____|', 'blue')

    return mat


def main ():



    rows = 3
    cols = 6
    mat = [[0 for _ in range(cols)] for _ in range(rows)]
   
  
  
    for i in mat:
        print('\t'.join(map(str, i)))

    for i in range(rows):
        for j in range(cols):
            mat[i][j] = colored('|_____|', 'blue')
        print()

    showGarage(mat,rows,cols)
    reserveSpot(mat)
    showGarage(mat,rows,cols)
    leavingLot(mat)
    showGarage(mat,rows,cols)
    


if __name__ == "__main__":
    main()