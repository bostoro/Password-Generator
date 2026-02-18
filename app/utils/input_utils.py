import getpass


def input_boolean(msg: str):
    valid_yes_responses = ["yes", "y", "true"]
    valid_no_responses = ["no", "n", "false"]
    while True:
        response = input(msg).lower()
        if response in valid_yes_responses:
            return True
        elif response in valid_no_responses:
            return False
        else:
            print("⚠️  Please, provide a valid yes/no answer!")


def input_string_notnull(msg: str):
    while True:
        response = input(msg)
        if response.strip():
            return response
        else:
            print("⚠️  Error: Answer may not be empty!")


def input_integer(msg: str, ignore_empty=False):
    while True:
        response = input(msg)
        if ignore_empty and not response.strip():
            return None
        try:
            return int(response)
        except ValueError:
            print("⚠️  Error: Answer must be an integer!")


def input_password(msg):
    while True:
        response = getpass.getpass(msg).strip()
        if response:
            return response
        else:
            print("⚠️  Error: Password must not be empty!")
