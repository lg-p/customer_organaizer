import os.path
from abc import ABC, abstractmethod
from xml.etree import ElementTree
from operator import attrgetter


class StorageStrategy(ABC):
    @abstractmethod
    def insert_customer(self, customer):
        pass

    @abstractmethod
    def find_customer(self, argument_name, argument_value):
        pass

    @abstractmethod
    def update_customer(self, customer_id, full_name, position, name_of_the_organization, email, phone):
        pass

    @abstractmethod
    def delete_customer(self, customer_id):
        pass

    @abstractmethod
    def list_of_customer(self, sort_params):
        pass


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

    def insert_customer(self, customer):
        self.customers.append(customer)

    def find_customer(self, argument_name, argument_value):
        for customer in self.customers:
            for attribute_name, attribute_value in customer.__dict__.items():
                if attribute_name == argument_name and attribute_value == argument_value:
                    return customer

    def update_customer(self, customer, full_name, position, name_of_the_organization, email, phone):
        customer.update(full_name, position, name_of_the_organization, email, phone)

    def delete_customer(self, customer):
        self.customers.remove(customer)

    def list_of_customer(self, sort_params):
        if len(sort_params) == 0:
            return self.customers
        else:
            order_customers = sorted(self.customers, key=attrgetter(*sort_params))
            return order_customers


class XMLService(StorageStrategy):

    def __init__(self, file_name):
        if not os.path.exists(file_name):
            root = ElementTree.Element('data')
            tree = ElementTree.ElementTree(root)
            tree.write(file_name)
        self.file_name = file_name

    def insert_customer(self, customer):
        tree = ElementTree.parse(self.file_name)
        root = tree.getroot()
        element_customer = ElementTree.Element("customer")
        root.append(element_customer)

        element_customer_id = ElementTree.SubElement(element_customer, 'customer_id')
        element_customer_id.text = customer.customer_id

        element_full_name = ElementTree.SubElement(element_customer, 'full_name')
        element_full_name.text = customer.full_name

        element_position = ElementTree.SubElement(element_customer, 'position')
        element_position.text = customer.position

        element_name_of_the_organization = ElementTree.SubElement(element_customer, 'name_of_the_organization')
        element_name_of_the_organization.text = customer.name_of_the_organization

        element_email = ElementTree.SubElement(element_customer, 'email')
        element_email.text = customer.email

        element_phone = ElementTree.SubElement(element_customer, 'phone')
        element_phone.text = customer.phone

        tree.write(self.file_name)

    def find_customer(self, argument_name, argument_value):
        found = False

        tree = ElementTree.parse(self.file_name)
        root = tree.getroot()
        for element_customer in root:
            customer_id, full_name, position, name_of_the_organization, email, phone = '', '', '', '', '', ''
            for attr in element_customer:
                if attr.tag == 'customer_id':
                    customer_id = attr.text
                elif attr.tag == 'full_name':
                    full_name = attr.text
                elif attr.tag == 'position':
                    position = attr.text
                elif attr.tag == 'name_of_the_organization':
                    name_of_the_organization = attr.text
                elif attr.tag == 'email':
                    email = attr.text
                elif attr.tag == 'phone':
                    phone = attr.text
                if attr.tag == argument_name and attr.text == argument_value:
                    found = True
            if found:
                return Customer(customer_id, full_name, position, name_of_the_organization, email, phone)

    def update_customer(self, customer, full_name, position, name_of_the_organization, email, phone):
        tree = ElementTree.parse(self.file_name)
        root = tree.getroot()
        for element_customer in root:
            for attr in element_customer:
                if attr.tag == 'customer_id' and attr.text == customer.customer_id:
                    for attribute in element_customer:
                        if attribute.tag == 'customer_id':
                            attribute.text = customer.customer_id
                        elif attribute.tag == 'full_name':
                            attribute.text = full_name
                        elif attribute.tag == 'position':
                            attribute.text = position
                        elif attribute.tag == 'name_of_the_organization':
                            attribute.text = name_of_the_organization
                        elif attribute.tag == 'email':
                            attribute.text = email
                        elif attribute.tag == 'phone':
                            attribute.text = phone
        tree.write(self.file_name)

    def delete_customer(self, customer):
        found = False
        tree = ElementTree.parse(self.file_name)
        root = tree.getroot()
        for element_customer in root.findall('customer'):
            for attr in element_customer:
                if attr.tag == 'customer_id' and attr.text == customer.customer_id:
                    found = True
            if found:
                root.remove(element_customer)
                tree.write(self.file_name)
                return

    def list_of_customer(self, sort_params):
        customers_all = []
        customer_id, full_name, position, name_of_the_organization, email, phone = '', '', '', '', '', ''

        tree = ElementTree.parse(self.file_name)
        root = tree.getroot()
        for element_customer in root:
            for attribute in element_customer:
                if attribute.tag == 'customer_id':
                    customer_id = attribute.text
                elif attribute.tag == 'full_name':
                    full_name = attribute.text
                elif attribute.tag == 'position':
                    position = attribute.text
                elif attribute.tag == 'name_of_the_organization':
                    name_of_the_organization = attribute.text
                elif attribute.tag == 'email':
                    email = attribute.text
                elif attribute.tag == 'phone':
                    phone = attribute.text
            customers_all.append(Customer(customer_id, full_name, position, name_of_the_organization, email, phone))
        if len(sort_params) > 0:
            customers_all.sort(key=attrgetter(*sort_params))
            return customers_all
        else:
            return customers_all


class CustomerService:
    def __init__(self, storage):
        self._storage = storage

    @staticmethod
    def storage(file_name):
        if file_name is not None:
            return XMLService
        else:
            return InMemoryService

    def create_customer(self, customer_id, full_name, position, name_of_the_organization, email, phone):
        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self._storage.insert_customer(customer)

    def display_customer_details(self, argument_name, argument_value):
        customer = self._storage.find_customer(argument_name, argument_value)
        print(customer)

    def update_customer(self, customer_id, full_name, position, name_of_the_organization, email, phone):
        customer = self._storage.find_customer('customer_id', customer_id)
        self._storage.update_customer(customer, full_name, position, name_of_the_organization, email, phone)

    def remove_customer(self, customer_id):
        customer = self._storage.find_customer('customer_id', customer_id)
        self._storage.delete_customer(customer)

    def display_customer_data(self, sort_params):
        customer_data = self._storage.list_of_customer(sort_params)
        print(*customer_data, sep='\n')
