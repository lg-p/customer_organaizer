import re


class ValidateException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class ValidationResult:
    def __init__(self):
        self.isSuccess = True
        self.errors = []


class Validator:
    @classmethod
    def validate_argument_name(cls, name_argument: str, expected_arguments) -> bool:
        """
        Validates the name of an argument in the list of expected arguments
        displays an error message
        """
        argument_valid = True

        if name_argument not in expected_arguments:
            argument_valid = False

        if not argument_valid:
            print(f"ERROR: Argument '{name_argument}' does not exist.")

        return argument_valid

    @classmethod
    def validate_argument_value(cls, name_argument: str, value_argument: str) -> bool:
        """
        Validates the value of an argument
        displays an error message
        """
        validation_result = cls.validate_data(name_argument, value_argument)
        if not validation_result.isSuccess:
            print(*validation_result.errors)

        return validation_result.isSuccess

    @classmethod
    def validate_data(cls, name: str, value: str) -> ValidationResult:
        """
        Validates the argument value
        and stores the validation result and error message in an instance of the 'ValidationResult'
        :return ValidationResult
        """
        result = ValidationResult()
        if name == "customer_id":
            if not cls.validate_number(value):
                result.isSuccess = False
                result.errors.append(f"{name} must be 9 digits long")
        elif name == "full_name" or name == "position":
            if not cls.validate_string(value):
                result.isSuccess = False
                result.errors.append(f"{name} must be up to 120 letters long")
        elif name == "name_of_the_organization":
            if not cls.validate_limited_length_string(value):
                result.isSuccess = False
                result.errors.append(f"{name} must be up to 120 characters long")
        elif name == "email":
            if not cls.validate_email(value):
                result.isSuccess = False
                result.errors.append("Invalid email template")
        elif name == "phone":
            if not cls.validate_phone(value):
                result.isSuccess = False
                result.errors.append(f"{name} must be no more than 11 digits")
        return result

    @staticmethod
    def validate_data_for_list(arguments: list) -> bool:
        """
        Validates a list of arguments
        and stores the validation result and error message in an instance of the 'ValidationResult'
        displays an error message
        """
        result = ValidationResult()
        available_arguments = ["customer_id", "full_name", "position", "name_of_the_organization", "email", "phone"]

        for argument in arguments:
            if argument not in available_arguments:
                result.isSuccess = False
                result.errors.append(f"'list' command has no argument: {argument}")

        if not result.isSuccess:
            print(*result.errors)

        return result.isSuccess

    @staticmethod
    def validate_string(value: str) -> bool:
        if re.fullmatch(r"^[a-zA-Zа-яА-я ]{1,120}$", value):
            return True
        return False

    @staticmethod
    def validate_limited_length_string(value: str) -> bool:
        if re.fullmatch(r"^[0-9a-zA-Zа-яА-я\S ]{1,120}$", value):
            return True
        return False

    @staticmethod
    def validate_number(value: str) -> bool:
        if re.match(r"^[0-9]{1,9}$", value):
            return True
        return False

    @staticmethod
    def validate_email(value: str) -> bool:
        if re.match(r"[\w'.+-]+@[\w'.+-]+", value):
            return True
        return False

    @staticmethod
    def validate_phone(value: str) -> bool:
        if re.match(r"^[0-9]{11}$", value):
            return True
        return False
