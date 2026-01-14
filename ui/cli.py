#  to take user inputs and also print the cli elements

from services import manager

print(f"{"-"*80}program starts{"-"*80}")
while True:
    choice = input(
        "Choose:\n1. to add a student \n2. to view list \n3. to search a student\n4. to delete a student\n5. To find percentage\n6. to exit\n"
    )
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

                res=manager.add_student(name, std, roll, marks)
                if res == False:
                    print("student already exists.")            
            except ValueError:
                print("enter valid values.")
        case "2":
            print(manager.view_list())
        case "3":
            try:
                sub_choice = input("Choose:\n\ta. by roll number\n\tb. by name\n")
                if sub_choice == "a":
                    std = input("Enter class: ").strip()
                    roll = input("ENter roll").strip()
                    (
                        print(manager.search_by_roll(std, roll))
                        if manager.search_by_roll(std, roll) != False
                        else print("Data not found")
                    )
                if sub_choice == "b":
                    name = input("Enter name: ").strip().lower()
                    (
                        print(manager.search_by_name(name))
                        if manager.search_by_name(name) != False
                        else print("Data not found")
                    )
            except ValueError:
                print("enter valid values.")
        case "4":
            try:
                std = input("Enter class: ").strip()
                roll = input("ENter roll").strip()
                res = manager.delete_student(std, roll)
                print("Data deleted.") if res != False else print("Data not found.")
            except ValueError:
                print("Enter valid values.")
        case "5":
            std = input("Enter class: ").strip()
            roll = input("Enter roll: ").strip()
            per = manager.per_marks(std, roll)
            (
                print(f"The percentage obtained by student are {per}")
                if per != False
                else print("Data not found.")
            )

        case "6":
            print(f"{"-"*80}The program ends!!!{"-"*80}")
            break
