from abc import ABC, abstractmethod
from collections import namedtuple

from handbook.customer_service import CustomerService
from handbook.validator import Validator


class Command(ABC):
    @abstractmethod
    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        pass


class CommandException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


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
            "\targuments:\n"
            "\t\tcustomer_id\n"
            "\t\tfull_name\n"
            "\t\tposition\n"
            "\t\tname_of_the_organization\n"
            "\t\temail\n"
            "\t\tphone\n"
            "\t'find' - searches for a customer\n"
            "\targuments:\n"
            "\t\t'one of the customer arguments'\n"
            "\t\t'argument value'\n"
            "\t'update' - update a customer\n"
            "\targuments:\n"
            "\t\tcustomer_id\n"
            "\t\t'one of the customer arguments'\n"
            "\t\t'argument value'\n"
            "\t'delete' - removes customer\n"
            "\targuments:\n"
            "\t\tcustomer_id\n"
            "\t'list' - displays a list of customers sorted by the listed arguments\n"
            "\targuments:\n"
            "\t\t'any number of customer arguments separated by a space'\n"
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

    def get_arguments(self, validator) -> list:
        """
        Prompts for a parameter value according to the list of expected_arguments and validates the entered value.
        If the parameter is not valid, the program asks for re-entry until a valid value or 'cancel' is entered.

        'cancel' raises CommandException.
        :return argument list
        """
        arguments = []

        print("Enter a parameter or 'cancel':")
        for name_argument in self.expected_arguments:
            while True:
                value_argument = input(f"{name_argument}:")
                value_argument.replace(" ", "")

                if value_argument == 'cancel':
                    raise CommandException("Input canceled.")

                value_argument_valid = validator.validate_argument_value(name_argument, value_argument)
                if value_argument_valid:
                    arguments.append(value_argument)
                    break

        return arguments

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Calls 'get_arguments' to request input and validate arguments
        Calls the 'create_customer' command to create a new customer.
        """
        arguments = self.get_arguments(validator)

        customer_service.create_customer(*arguments)
        print("Success!")


class FindCommand(Command):
    def __init__(self) -> None:
        self.expected_arguments = ["customer_id", "full_name", "position", "name_of_the_organization", "email",
                                   "phone"]

    def get_arguments(self, validator) -> namedtuple:
        """
        Prompts for input for the name of the parameter and checks if it is in the list of expected_arguments.
        Then you are prompted to enter a value for the parameter.

        If the parameter or parameter name is not valid, the program asks for re-entry
        until a valid value or 'cancel' is entered.

        'cancel' raises CommandException.
        :return a tuple with the name and value of the argument
        """
        arguments = namedtuple("arguments", "name value")

        print("Enter a parameter or 'cancel':")

        while True:
            name_argument = input("argument name:")
            name_argument.replace(" ", "")

            if name_argument == 'cancel':
                raise CommandException("Input canceled.")

            name_argument_valid = validator.validate_argument_name(name_argument, self.expected_arguments)
            if name_argument_valid:
                arguments.name = name_argument
                break

        while True:
            value_argument = input("argument value:")
            value_argument.replace(" ", "")

            if value_argument == 'cancel':
                raise CommandException("Input canceled.")

            value_argument_valid = validator.validate_argument_value(name_argument, value_argument)
            if value_argument_valid:
                arguments.value = value_argument
                break

        return arguments

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Calls 'get_arguments' to request input and validate arguments
        Calls the 'find_customer' command to find a customer and displays the result of the command.
        """
        arguments = self.get_arguments(validator)

        customer = customer_service.find_customer(arguments.name, arguments.value)
        if customer is None:
            print("No data")
        else:
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

    def get_arguments(self, validator) -> dict:
        """
        Prompts for "customer_id" input and validates the entered value.

        Prompts for the name of the parameter to update and checks if it is in the list of expected_arguments.
        Then you are prompted to enter a value for the parameter.
        If an empty parameter name is entered, the loop breaks.

        If the parameter or parameter name is not valid, the program asks for re-entry
        until a valid value or 'cancel' is entered.

        'cancel' raises CommandException.
        :return dict with arguments
        """
        updatable_arguments = dict()

        print("Enter a parameter or 'cancel':")
        while True:
            value_argument = input("customer_id:")
            value_argument.replace(" ", "")

            if value_argument == 'cancel':
                raise CommandException("Input canceled.")

            value_argument_valid = validator.validate_argument_value("customer_id", value_argument)
            if value_argument_valid:
                updatable_arguments["customer_id"] = value_argument
                break

        print("Enter argument name and argument value or '' to stop entering arguments:")
        while True:
            while True:
                name_argument = input("argument name:")
                name_argument.replace(" ", "")

                if name_argument == 'cancel':
                    raise CommandException("Input canceled.")

                if name_argument == "":
                    break

                name_argument_valid = validator.validate_argument_name(name_argument, self.expected_arguments)
                if name_argument_valid:
                    break

            if name_argument == "":
                break

            while True:
                value_argument = input("argument value:")
                value_argument.replace(" ", "")

                if value_argument == 'cancel':
                    raise CommandException("Input canceled.")

                value_argument_valid = validator.validate_argument_value(name_argument, value_argument)
                if value_argument_valid:
                    updatable_arguments[name_argument] = value_argument
                    break

        return updatable_arguments

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Calls 'get_arguments' to request input and validate arguments
        Calls the 'update_customer' command to update the customer.
        """
        updatable_arguments = self.get_arguments(validator)

        customer_service.update_customer(updatable_arguments)
        print("Success!")


class DeleteCommand(Command):
    def get_arguments(self, validator) -> str:
        """
        Prompts for input parameter and checks if it is in the list of expected_arguments.

        If the parameter is not valid, the program asks for re-entry until a valid value or 'cancel' is entered.

        'cancel' raises CommandException.
        :return: customer_id value
        """
        print("Enter argument value or 'cancel':")
        while True:
            value_argument = input("customer_id:")
            value_argument.replace(" ", "")

            if value_argument == 'cancel':
                raise CommandException("Input canceled.")

            value_argument_valid = validator.validate_argument_value("customer_id", value_argument)
            if value_argument_valid:
                break

        return value_argument

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Calls 'get_arguments' to request input and validate arguments
        Calls the 'remove_customer' command to remove a customer.
        """
        value_argument = self.get_arguments(validator)

        customer_service.remove_customer(value_argument)
        print("Success!")


class ListCommand(Command):
    def get_arguments(self, validator) -> list:
        """
        Prompts for input for the name of the parameter and checks if it is in the list of expected_arguments.

        If the parameter or parameter name is not valid, the program asks for re-entry
        until a valid value or 'cancel' is entered.

        'cancel' raises CommandException.
        :return: list argument
        """
        arguments = []

        print("Enter one or more arguments, separated by a space or nothing, "
              "or enter 'cancel' to cancel:")
        while True:
            input_arguments = input("sorted by:").split()

            if 'cancel' in arguments:
                raise CommandException("Input canceled.")

            if input_arguments is None:
                break
            else:
                arguments_valid = validator.validate_data_for_list(input_arguments)
                if arguments_valid:
                    arguments = input_arguments
                    break

        return arguments

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Calls 'get_arguments' to request input and validate arguments
        Calls the 'get_list_of_customers' command to get a list of customers and displays the result of the command.
        """
        arguments = self.get_arguments(validator)

        customer_data = customer_service.get_list_of_customers(arguments)
        if len(customer_data) == 0:
            print("No data")
        else:
            print(*customer_data, sep='\n')
