# Simulated storage
# ==================================================================================================
students = {
    1: {
        'id': 1,
        'name': 'Ian Taylor',
        'marks': [4, 3, 5, 5, 4, 3, 4, 4, 2],
        'info': 'Maile, 20 y.o.'
    },
    2: {
        'id': 2,
        'name': 'Amy Smith',
        'marks': [5, 5, 4, 5, 5, 4, 3, 5, 5],
        'info': 'Female, 21 y.o.'
    }
}

last_setup_id = 2


def students_show():
    for id_, student in students.items():
        print(f'[{id_}] {student['name']}. Marks: {student['marks']}')


def student_details(student: dict) -> None:
    print("Student's info:")
    print(
        f'{student['name']}. Marks: {student['marks']}\n'
    )


def students_add(student: dict) -> dict | None:
    global last_setup_id

    if len(student) != 2:
        return None
    if not student.get('name') or not student.get('marks'):
        return None
    else:
        last_setup_id += 1
        students[last_setup_id] = student

    return student


def students_retrieve(id_: int) -> dict | None:
    return students.get(id_)


def students_remove(id_: int):
    if students_retrieve(id_):
        del students[id_]
        print(f"Student with id '{id_}' is removed from the list")
    else:
        print(f"There is no requested student with id '{id_}' in the list")


def students_add_mark(id_: int):
    additional_mark = input('Please type your mark to add: ')
    if id_ in students:
        students[id_]['marks'].append(int(additional_mark))
        print("Mark was successfully added!")
    else:
        print(f"There is no requested student with id '{id_}' in the list")


def students_update(id_: int, payload: dict) -> dict:
    students[id_] = payload
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
    students[id_] = part_payload
    return part_payload


def student_part_payload(id_: int) -> dict:

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

        if id_ in students and update_part.isalpha():
            new_name = ' '.join(items_part)
            return {'name': new_name, 'marks': students[id_]['marks']}
        elif id_ in students and update_part.isdigit():
            new_marks = list(update_part)
            return {'name': students[id_]['name'], 'marks': new_marks}
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
        update_id = input("Type student's id to update: ")
        id_ = int(update_id)
        if id_ not in students:
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
        mark_id = input("Type student's id to add mark: ")
        id_ = int(mark_id)
        if id_ not in students:
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
