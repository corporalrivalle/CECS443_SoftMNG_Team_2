import numpy as nps
import pandas as pd

def reserve():
    print("choose 1 for onsite or 2 for online?\n")

    choice = int(input())

    match choice:
        case 1:
            print("you have chosen onsite, let me check if we are at capacity...\n")





def main ():


    lot = []
    end = 4
    print ("Welcome to the Automated parking garage.\n")

    print("please select an option\n")
    print("1: make a reservation\n")
    print("2: check what spots on what floor are available\n")
    my_input = int(input())

    match my_input:
        case 1:
            reserve()

        case 2:
            print("what floor?\n")


    

  


    




if __name__ == "__main__":
    main()