from abc import ABC, abstractmethod

from handbook.customer_service import CustomerService
from handbook.validator import Validator, ValidateException


class Command(ABC):
    @abstractmethod
    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        pass


class ExitCommand(Command):
    def execute(self, customer_service: CustomerService, validator=Validator) -> SystemExit:
        """
         Closes the program
        """
        raise SystemExit


class HelpCommand(Command):
    def execute(self, customer_service: CustomerService, validator=Validator) -> print:
        """
        Calls help for working with the program
        """
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
    def __init__(self) -> None:
        self.expected_arguments = [
            "customer_id",
            "full_name",
            "position",
            "name_of_the_organization",
            "email",
            "phone"
        ]

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for a parameter value according to the list of expected_arguments and validates the entered value.
        Raises ValidateException exception if the parameter fails validation.
        Calls the 'create_customer' command to create a new customer.
        """
        arguments = []
        for argument in self.expected_arguments:
            argument_value = input(f"{argument}:")
            validation_result = validator.validate_data(argument, argument_value)
            if not validation_result.isSuccess:
                raise ValidateException(*validation_result.errors)
            arguments.append(argument_value)
        customer_service.create_customer(*arguments)


class FindCommand(Command):
    def __init__(self) -> None:
        self.expected_arguments = ["arguments name"]

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for a parameter value according to the list of expected_arguments and validates the entered value.
        Raises ValidateException exception if the parameter fails validation.
        Calls the 'find_customer' command to find a customer and displays the result of the command.
        """
        arguments = []
        for argument in self.expected_arguments:
            argument_name = input(f"{argument}:")
            argument_value = input(f"argument value:")
            validation_result = validator.validate_data(argument, argument_value)
            if not validation_result.isSuccess:
                raise ValidateException(*validation_result.errors)
            arguments.append(argument_name)
            arguments.append(argument_value)
        customer = customer_service.find_customer(*arguments)
        print(customer)


class UpdateCommand(Command):
    def __init__(self) -> None:
        self.expected_arguments = [
            "customer_id",
            "full_name",
            "position",
            "name_of_the_organization",
            "email",
            "phone"
        ]

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for a parameter value according to the list of expected_arguments and validates the entered value.
        Raises ValidateException exception if the parameter fails validation.
        Calls the 'update_customer' command to update the customer.
        """
        arguments = []
        for argument in self.expected_arguments:
            argument_value = input(f"{argument}:")
            validation_result = validator.validate_data(argument, argument_value)
            if not validation_result.isSuccess:
                raise ValidateException(*validation_result.errors)
            arguments.append(argument_value)
        customer_service.update_customer(*arguments)


class DeleteCommand(Command):
    def __init__(self) -> None:
        self.expected_arguments = ["customer_id"]

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for a parameter value according to the list of expected_arguments and validates the entered value.
        Raises ValidateException exception if the parameter fails validation.
        Calls the 'remove_customer' command to remove a customer.
        """
        arguments = []
        for argument in self.expected_arguments:
            argument_value = input(f"{argument}:")
            validation_result = validator.validate_data(argument, argument_value)
            if not validation_result.isSuccess:
                raise ValidateException(*validation_result.errors)
            arguments.append(argument_value)
        customer_service.remove_customer(*arguments)


class ListCommand(Command):
    def __init__(self):
        self.expected_arguments = ["arguments name"]

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for a parameter value according to the list of expected_arguments and validates the entered value.
        Raises ValidateException exception if the parameter fails validation.
        Calls the 'get_list_of_customers' command to get a list of customers and displays the result of the command.
        """
        arguments = []
        for argument in self.expected_arguments:
            arguments_valid = input(f"{argument}:").split()
            if arguments_valid is not None:
                for argument_valid in arguments_valid:
                    arguments.append(argument_valid)
        if len(arguments) > 0:
            validation_result = validator.validate_data_for_list(arguments)
            if not validation_result.isSuccess:
                raise ValidateException(*validation_result.errors)
        customer_data = customer_service.get_list_of_customers(arguments)
        print(*customer_data, sep='\n')
