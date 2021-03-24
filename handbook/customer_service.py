import os.path
from abc import ABC, abstractmethod
from xml.etree import ElementTree
from operator import attrgetter

from handbook.database_connection import create_connection


class Customer:
    def __init__(self, customer_id: str, full_name: str, position: str, name_of_the_organization: str, email: str,
                 phone: str) -> None:
        self.customer_id = customer_id
        self.full_name = full_name
        self.position = position
        self.name_of_the_organization = name_of_the_organization
        self.email = email
        self.phone = phone

    def __str__(self) -> str:
        return '\t'.join([self.customer_id,
                          self.full_name,
                          self.position,
                          self.name_of_the_organization,
                          self.email,
                          self.phone])

    def __repr__(self) -> str:
        return '\t'.join([self.customer_id,
                          self.full_name,
                          self.position,
                          self.name_of_the_organization,
                          self.email,
                          self.phone])

    def __eq__(self, other) -> bool:
        return isinstance(other, Customer) \
               and self.customer_id == other.customer_id

    def update(self, full_name: str, position: str, name_of_the_organization: str, email: str, phone: str):
        self.full_name = full_name
        self.position = position
        self.name_of_the_organization = name_of_the_organization
        self.email = email
        self.phone = phone


class StorageStrategy(ABC):
    @abstractmethod
    def insert_customer(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def find_customer(self, argument_name: str, argument_value: str) -> Customer:
        pass

    @abstractmethod
    def update_customer(self, customer: Customer, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        pass

    @abstractmethod
    def delete_customer(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def list_of_customer(self, sort_params: list) -> list:
        pass


class InMemoryStorage(StorageStrategy):
    def __init__(self) -> None:
        self.customers = []

    def __str__(self) -> str:
        return '\n'.join(self.customers)

    def __repr__(self) -> str:
        return '\n'.join(self.customers)

    def insert_customer(self, customer: Customer) -> None:
        self.customers.append(customer)

    def find_customer(self, argument_name: str, argument_value: str) -> Customer:
        for customer in self.customers:
            for attribute_name, attribute_value in customer.__dict__.items():
                if attribute_name == argument_name and attribute_value == argument_value:
                    return customer

    def update_customer(self, customer: Customer, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        customer.update(full_name, position, name_of_the_organization, email, phone)

    def delete_customer(self, customer):
        self.customers.remove(customer)

    def list_of_customer(self, sort_params: list) -> list:
        if len(sort_params) == 0:
            return self.customers
        else:
            order_customers = sorted(self.customers, key=attrgetter(*sort_params))
            return order_customers


class XMLStorage(StorageStrategy):
    def __init__(self, file_name: str) -> None:
        if not os.path.exists(file_name):
            root = ElementTree.Element('data')
            tree = ElementTree.ElementTree(root)
            tree.write(file_name)
        self.file_name = file_name

    def insert_customer(self, customer: Customer) -> None:
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

    def find_customer(self, argument_name: str, argument_value: str) -> Customer:
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

    def update_customer(self, customer: Customer, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
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

    def delete_customer(self, customer: Customer) -> None:
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

    def list_of_customer(self, sort_params: list) -> list:
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


class DataBaseStorage(StorageStrategy):
    def __init__(self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> None:
        self.connection = create_connection(db_name, db_user, db_password, db_host, db_port)

    def insert_customer(self, customer: Customer) -> None:
        query = (
            f"""INSERT INTO customers (customer_id, full_name, position, name_of_the_organization, email, phone) 
            VALUES (
                    '{customer.customer_id}', 
                    '{customer.full_name}',
                    '{customer.position}',
                    '{customer.name_of_the_organization}',
                    '{customer.email}',
                    '{customer.phone}'
                    );"""
                )
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        cursor.execute(query)

    def find_customer(self, argument_name: str, argument_value: str) -> str:
        query = f"SELECT * from customers WHERE customers.{argument_name} = '{argument_value}';"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    def update_customer(self, customer: Customer, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        query = f"""UPDATE customers 
                SET 
                    full_name = '{full_name}',
                    position = '{position}',
                    name_of_the_organization = '{name_of_the_organization}',
                    email = '{email}',
                    phone = '{phone}'
                WHERE customer_id = '{customer.customer_id}';"""
        cursor = self.connection.cursor()
        cursor.execute(query)

    def delete_customer(self, customer: Customer) -> None:
        query = f"DELETE FROM customers WHERE customer_id = '{customer.customer_id}'"
        cursor = self.connection.cursor()
        cursor.execute(query)

    def list_of_customer(self, sort_params: list) -> list:
        if len(sort_params) == 0:
            query = "SELECT * from customers;"
        else:
            param = ",".join(sort_params)
            query = f"SELECT * from customers ORDER BY {param};"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


class CustomerService:
    def __init__(self, storage: StorageStrategy) -> None:
        self._storage = storage

    @staticmethod
    def storage(sys_arguments):
        if sys_arguments.path is not None:
            return XMLStorage(sys_arguments.path)
        elif sys_arguments.db is not None:
            return create_connection(
                sys_arguments.db,
                sys_arguments.user,
                sys_arguments.password,
                sys_arguments.host,
                sys_arguments.port
            )
        else:
            return InMemoryStorage

    def create_customer(self, customer_id: str, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self._storage.insert_customer(customer)

    def display_customer_details(self, argument_name: str, argument_value: str) -> None:
        customer = self._storage.find_customer(argument_name, argument_value)
        print(customer)

    def update_customer(self, customer_id: str, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        customer = self._storage.find_customer('customer_id', customer_id)
        self._storage.update_customer(customer, full_name, position, name_of_the_organization, email, phone)

    def remove_customer(self, customer_id: str) -> None:
        customer = self._storage.find_customer('customer_id', customer_id)
        self._storage.delete_customer(customer)

    def display_customer_data(self, sort_params: list) -> None:
        customer_data = self._storage.list_of_customer(sort_params)
        print(*customer_data, sep='\n')
