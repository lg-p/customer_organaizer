import argparse
from operator import attrgetter


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

    def update(self, customer_id, full_name, position, name_of_the_organization, email, phone):
        self.customer_id = customer_id
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

    def find_customer(self, arg):
        for cust in self.customers:
            for attr in cust.__dict__.items():
                if arg in attr:
                    return cust

    def update_customer(self, customer_id, full_name, position, name_of_the_organization, email, phone):
        cust = self.find_customer(customer_id)
        cust.update(customer_id, full_name, position, name_of_the_organization, email, phone)

    def delete_customer(self, customer_id):
        cust = self.find_customer(customer_id)
        print(customer_id)
        self.customers.remove(cust)

    def list_of_customer(self, args):
        if len(args) == 0:
            print(self.customers, sep='\n')
        else:
            order_customers = sorted(self.customers, key=attrgetter(*args))
            print(*order_customers, sep='\n')

    @staticmethod
    def help():
        print("The program is designed to store, view and edit customer data\n"
              "Commands:\n"
              "\n"
              "\t'insert' - insert a new customer\n"
              "\t\targuments:\n"
              "\t\t\tcustomer_id\n"
              "\t\t\tfull_name\n"
              "\t\t\tposition\n"
              "\t\t\tname_of_the_organization\n"
              "\t\t\temail\n"
              "\t\t\tphone\n"
              "\n"
              "\t'find' - searches for a customer\n"
              "\t\targuments:\n"
              "\t\t\tone of the customer arguments \n"
              "\n"
              "\t'update' - update a customer\n"
              "\t\targuments:\n"
              "\t\t\tcustomer_id\n"
              "\t\t\tfull_name\n"
              "\t\t\tposition\n"
              "\t\t\tname_of_the_organization\n"
              "\t\t\temail\n"
              "\t\t\tphone\n"
              "\n"
              "\t'delete' - removes customer\n"
              "\t\targuments:\n"
              "\t\t\tcustomer_id\n"
              "\n"
              "\t'list' - displays a list of customers sorted by the listed arguments \n"
              "\t\targuments:\n"
              "\t\t\tany number of customer arguments separated by a space\n"
              "\n"
              "\t'exit' - exit the program")


parser = argparse.ArgumentParser(description='The program is designed to store, view and edit customer data')
# parser.add_argument('path', type=str, help='XML file path')
args = parser.parse_args()

customers = CustomerService()

while True:

    commands = input().split()

    if commands[0] == 'help':
        customers.help()
    elif commands[0] == 'exit':
        raise SystemExit
    elif commands[0] == 'insert':
        try:
            customers.insert_customer(*commands[1:])
        except TypeError:
            print("Error: 'insert' command requires 5 positional arguments\n"
                  "< insert customer_id full_name position name_of_the_organization email phone >")
    elif commands[0] == 'update':
        try:
            customers.update_customer(*commands[1:])
        except TypeError:
            print("Error: 'update' command requires 5 positional arguments\n"
                  "< update customer_id full_name position name_of_the_organization email phone >")
    elif commands[0] == 'delete':
        try:
            customers.delete_customer(*commands[1:])
        except TypeError as e:
            print("Error: 'delete' command requires 1 positional arguments - customer_id\n"
                  "< delete customer_id >")
    elif commands[0] == 'list':
        try:
            customers.list_of_customer(commands[1:])
        except TypeError as e:
            print("Error: 'list' command requires any number positional arguments (customer_id, "
                  "full_name, position name,_of_the_organization, email, phone)\n"
                  "< list 'any number of customer arguments separated by a space' >")
    elif commands[0] == 'find':
        try:
            print(customers.find_customer(*commands[1:]))
        except TypeError:
            print("Error: 'find' command requires 1 positional arguments (customer_id, "
                  "full_name, position name,_of_the_organization, email, phone)\n"
                  "< find 'one of the customer arguments' >")
    else:
        print('Invalid command!')
