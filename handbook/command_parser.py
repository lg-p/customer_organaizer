from enum import Enum

from handbook.customer_service import CustomerService
from handbook.validator import Validator


class Command(Enum):
    def __init__(self, name, description):
        self.val = name
        self.description = description

    HELP = (
        "help",
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
        "\t'exit' - exit the program"
    )
    EXIT = (
        "exit",
        ""
    )
    INSERT = (
        "insert",
        "Error: 'insert' command requires 5 positional arguments separated by commas (no spaces!)\n"
        "<insert customer_id,full_name,position,name_of_the_organization,email,phone>"
    )
    UPDATE = (
        "update",
        "Error: 'update' command requires 5 positional arguments separated by commas (no spaces!)\n"
        "<update customer_id,full_name,position,name_of_the_organization,email,phone>"
    )
    FIND = (
        "find",
        "Error: 'find' command requires one positional argument name (customer_id,"
        "full_name, position name,_of_the_organization, email, phone) and one argument value "
        "separated by commas (no spaces!)\n"
        "<find 'one of the customer arguments','argument value'>"
    )
    DELETE = (
        "delete",
        "Error: 'delete' command requires 1 positional arguments - customer_id\n"
        "<delete customer_id>"
    )
    LIST = (
        "list",
        "Error: 'list' command requires any number positional arguments (customer_id,"
        "full_name, position name,_of_the_organization, email, phone) separated by commas (no spaces!)\n"
        "<list 'any number of customer arguments separated by a space'>"
    )

    @staticmethod
    def get_by_value(value):
        for command in Command:
            if command.val.lower() == value.lower():
                return command


class Parser:
    def __init__(self):
        self.customer_service = CustomerService()
        self.validator = Validator()

    def parse_command(self, command, arguments):
        if command == Command.HELP:
            print(command.HELP.description)
        elif command == Command.EXIT:
            raise SystemExit
        elif command == Command.INSERT:
            valid_arguments = dict()
            valid_arguments['customer_id'] = arguments[0]
            valid_arguments['full_name'] = arguments[1]
            valid_arguments['position'] = arguments[2]
            valid_arguments['name_of_the_organization'] = arguments[3]
            valid_arguments['email'] = arguments[4]
            valid_arguments['phone'] = arguments[5]
            if self.validator.validate_data(valid_arguments):
                try:
                    self.customer_service.insert_customer(*arguments)
                except TypeError:
                    print(command.INSERT.description)
        elif command == Command.UPDATE:
            valid_arguments = dict()
            valid_arguments['customer_id'] = arguments[0]
            valid_arguments['full_name'] = arguments[1]
            valid_arguments['position'] = arguments[2]
            valid_arguments['name_of_the_organization'] = arguments[3]
            valid_arguments['email'] = arguments[4]
            valid_arguments['phone'] = arguments[5]
            if self.validator.validate_data(valid_arguments):
                try:
                    self.customer_service.update_customer(*arguments)
                except TypeError:
                    print(command.UPDATE.description)
        elif command == Command.DELETE:
            valid_arguments = dict()
            valid_arguments['customer_id'] = arguments[0]
            if self.validator.validate_data(valid_arguments):
                try:
                    self.customer_service.delete_customer(*arguments)
                except TypeError:
                    print(command.DELETE.description)
        elif command == Command.LIST:
            if self.validator.validate_data_for_list(arguments):
                try:
                    list_of_customer = self.customer_service.list_of_customer(arguments)
                    print(*list_of_customer, sep='\n')
                except TypeError:
                    print(command.LIST.description)
        elif command == Command.FIND:
            valid_arguments = dict()
            argument_name, argument_value = arguments[0], arguments[1]
            valid_arguments[argument_name] = argument_value
            if self.validator.validate_data(valid_arguments):
                try:
                    customer = self.customer_service.find_customer(*arguments)
                    print(customer)
                except TypeError:
                    print(command.FIND.description)
        else:
            print('Invalid command!')
