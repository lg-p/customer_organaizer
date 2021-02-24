from abc import ABC, abstractmethod

from handbook.customer_service import CustomerService
from handbook.validator import Validator, ValidateException


class Command(ABC):

    @abstractmethod
    def execute(self, customer_service: CustomerService) -> None:
        pass


class ExitCommand(Command):

    def execute(self, customer_service):
        raise SystemExit


class HelpCommand(Command):

    def execute(self, customer_service):
        print(
            "The program is designed to store, view and edit customer data\n"
            "Commands:\n"
            "\t'insert' - insert a new customer\n"
            "\t\targuments: customer_id full_name position name_of_the_organization email phone\n"
            "\t'find' - searches for a customer\n"
            "\t\targuments: 'one of the customer arguments' 'argument value'\n"
            "\t'update' - update a customer\n"
            "\t\targuments: customer_id full_name position name_of_the_organization email phone\n"
            "\t'delete' - removes customer\n"
            "\t\targuments: customer_id\n"
            "\t'list' - displays a list of customers sorted by the listed arguments\n"
            "\t\targuments: 'any number of customer arguments separated by a space'\n"
        )


class InsertCommand(Command):
    def __init__(self):
        self.expected_arguments = [
            "customer_id",
            "full_name",
            "position",
            "name_of_the_organization",
            "email",
            "phone"
        ]

    def execute(self, customer_service):
        arguments = []
        try:
            for argument in self.expected_arguments:
                argument_value = input(f"{argument}:")
                if not Validator.validate_data(argument, argument_value):
                    raise ValidateException()
                arguments.append(argument_value)
        except ValidateException:
            return
        else:
            customer_service.create_customer(*arguments)


class FindCommand(Command):

    def __init__(self):
        self.expected_arguments = ["arguments name"]

    def execute(self, customer_service):
        arguments = []
        try:
            for argument in self.expected_arguments:
                argument_name = input(f"{argument}:")
                argument_value = input(f"argument value:")
                if not Validator.validate_data(argument_name, argument_value):
                    raise ValidateException()
                arguments.append(argument_name)
                arguments.append(argument_value)
        except ValidateException:
            return
        else:
            customer_service.display_customer_details(*arguments)


class UpdateCommand(Command):

    def __init__(self):
        self.expected_arguments = ["customer_id", "full_name", "position", "name_of_the_organization", "email", "phone"]

    def execute(self, customer_service):
        arguments = []
        try:
            for argument in self.expected_arguments:
                argument_value = input(f"{argument}:")
                if not Validator.validate_data(argument, argument_value):
                    raise ValidateException()
                arguments.append(argument_value)
        except ValidateException:
            return
        else:
            customer_service.update_customer(*arguments)


class DeleteCommand(Command):

    def __init__(self):
        self.expected_arguments = ["customer_id"]

    def execute(self, customer_service):
        arguments = []
        try:
            for argument in self.expected_arguments:
                argument_value = input(f"{argument}:")
                if not Validator.validate_data(argument, argument_value):
                    raise ValidateException()
                arguments.append(argument_value)
        except ValidateException:
            return
        else:
            customer_service.remove_customer(*arguments)


class ListCommand(Command):

    def __init__(self):
        self.expected_arguments = ["arguments name"]

    def execute(self, customer_service):
        arguments = []
        try:
            for argument in self.expected_arguments:
                arguments_valid = input(f"{argument}:").split()
                if arguments_valid is not None:
                    for argument_valid in arguments_valid:
                        arguments.append(argument_valid)
            if len(arguments) > 0:
                if not Validator.validate_data_for_list(arguments):
                    raise ValidateException()
        except ValidateException:
            return
        else:
            customer_service.display_customer_data(arguments)
