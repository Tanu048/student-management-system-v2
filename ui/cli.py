#  to take user inputs and also print the cli elements

from validators import check_inputs, check_choice
from services.manager import StudentManager
from student_logging.student_log import LogInfo


class StudentCli:

    RED = "\033[31m"
    GREEN = "\033[32m"
    RESET = "\033[0m"

    def __init__(self, manager):
        self.manager = manager

    @staticmethod
    def main_menu():
        """
        generates an interractive menu
        """
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Calculate Percentage")
        print("6. Exit")
        return input("Select an option (1-6): ").strip()

    @staticmethod
    def display_header():
        print(f"\n{'-'*40}STUDENT MANAGEMENT SYSTEM{'-'*40}")
        LogInfo.log_info("Program accessed")

    @staticmethod
    def end_note():
        print(f"\n{'-'*40}PROGRAM ENDS{'-'*40}")
        LogInfo.log_info("program ended\n")

    def get_input(self, prompt: str):
        return input(prompt).strip()

    def handle_add(self):
        name = self.get_input("Enter name: ").lower()
        std = self.get_input("Enter standard: ").lower()
        roll = self.get_input("Enter roll number: ").lower()
        marks = []
        raw_marks = self.get_input("Enter marks: ")
        for item in raw_marks.split():
            marks.append(int(item))
        if check_inputs(name=name, std=std, roll=roll, marks=marks):
            if self.manager.add_student(name, std, roll, marks):
                print(f"{self.GREEN}Success{self.RESET}:Student added successfully!")
            else:
                LogInfo.log_error("Duplication detected")
                print(f"{self.RED}Error{self.RESET}:Student already exists!")

                
    def handle_view(self):
        students = self.manager.view_list()
        if not students:
            LogInfo.log_error("Empty list viewing")
            print(
                f"{StudentCli.RED}Error{StudentCli.RESET}: FIle is either corrupted, empty or non existing."
            )
        for student_key in students:
            print(
                f"Name: {students[student_key]["name"]} | Standard: {students[student_key]["standard"]} | Roll Number: {students[student_key]["roll_number"]} | Marks: {students[student_key]["marks"]} | Percentage: {students[student_key]["percentage"]}"
            )

    def handle_search(self):
        sub_choice = self.get_input("Choose:\n\ta. by roll number\n\tb. by name\n")
        if check_choice(sub_choice):
            if sub_choice == "a":
                self.search_by_roll()
            if sub_choice == "b":
                self.search_by_name()

    def handle_deletion(self):
        std = self.get_input("Enter standard: ")
        roll = self.get_input("Enter roll number: ")
        result = self.manager.delete_student(std, roll)
        if check_inputs(std=std, roll=roll):
            if result:
                print(f"{self.GREEN}Success{self.RESET}: Data deleted.\n")
            else:
                LogInfo.log_error("Deletion failed")
                print(f"{self.RED}Error{self.RESET}: Data not found.\n")

    def handle_per(self):
        std = self.get_input("Enter standard: ")
        roll = self.get_input("Enter roll number: ")
        result = self.manager.per_calc(std, roll)
        if check_inputs(std=std,roll=roll):
            if result:
                print(f"The percentage obtained by student are {result}\n")
            else:
                LogInfo.log_error("percentage access failed")
                print(f"{self.RED}Error{self.RESET}: Data not found.\n")

    def search_by_roll(self):
        std = self.get_input("Enter standard: ")
        roll = self.get_input("Enter roll number: ")
        result = self.manager.search_by_roll(std, roll)
        if check_inputs(std=std,roll=roll):
            if result:
                print(f"{result}\n")
            else:
                LogInfo.log_error("search intruppted")
                print(f"{self.RED}Error{self.RESET}: Data not found.\n")

    def search_by_name(self):
        name = self.get_input("Enter name: ")
        result = self.manager.search_by_name(name)
        if check_inputs(name=name):
            if result:
              for student_key in result:
                print(
                f"Name: {result[student_key]["name"]} | Standard: {result[student_key]["standard"]} | Roll Number: {result[student_key]["roll_number"]} | Marks: {result[student_key]["marks"]} | Percentage: {result[student_key]["percentage"]}"
            )
            else:                
                LogInfo.log_error("search intruppted")
                print(f"{self.RED}Error{self.RESET}: Data not found.\n")

    def run(self):
        self.display_header()
        while True:
            choice = StudentCli.main_menu()
            if check_choice(choice):
                match choice:
                    case "1":
                        self.handle_add()

                    case "2":
                        self.handle_view()

                    case "3":
                        self.handle_search()

                    case "4":
                        self.handle_deletion()

                    case "5":
                        self.handle_per()

                    case "6":
                        self.end_note()
                        break


s1 = StudentCli(StudentManager())
s1.run()