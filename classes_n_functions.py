# importing modules
import sys
import csv

# asks user for number of credits until correct input is entered
def get_credits(question):
    credits = input(question)
    if not credits.isnumeric():
        return get_credits(question)
    return int(credits)


class Course:
    # initiates with user supplied values
    def __init__(self, course_name, credits, status):
        self.course_name = course_name
        self.credits = credits
        self.status = status

    # creates iterable object
    def __iter__(self, course_name, credits, status):
        return iter(self.course_name, self.credits, self.status)


class Transcript:
    # initiates program with values
    def __init__(self, credits_to_graduate, student_name):
        self.courses = []
        self.credits_completed = 0
        self.credits_to_graduate = credits_to_graduate
        self.credits_remaining = 0
        self.student_name = student_name

    # add a new course
    def add_course(self):
        
        # input course information
        course_name = self.get_course_name()
        credits = get_credits("How many credits does this class fulfill? Please enter a numerical value. \t")
        status = self.get_status()

        # creates new instance of course using input
        new_course = Course(course_name, int(credits, status)
        self.courses.append(new_course)
        
        # if student completed class, add the credits to the total completed credits
        if status == "y":
            self.add_credits_completed(credits)
        print(new_course.course_name + " added.")

    # lists all entered courses
    def list_courses(self):
        num_of_courses = len(self.courses)
        if num_of_courses == 0:
            print("You have no courses added.")
        else:
            print("Courses added: ")
            print("Course ", " Credits ", "Status")
            for course in self.courses:
                print(course.course_name, "\t", course.credits, "\t", course.status)

    # deletes a course
    def delete_course(self, index, credits):
        if len(self.courses) > index >= 0:
            
            # removes credits completed
            completion_status = self.courses[index].status
            
            # only deleting credits added to transcript if completion status marked as yes
            if completion_status == "y":
                self.delete_credits_completed(credits)

            # deleting course after updating credits
            print("Deleting " + self.courses[index].course_name)
            del self.courses[index]
            
        else:
            print("Course name not found.")

    # updates existing course info
    def edit_course(self, index):

        # if course is found, update information and credits
        if len(self.courses) > index >= 0:

            # grabs information to update
            updated_credits = get_credits(
                "Enter the credits for this course. Please enter a numerical value. \t"
            )
            updated_course_name = self.get_course_name()
            updated_status = self.get_status()

            updated_course = Course(
                updated_course_name, updated_credits, updated_status
            )

            # updating credit discrepancies before deleting course entirely
            if updated_status == self.courses[index].status:
                if updated_status == "y":
                    if (
                        updated_credits > self.courses[index].credits
                    ):  # status remains same but updated credits are more
                        credits_to_increment = (
                            updated_credits - self.courses[index].credits
                        )
                        self.add_credits_completed(credits_to_increment)
                    else:  # both status remain the same but new credits are less
                        credits_to_decrement = (
                            self.courses[index].credits - updated_credits
                        )
                        self.delete_credits_completed(credits_to_decrement)
            else:
                if updated_status == "y":  # original class not completed
                    self.add_credits_completed(updated_credits)
                else:  # original class completed but not new class, removing credits completed
                    original_credits = self.courses[index].credits
                    self.delete_credits_completed(original_credits)

            # update with new instance of Course after updating credits
            self.courses[index] = updated_course
            print(self.courses[index].course_name + " updated")
            print(self.courses[index].status)

        else:
            print("Course name not found.")
            self.present_options()

    # saves courses to csv file. Note: courses are only written once the program exits
    def save_courses(self):
        try:
            with open("transcript.csv", "w", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=" ")
                
                # writes name and header
                writer.writerow(["Student Name:", self.student_name])
                writer.writerow(["Course", "Credits", "Completion"])
                
                # writes course information
                for course in self.courses:
                    writer.writerow([course.course_name, "\t", course.credits,"\t\t", course.status])
                credits_remaining = (
                    str(self.credits_remaining) + " remaining credits to graduate."
                )
                credits_completed = str(self.credits_completed) + " credits completed."
                writer.writerow([credits_completed, credits_remaining])
                print("Courses saved to csv file.")
        except Exception as e:
            print("Unable to write courses to csv with exception: ", e)
            sys.exit()

    # saves, exits, or returns to main menu
    def exit_program(self):
        print("Courses entered are not automatically saved when exiting the program.")
        leave_wo_saving = input("Do you wish to exit without saving? y or n: ")
        if leave_wo_saving == "y":
            print("Exiting program")
            sys.exit()
        elif leave_wo_saving == "n":
            save_or_main_menu = input(
                "Do you wish to save courses and exit or return to the main menu? Type \ns - save and exit \nm - return to main menu \t"
            )
            if save_or_main_menu == "s":
                print("Saving courses and exiting.")
                self.save_courses()
                sys.exit()
            elif save_or_main_menu == "m":
                self.present_options()

    # finds course to delete or edit by course name
    def find_course_index(self, course_name):
        num_of_courses = len(self.courses)
        for i in range(0, num_of_courses):
            if course_name == self.courses[i].course_name:
                return i

        # unable to find course
        return -1

    # adds credits for new class or updated class has more credits than original
    def add_credits_completed(self, credits):
        self.credits_completed += credits
        self.credits_remaining = self.credits_to_graduate - self.credits_completed

    # deletes credits if edited class no longer has status of completed
    def delete_credits_completed(self, credits):
        self.credits_completed -= credits
        self.credits_remaining = self.credits_to_graduate - self.credits_completed

    # displays total and remaining credits
    def display_credits(self):
        print(str(self.credits_to_graduate) + " credits to graduate.")
        print(str(self.credits_completed) + " credits completed so far.")
        print(str(self.credits_remaining) + " credits remaining")
    
    # gets the completion status of class
    def get_status(self):
        status = input("Did you complete this class? y or n: \t")
        if status == "y" or status == "n":
            return status
        return self.get_status()
    
    # gets course name 
    def get_course_name(self):
        course_name = input("Enter the course name. \t")
        if not course_name:
            return self.get_course_name()
        return course_name

    # presents main menu options
    def present_options(self):
        option = input("Please choose an option: add, list, delete, edit, save, exit. \n")

        if option == "add":
            
            # add course to course list
            self.add_course()

        elif option == "list":

            # list all courses entered
            self.list_courses()
            self.display_credits()

        elif option == "delete":

            # find index of course based on course name
            print("Please provide the information to delete a course. \n")
            course_name = self.get_course_name()
            delete_index = self.find_course_index(course_name)
            credits = self.courses[delete_index].credits
            
             # removes course based on index
            self.delete_course(delete_index, credits)

        elif option == "edit":

            # user input of course name needed to find the course index to edit
            print("Please provide the following information to edit the course. \n")
            course_name = input("Enter the course name you want to edit. \t")
            edit_index = self.find_course_index(course_name)

            # edits course based on index
            self.edit_course(edit_index)

        elif option == "save":
            # saves courses to csv file
            self.save_courses()

        elif option == "exit":
            # exits program
            self.exit_program()
