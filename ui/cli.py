#  to take user inputs and also print the cli elements

from services import manager

SUCCESS = "\033[92m"
ERROR= "\033[91m"
RESET= "\033[0m"

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


print(f"\n{'-'*40}STUDENT MANAGEMENT SYSTEM{'-'*40}")
while True:
    choice = main_menu()
    match choice:
        case "1":
            try:
                name = input("Enter name of the student: ").strip().lower()
                std = input("Enter class: ").strip()
                roll = input("Enter roll number: ").strip()
                marks = []
                marks_from_user = input("Enter marks: ").split()
                for item in marks_from_user:
                    marks.append(int(item))

                res = manager.add_student(name, std, roll, marks)
                if res == False:
                    print("Error: Student already exists.\n")
                else:
                    print(f"{SUCCESS}Success{RESET}: Student added.\n")
            except ValueError:
                print(f"{ERROR}Error{RESET}: Enter valid values.\n")

        case "2":
            students = manager.view_list()
            for student in students:
            # This prints each student on a clean new line
                print(f" Name: {student['name'].title()} | Std: {student['standard']} | Roll: {student['roll_number']} | Marks: {student["marks"]}")

        case "3":
            try:
                sub_choice = input("Choose:\n\ta. by roll number\n\tb. by name\n")
                if sub_choice == "a":
                    std = input("Enter class: ").strip()
                    roll = input("ENter roll").strip()
                    (
                        print(f"{manager.search_by_roll(std, roll)}\n")
                        if manager.search_by_roll(std, roll) != False
                        else print(f"{ERROR}Error{RESET}: Data not found.\n")
                    )
                if sub_choice == "b":
                    name = input("Enter name: ").strip().lower()
                    (
                        print(f"{manager.search_by_name(name)}\n")
                        if manager.search_by_name(name) != False
                        else print(f"{ERROR}Error{RESET}: Data not found.\n")
                    )
            except ValueError:
                print(f"{ERROR}Error{RESET}: Enter valid values.\n")

        case "4":
            try:
                std = input("Enter class: ").strip()
                roll = input("ENter roll").strip()
                res = manager.delete_student(std, roll)
                (
                    print(f"{SUCCESS}Success{RESET}: Data deleted.\n")
                    if res != False
                    else print(f"{ERROR}Error{RESET}: Data not found.\n")
                )
            except ValueError as e:
                print(f"{ERROR}Error{RESET}: Enter valid values.{e}\n")

        case "5":
            std = input("Enter class: ").strip()
            roll = input("Enter roll: ").strip()
            per = manager.per_marks(std, roll)
            (
                print(f"The percentage obtained by student are {per}\n")
                if per is not False
                else print(f"{ERROR}Error{RESET}: Data not found.\n")
            )

        case "6":
            print(f"\n{'-'*40}PROGRAM ENDS{'-'*40}")
            break
