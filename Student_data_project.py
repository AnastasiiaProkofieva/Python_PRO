COMMANDS = ('quit', 'show', 'retrieve', 'add')

students = [
    {'id': 1, 'name': 'Ian Taylor', 'marks': [4, 3, 5, 5, 4, 3, 4, 4, 2], 'info': 'Maile, 20 y.o.'},
    {'id': 2, 'name': 'Amy Smith', 'marks': [5, 5, 4, 5, 5, 4, 3, 5, 5], 'info': 'Female, 21 y.o.'}
]


def find_student(id: int):
    for student in students:
        if student['id'] == int(id):
            return student
    return None


def show_students():
    print('*' * 20)
    print("The Students' List:")
    for student in students:
        print(f'{student['id']}: {student['name']}. Marks: {student['marks']}')

    print('*' * 20)


def show_student(id: int):
    student: dict | None = find_student(id)

    if not student:
        print("There is no student with id you've mentioned")
        return

    print("Student's info:")
    print(
        f'{student['id']}: {student['name']}. Marks: {student['marks']}\n'
        f'Details: {student['info']}'
    )


def add_student(student_name: str, student_details: str | None):
    student_id = int(students[-1]['id']) + 1
    instance = {'id': student_id, 'name': student_name, 'marks': [], 'info': student_details}
    students.append(instance)
    return instance


def main():
    print(f'Welcome to the Digital jornal!\nAvailable options: {COMMANDS}')
    while True:
        user_input = input('Type your option: ')

        if user_input not in COMMANDS:
            print(f'Option {user_input} is not available.\n')
            continue

        if user_input == 'quit':
            print('See you next time!')
            break

        try:
            if user_input == 'show':
                show_students()
            elif user_input == 'retrieve':
                student_id = input('Type student id: ')
                show_student(student_id)
            elif user_input == 'add':
                name = input("Enter the student's name: ")
                enquiry_details = input("Do you want to add student's details? (Y/N): ")
                if enquiry_details != 'Y' and enquiry_details != 'N':
                    print("Can't recognise the option. Student's details will not be saved.")
                    details = None
                elif enquiry_details == 'Y':
                    details = input("Enter the student's details here: ")
                else:
                    details = None
                add_student(name, details)
        except NotImplementedError as error:
            print(f"Feature '{error}' is not available.")
        except Exception as error:
            print(error)


main()
