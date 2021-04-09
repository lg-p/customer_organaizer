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

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for a parameter value according to the list of expected_arguments and validates the entered value.

        If the parameter is not valid, the program asks for re-entry until a valid value or 'cancel' is entered.
        'cancel' raises ValidateException.

        Calls the 'create_customer' command to create a new customer.
        """
        arguments = []

        for argument in self.expected_arguments:
            argument_value = ""
            argument_valid = False

            while not argument_valid:
                argument_value = input(f"{argument}:").replace(" ", "")

                if argument_value == "cancel":
                    raise ValidateException("Input canceled.")

                validation_result = validator.validate_data(argument, argument_value)
                argument_valid = validation_result.isSuccess
                if not argument_valid:
                    print(*validation_result.errors,
                          "Enter again argument name or enter 'cancel' to cancel:",
                          sep="\n")

            arguments.append(argument_value)

        customer_service.create_customer(*arguments)
        print("Success!")


class FindCommand(Command):
    def __init__(self) -> None:
        self.expected_arguments = ["customer_id", "full_name", "position", "name_of_the_organization", "email",
                                   "phone"]

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for input for the name of the parameter and checks if it is in the list of expected_arguments.
        Then you are prompted to enter a value for the parameter.

        If the parameter or parameter name is not valid, the program asks for re-entry
        until a valid value or 'cancel' is entered.
        'cancel' raises ValidateException.

        Calls the 'find_customer' command to find a customer and displays the result of the command.
        """
        argument_name = ""
        argument_value = ""
        valid_argument = False
        valid_value = False

        while not valid_argument:
            argument_name = input("argument name:").replace(" ", "")

            if argument_name == 'cancel':
                raise ValidateException("Input canceled.")

            if argument_name in self.expected_arguments:
                valid_argument = True
            else:
                print(f"ERROR: Argument '{argument_name}' does not exist.",
                      "Enter again argument name or enter 'cancel' to cancel:",
                      sep="\n")

        while not valid_value:
            argument_value = input("argument value:").replace(" ", "")

            if argument_value == "cancel":
                raise ValidateException("Input canceled.")

            validation_result = validator.validate_data(argument_name, argument_value)
            if validation_result.isSuccess:
                valid_value = True
            else:
                print(*validation_result.errors,
                      "Enter again argument name or enter 'cancel' to cancel:",
                      sep="\n")

        customer = customer_service.find_customer(argument_name, argument_value)

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

    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for "customer_id" input and validates the entered value.

        Prompts for the name of the parameter to update and checks if it is in the list of expected_arguments.
        Then you are prompted to enter a value for the parameter.
        If an empty parameter name is entered, the loop breaks.

        If the parameter or parameter name is not valid, the program asks for re-entry
        until a valid value or 'cancel' is entered.
        'cancel' raises ValidateException.

        Calls the 'update_customer' command to update the customer.
        """
        updatable_arguments = dict()

        valid_value = False
        while not valid_value:
            argument_value = input("customer_id:").replace(" ", "")

            if argument_value == "cancel":
                raise ValidateException("Input canceled.")

            validation_result = validator.validate_data("customer_id", argument_value)
            if validation_result.isSuccess:
                valid_value = True
                updatable_arguments["customer_id"] = argument_value
            else:
                print(*validation_result.errors,
                      "Enter again argument name or enter 'cancel' to cancel:",
                      sep="\n")

        argument_name = "customer_id"
        while argument_name != '':
            valid_argument = False
            valid_value = False

            while not valid_argument:
                argument_name = input("argument name:").replace(" ", "")

                if argument_name == 'cancel':
                    raise ValidateException("Input canceled.")
                elif argument_name == '':
                    break

                if argument_name in self.expected_arguments:
                    valid_argument = True
                else:
                    print(f"ERROR: Argument '{argument_name}' does not exist.",
                          "Enter again argument name or enter 'cancel' to cancel:",
                          sep="\n")

            while not valid_value:
                if argument_name == '':
                    break

                argument_value = input("argument value:").replace(" ", "")

                if argument_value == "cancel":
                    raise ValidateException("Input canceled.")

                validation_result = validator.validate_data(argument_name, argument_value)
                if validation_result.isSuccess:
                    valid_value = True
                    updatable_arguments[argument_name] = argument_value
                else:
                    print(*validation_result.errors,
                          "Enter again argument name or enter 'cancel' to cancel:",
                          sep="\n")
        # ---
        customer_service.update_customer(updatable_arguments)
        print("Success!")


class DeleteCommand(Command):
    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for input parameter and checks if it is in the list of expected_arguments.

        If the parameter is not valid, the program asks for re-entry until a valid value or 'cancel' is entered.
        'cancel' raises ValidateException.

        Calls the 'remove_customer' command to remove a customer.
        """
        argument_value = ""
        valid_value = False

        while not valid_value:
            argument_value = input("customer_id:").replace(" ", "")

            if argument_value == "cancel":
                raise ValidateException("Input canceled.")

            validation_result = validator.validate_data("customer_id", argument_value)
            if validation_result.isSuccess:
                valid_value = True
            else:
                print(*validation_result.errors,
                      "Enter again argument name or enter 'cancel' to cancel:",
                      sep="\n")

        customer_service.remove_customer(argument_value)
        print("Success!")


class ListCommand(Command):
    def execute(self, customer_service: CustomerService, validator=Validator) -> None:
        """
        Prompts for input for the name of the parameter and checks if it is in the list of expected_arguments.

        If the parameter or parameter name is not valid, the program asks for re-entry
        until a valid value or 'cancel' is entered.
        'cancel' raises ValidateException.

        Calls the 'get_list_of_customers' command to get a list of customers and displays the result of the command.
        """
        arguments = []
        arguments_valid = False

        while not arguments_valid:
            input_arguments = input("sorted by:").split()

            if "cancel" in input_arguments:
                raise ValidateException("Input canceled.")

            if input_arguments is None:
                arguments_valid = True
            else:
                validation_result = validator.validate_data_for_list(input_arguments)
                arguments_valid = validation_result.isSuccess
                if not arguments_valid:
                    print(*validation_result.errors,
                          "Enter one or more arguments, separated by a space or nothing, "
                          "or enter 'cancel' to cancel:",
                          sep="\n")
                else:
                    arguments = input_arguments

        customer_data = customer_service.get_list_of_customers(arguments)

        if len(customer_data) == 0:
            print("No data")
        else:
            print(*customer_data, sep='\n')
