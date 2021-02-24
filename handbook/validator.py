import re


class ValidateException(Exception):
    pass


class Validator:
    @classmethod
    def validate_data(cls, name, value):
        if name == "customer_id":
            if not cls.validate_number(value):
                print(f"{name} must be 9 digits long")
                return False
        elif name == "full_name" or name == "position":
            if not cls.validate_string(value):
                print(f"{name} must be up to 120 letters long")
                return False
        elif name == "name_of_the_organization":
            if not cls.validate_limited_length_string(value):
                print(f"{name} must be up to 120 characters long")
                return False
        elif name == "email":
            if not cls.validate_email(value):
                print("Invalid email template")
                return False
        elif name == "phone":
            if not cls.validate_phone(value):
                print(f"{name} must be no more than 11 digits")
                return False
        return True

    @staticmethod
    def validate_data_for_list(arguments):
        available_arguments = ["customer_id", "full_name", "position", "name_of_the_organization", "email", "phone"]
        for argument in arguments:
            if argument not in available_arguments:
                print(f"'list' command has no argument: {argument}")
                return False
        return True

    @staticmethod
    def validate_string(value):
        if re.fullmatch(r"^[a-zA-Zа-яА-я ]{1,120}$", value):
            return True
        return False

    @staticmethod
    def validate_limited_length_string(value):
        if re.fullmatch(r"^[0-9a-zA-Zа-яА-я\S ]{1,120}$", value):
            return True
        return False

    @staticmethod
    def validate_number(value):
        if re.match(r"^[0-9]{9}$", value):
            return True
        return False

    @staticmethod
    def validate_email(value):
        if re.match(r"[\w'.+-]+@[\w'.+-]+", value):
            return True
        return False

    @staticmethod
    def validate_phone(value):
        if re.match(r"^[0-9]{11}$", value):
            return True
        return False
