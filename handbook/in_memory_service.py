from operator import attrgetter
from handbook.customer_service import StorageStrategy


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


class InMemoryService(StorageStrategy):
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
