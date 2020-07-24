from schedule_pass import *

class Util:
    def mainMenu(self):
        menuOption = 0

        while(1 > menuOption or 4 < menuOption):
            print("\nMain Menu:\n")
            print("1 - Show All Passes")
            print("2 - Schedule Passes")
            print("3 - Cancel Passes")
            print("4 - Exit Program")

            menuOption = int(input("\nEnter menu option here: "))
            if(1 > menuOption or 4 < menuOption):
                print("\n***Option out of range***")

        return menuOption

def main():

    menu = Util()
    choice = menu.mainMenu()
    passes = Schedule_Pass()

    #while user chooses not to exit the program
    while(4 != choice):

        #if user chooses to view sample recording options
        if(1 == choice):
            passList = passes.show_list()
           
        #if user chooses to view Sample Library options
        if(2 == choice):
            scheduledPasses = passes.schedule_all()

        #if user chooses to view Sample Library options
        if(3 == choice):
            canceledPasses = passes.cancel_all()
            
        choice = menu.mainMenu()

#if __name__ == "__main__":
main()
