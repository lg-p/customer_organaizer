from operator import attrgetter
from enum import Enum


class Customer:
    def __init__(self, customer_id, full_name, position, name_of_the_organization, email, phone):
        self.customer_id = customer_id
        self.full_name = full_name
        self.position = position
        self.name_of_the_organization = name_of_the_organization
        self.email = email
        self.phone = phone

    def __str__(self):
        return '\t'.join([self.customer_id,
                          self.full_name,
                          self.position,
                          self.name_of_the_organization,
                          self.email,
                          self.phone])

    def __repr__(self):
        return '\t'.join([self.customer_id,
                          self.full_name,
                          self.position,
                          self.name_of_the_organization,
                          self.email,
                          self.phone])

    def update(self, full_name, position, name_of_the_organization, email, phone):
        self.full_name = full_name
        self.position = position
        self.name_of_the_organization = name_of_the_organization
        self.email = email
        self.phone = phone


class CustomerService:
    def __init__(self):
        self.customers = []

    def __str__(self):
        return '\n'.join(self.customers)

    def __repr__(self):
        return '\n'.join(self.customers)

    def insert_customer(self, customer_id, full_name, position, name_of_the_organization, email, phone):
        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self.customers.append(customer)

    def find_customer(self, argument_name, argument_value):
        for customer in self.customers:
            for attribute_name, attribute_value in customer.__dict__.items():
                if attribute_name == argument_name and attribute_value == argument_value:
                    return customer

    def update_customer(self, customer_id, full_name, position, name_of_the_organization, email, phone):
        customer = self.find_customer('customer_id', customer_id)
        customer.update(full_name, position, name_of_the_organization, email, phone)

    def delete_customer(self, customer_id):
        customer = self.find_customer('customer_id', customer_id)
        self.customers.remove(customer)

    def list_of_customer(self, sort_params):
        if len(sort_params) == 0:
            return self.customers
        else:
            order_customers = sorted(self.customers, key=attrgetter(*sort_params))
            return order_customers


class Command(Enum):
    def __init__(self, name, description):
        self.val = name
        self.description = description

    HELP = ("help",
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
            "\t'exit' - exit the program")
    EXIT = ("exit",
            "")
    INSERT = ("insert",
              "Error: 'insert' command requires 5 positional arguments\n"
              "< insert customer_id full_name position name_of_the_organization email phone >")
    UPDATE = ("update",
              "Error: 'update' command requires 5 positional arguments\n"
              "< update customer_id full_name position name_of_the_organization email phone >")
    FIND = ("find",
            "Error: 'find' command requires positional argument name (customer_id,"
            "full_name, position name,_of_the_organization, email, phone) and argument value\n"
            "< find 'one of the customer arguments' 'argument value'>")
    DELETE = ("delete",
              "Error: 'delete' command requires 1 positional arguments - customer_id\n"
              "< delete customer_id >")
    LIST = ("list",
            "Error: 'list' command requires any number positional arguments (customer_id,"
            "full_name, position name,_of_the_organization, email, phone)\n"
            "< list 'any number of customer arguments separated by a space' >")

    @staticmethod
    def get_by_value(value):
        for command in Command:
            if command.val.lower() == value.lower():
                return command


class Parser:
    def __init__(self):
        self.customer_service = CustomerService()

    def parse_command(self, command, arguments):
        if command == Command.HELP:
            print(command.HELP.description)
        elif command == Command.EXIT:
            raise SystemExit
        elif command == Command.INSERT:
            try:
                self.customer_service.insert_customer(*arguments)
            except TypeError:
                print(command.INSERT.description)
        elif command == Command.UPDATE:
            try:
                self.customer_service.update_customer(*arguments)
            except TypeError:
                print(command.UPDATE.description)
        elif command == Command.DELETE:
            try:
                self.customer_service.delete_customer(*arguments)
            except TypeError:
                print(command.DELETE.description)
        elif command == Command.LIST:
            try:
                list_of_customer = self.customer_service.list_of_customer(arguments)
                print(*list_of_customer, sep='\n')
            except TypeError:
                print(command.LIST.description)
        elif command == Command.FIND:
            try:
                customer = self.customer_service.find_customer(*arguments)
                print(customer)
            except TypeError:
                print(command.FIND.description)
        else:
            print('Invalid command!')
