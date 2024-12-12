import csv
import json
from pathlib import Path

# Simulated storage
# ==================================================================================================
csv_file = Path("/Users/anastasiiaprokofieva/PycharmProjects/Python_PRO")
files_dir = Path("/Users/anastasiiaprokofieva/PycharmProjects/Python_PRO")
csv_storage = 'students.csv'
storage_file = 'students.json'


class StudentsRepository:

    def __init__(self) -> None:
        self.students = {}
        self.students.update(self.load_csv())

    @staticmethod
    def read_json(self) -> dict:
        with open(files_dir / storage_file) as file:
            return json.load(file)

    @staticmethod
    def write_json(data: dict) -> None:
        with open(files_dir / storage_file, mode='w') as file:
            json.dump(data, file)

    @staticmethod
    def load_csv() -> dict:
        students = {}
        with open(csv_file / csv_storage, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students[row['id']] = {
                    'name': row['name'],
                    'marks': list(map(int, row['marks'].split(',')))
                }
        return students


    @staticmethod
    def write_csv(data: dict) -> None:
        with open(csv_file / csv_storage, mode='w') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'marks'])
            writer.writeheader()
            for student_id, student_data in data.items():
                writer.writerow({
                    'id': student_id,
                    'name': student_data['name'],
                    'marks': ','.join(map(str, student_data['marks']))
                })

    def update_students(self) -> None:
        self.write_json(self.students)
        self.write_csv(self.students)


def students_show():

    for id_, student in StudentsRepository().students.items():
        print(f"[{id_}] {student['name']}. Marks: {student['marks']}")


def student_details(student: dict) -> None:
    print("Student's info:")
    print(
        f'{student['name']}. Marks: {student['marks']}\n'
    )


def students_add(student: dict) -> dict | None:
    storage = StudentsRepository()

    if len(student) != 2:
        return None
    if not student.get('name') or not student.get('marks'):
        return None

    if storage.students:
        current_id = list(map(int, storage.students.keys()))
        new_id = str(max(current_id) + 1)
    else:
        new_id = '1'

    storage.students[new_id] = student
    storage.update_students()
    return student


def students_retrieve(id_: int) -> dict | None:
    storage = StudentsRepository()
    return storage.students.get(str(id_))


def students_remove(id_: int):
    storage = StudentsRepository()
    if students_retrieve(id_):
        del storage.students[str(id_)]
        storage.update_students()
        print(f"Student with id '{id_}' is removed from the list")
    else:
        print(f"There is no requested student with id '{id_}' in the list")


def students_add_mark(id_: int):
    storage = StudentsRepository()
    additional_mark = input('Please type your mark to add: ')
    if id_ in storage.students:
        storage.students[str(id_)]['marks'].append(int(additional_mark))
        storage.update_students()
        print("Mark was successfully added!")
    else:
        print(f"There is no requested student with id '{id_}' in the list")


def students_update(id_: int, payload: dict) -> dict:
    storage = StudentsRepository()
    storage.students[str(id_)] = payload
    storage.update_students()
    return payload


def parse(data: str) -> tuple[str, list[int]]:
    """Return student's name and marks.

    user example:
    'John Doe;4,5,4,5,4,5'
    """
    example = 'John Doe;4,5,4,5,4,5'
    items = data.split(';')

    if len(items) != 2:
        raise Exception(f"Incorrect formating. Use the example: {example}")

    name, marks_group = items

    try:
        marks = [int(item) for item in marks_group.split(',')]
    except ValueError as error:
        print(error)
        raise Exception(f"Mars formating is incorrect. Please use the example: {example}")

    return name, marks


def students_partial_update(id_: int, part_payload: dict) -> dict:
    storage = StudentsRepository()
    storage.students[str(id_)] = part_payload
    storage.update_students()
    return part_payload


def student_part_payload(id_: int) -> dict:
    storage = StudentsRepository()
    prompt_part = input(
        "Type the part of student's payload you would like to change.\n"
        "(Example for the name update: John Doe\n"
        "Example for the marks update: 4,5,4,5,4,5)\n"
        "To make a full update type: FULL "
    )
    if prompt_part == 'FULL':
        return student_payload()
    else:
        items_part = prompt_part.split(',')
        items_part1 = ''.join(items_part)
        items_part = items_part1.split(' ')
        update_part = ''.join(items_part)

        if id_ in storage.students and update_part.isalpha():
            new_name = ' '.join(items_part)
            return {'name': new_name, 'marks': storage.students[id_]['marks']}
        elif id_ in storage.students and update_part.isdigit():
            new_marks = list(update_part)
            return {'name': storage.students[id_]['name'], 'marks': new_marks}
        else:
            raise Exception('Incorrect formating')


def student_payload():
    prompt = "Type student's payload using the example: 'John Doe;4,5,4,5,4,5'"

    if not (payload := parse(input(prompt))):
        return None
    else:
        name, marks = payload

    return {'name': name, 'marks': marks}


# Handle user input
# =================================================================================================
def handle_user_commands(command: str):
    if command == 'show':
        students_show()

    elif command == 'retrieve':
        search_id = input("Type student's id to retrieve: ")
        try:
            id_ = int(search_id)
        except ValueError as error:
            raise Exception(f"There is not student with id '{search_id}'") from error
        else:
            if student := students_retrieve(id_):
                student_details(student)
            else:
                print(f"There is not student with id '{search_id}'")

    elif command == 'remove':
        remove_id = input("Type student's id to remove: ")
        try:
            id_ = int(remove_id)
        except ValueError as error:
            raise Exception(f"There is not student with id '{remove_id}'") from error
        else:
            students_remove(id_)

    elif command == 'update':
        storage = StudentsRepository()
        update_id = input("Type student's id to update: ")
        id_ = str(update_id)
        if id_ not in storage.students:
            print(f"There is not student with id '{update_id}'")
        else:
            if data := student_part_payload(id_):
                students_partial_update(id_, data)
                print(f"Student details are successfully updated")
                if student := students_retrieve(id_):
                    student_details(student)
                else:
                    print(f"Can't update student details with data: '{data}")

    elif command == 'add student':
        data = student_payload()
        if data is None:
            return None
        else:
            if not (student := students_add(data)):
                print(f"Can't create student with data: {data}")
            else:
                print(f"New student '{student['name']}' is created")

    elif command == 'add mark':
        storage = StudentsRepository()
        mark_id = input("Type student's id to add mark: ")
        id_ = str(mark_id)
        if id_ not in storage.students:
            print(f"There is not student with id '{mark_id}'")
        else:
            students_add_mark(id_)
            if student := students_retrieve(id_):
                student_details(student)
            else:
                return None

    else:
        raise SystemExit(f"Unavailable '{command}'")


def handle_user_input():
    """This is an application entrypoint"""

    GENERAL_COMMANDS = ('quit', 'help')
    USER_COMMANDS = ('show', 'add student', 'retrieve', 'remove', 'update', 'add mark')
    AVAILABLE_COMMANDS = GENERAL_COMMANDS + USER_COMMANDS

    help_message = (
        "Welcome to the Journal! Choose your option to follow.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(help_message)

    while True:
        command = input("Type your command: ")

        if command == 'quit':
            print(f'\nSee you next time!')
            break
        elif command == 'help':
            print(help_message)
        elif command in USER_COMMANDS:
            handle_user_commands(command=command)
        else:
            print(f"Cannot recognise the command '{command}'")


handle_user_input()
