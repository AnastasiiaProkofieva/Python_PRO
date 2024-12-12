users = [
            {'username': 'oleg', 'password': 'oleg34oleg'},
            {'username': 'cat', 'password': 'cat_894'},
            {'username': 'domino', 'password': 'follow'}
        ]


def auth(func):
    authorized_user = {'username': None, 'password': None}

    def wrapper(*args, **kwargs):
        if authorized_user['username']:
            return func(*args, **kwargs)

        while True:
            print("Authorization is required")
            username = input("Enter username: ")
            password = input("Enter password: ")
            for user in users:
                if user['username'] == username and user['password'] == password:
                    authorized_user['username'] = username
                    authorized_user['password'] = password
                    print("Authorization successful!")
                    return func(*args, **kwargs)

            print("Please check your details and try again.")

    return wrapper


@auth
def command():
    print("Executing command...")


command()
command()
