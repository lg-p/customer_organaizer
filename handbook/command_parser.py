from abc import ABC, abstractmethod
from collections import namedtuple

from handbook.customer_service import CustomerService
from handbook.validator import Validator


class Command(ABC):
    @abstractmethod
    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        pass

    @staticmethod
    def prompt_argument_input(name_arg: str, type_arg: str, validator, expected_arguments: list,
                              possibly_empty=False) -> str:
        """
        Prompts for an argument value according to the list of expected_arguments and validates the entered value.
        If the argument is not valid, the program asks for re-entry until a valid value or 'cancel' is entered.

        'cancel' raises CommandException.
        :return input value
        """
        while True:
            input_value = input(f"{name_arg}:").strip()

            if input_value == 'cancel':
                raise CommandException("Input canceled.")

            if possibly_empty and input_value == "":
                return input_value

            if type_arg == "value_argument":
                value_argument_valid = validator.validate_argument_value(name_arg, input_value)
            else:
                value_argument_valid = validator.validate_argument_name(input_value, expected_arguments)

            if value_argument_valid:
                break

        return input_value


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
        exit()


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
        Call 'prompt_argument_input' method for 'expected_arguments'
        :return argument list
        """
        arguments = []

        print("Enter a argument or 'cancel':")
        for name_argument in self.expected_arguments:
            value_argument = self.prompt_argument_input(name_argument, "value_argument",
                                                        validator, self.expected_arguments)
            arguments.append(value_argument)

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
        Call 'prompt_argument_input' method for argument name
        Call 'prompt_argument_input' method for argument value
        :return a tuple with the name and value of the argument
        """
        arguments = namedtuple("arguments", "name value")

        print("Enter a argument (customer_id, full_name, position, name_of_the_organization, email, phone) "
              "or 'cancel':")

        name_argument = self.prompt_argument_input("argument name", "name_argument",
                                                   validator, self.expected_arguments)
        arguments.name = name_argument

        value_argument = self.prompt_argument_input("argument value", "value_argument",
                                                    validator, self.expected_arguments)
        arguments.value = value_argument

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
        Call 'prompt_argument_input' method for 'customer_id'
        Call 'prompt_argument_input' method for argument name
        and call 'prompt_argument_input' method for argument value as long as the argument name is not empty.
        :return dict with arguments
        """
        updatable_arguments = dict()

        customer_id = self.prompt_argument_input("customer_id", "value_argument", validator, self.expected_arguments)
        updatable_arguments["customer_id"] = customer_id

        print("Enter an argument (customer_id, full_name, position, name_of_the_organization, email, phone) "
              "or 'cancel':")
        while True:
            name_argument = self.prompt_argument_input("argument name", "name_argument",
                                                       validator, self.expected_arguments, True)

            if name_argument == "":
                break

            value_argument = self.prompt_argument_input("argument value", "value_argument",
                                                        validator, self.expected_arguments)
            updatable_arguments[name_argument] = value_argument

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
        Call 'prompt_argument_input' method for customer_id
        :return: customer_id value
        """
        print("Enter an argument or 'cancel':")

        customer_id = self.prompt_argument_input("customer_id", "value_argument", validator, [])

        return customer_id

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
        Prompts for input for the name of the argument and checks if it is in the list of expected_arguments.

        If the argument or argument name is not valid, the program asks for re-entry
        until a valid value or 'cancel' is entered.

        'cancel' raises CommandException.
        :return: list argument
        """
        arguments = []

        print("Enter one or more arguments (customer_id, full_name, position, name_of_the_organization, email, phone), "
              "separated by a space or nothing, or enter 'cancel' to cancel:")
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
