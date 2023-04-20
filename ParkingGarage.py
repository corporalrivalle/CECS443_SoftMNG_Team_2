import numpy as nps
import pandas as pd

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


def main ():


    lot = [ [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0]]
    cap=0
    limit = 16
    end = 4
    
    while 1:
        onsite=False
        online = False
        leave = False
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
                
        
        if onsite == True:
            print("onsite is true\n")
        elif online == True:
            print("online reservation is true\n")
        elif leave == True:
            online =False
            onsite = False
            break
    

  


    




if __name__ == "__main__":
    main()