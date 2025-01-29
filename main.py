# importing modules
from classes_n_functions import *

def main():

    print("Welcome to Graduation Tracker!")
    student_name = input("What is your name? \t")
    creds_to_graduate = get_credits("What are the total number of credits needed to graduate? Please enter a numerical value. \t")

    # creates a new instance of Transcript
    transcript = Transcript(creds_to_graduate, student_name)

    # run program as long as True or user chooses to exit
    while True:
        transcript.present_options()

if __name__ == "__main__":
    main()
