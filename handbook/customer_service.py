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


class CustomerException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


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
        """
        Inserts a customer instance into the storage
        :param customer: Customer
        :return: None
        """
        self.customers.append(customer)

    def find_customer(self, argument_name: str, argument_value: str) -> Customer:
        """
        Searches for a customer in the storage by argument name and value
        and returns the result
        :param argument_name: the name of the argument to search for
        :param argument_value: the value of the argument to search for
        :return: Customer
        """
        for customer in self.customers:
            for attribute_name, attribute_value in customer.__dict__.items():
                if attribute_name == argument_name and attribute_value == argument_value:
                    return customer

    def update_customer(self, customer: Customer, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        """
        Updates the customer instance in the storage
        :param customer: Customer
        :param full_name: surname, name, patronymic of the customer
        :param position: customer position
        :param name_of_the_organization: name of company
        :param email: Customer email address
        :param phone: customer's phone number
        :return: None
        """
        customer.update(full_name, position, name_of_the_organization, email, phone)

    def delete_customer(self, customer: Customer) -> None:
        """
        Remove the customer instance in the storage
        :param customer: Customer
        :return: None
        """
        self.customers.remove(customer)

    def list_of_customer(self, sort_params: list) -> list:
        """
        Searches for all customers in the storage
        and returns the result
        :param sort_params: list of parameters for sorting
        :return: List
        """
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
        """
        Inserts a customer instance into the storage
        and writes the file
        :param customer: Customer
        :return: None
        """
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
        """
        Searches for a customer in the storage by argument name and value
        and returns the result
        :param argument_name: the name of the argument to search for
        :param argument_value: the value of the argument to search for
        :return: Customer
        """
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
        """
        Updates the customer instance in the storage
        and writes the file
        :param customer: Customer
        :param full_name: surname, name, patronymic of the customer
        :param position: customer position
        :param name_of_the_organization: name of company
        :param email: Customer email address
        :param phone: customer's phone number
        :return: None
        """
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
        """
        Remove the customer instance in the storage
        and writes the file
        :param customer: Customer
        :return: None
        """
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
        """
        Searches for all customers in the storage
        and returns the result
        :param sort_params: list of parameters for sorting
        :return: List
        """
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
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def insert_customer(self, customer: Customer) -> None:
        """
        Inserts a customer instance into the storage
        :param customer: Customer
        :return: None
        """
        query = f"""
        INSERT INTO 
            customers (customer_id, full_name, position, name_of_the_organization, email, phone) 
        VALUES (
            '{customer.customer_id}', 
            '{customer.full_name}',
            '{customer.position}',
            '{customer.name_of_the_organization}',
            '{customer.email}',
            '{customer.phone}'
            );
        """
        with create_connection(self.db_name, self.db_user, self.db_password, self.db_host, self.db_port) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()

    def find_customer(self, argument_name: str, argument_value: str) -> str:
        """
        Searches for a customer in the storage by argument name and value
        and returns the result
        :param argument_name: the name of the argument to search for
        :param argument_value: the value of the argument to search for
        :return: Customer
        """
        query = f"""
        SELECT *
        FROM customers 
        WHERE 
            customers.{argument_name} = '{argument_value}';
        """
        with create_connection(self.db_name, self.db_user, self.db_password, self.db_host, self.db_port) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result

    def update_customer(self, customer: Customer, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        """
        Updates the customer instance in the storage
        :param customer: Customer
        :param full_name: surname, name, patronymic of the customer
        :param position: customer position
        :param name_of_the_organization: name of company
        :param email: Customer email address
        :param phone: customer's phone number
        :return: None
        """
        query = f"""
        UPDATE customers 
        SET 
            full_name = '{full_name}',
            position = '{position}',
            name_of_the_organization = '{name_of_the_organization}',
            email = '{email}',
            phone = '{phone}'
        WHERE 
            customer_id = '{customer.customer_id}';
        """
        with create_connection(self.db_name, self.db_user, self.db_password, self.db_host, self.db_port) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()

    def delete_customer(self, customer: Customer) -> None:
        """
        Remove the customer instance in the storage
        and writes the file
        :param customer: Customer
        :return: None
        """
        query = f"""
        DELETE 
        FROM customers 
        WHERE 
            customer_id = '{customer.customer_id}'
        """
        with create_connection(self.db_name, self.db_user, self.db_password, self.db_host, self.db_port) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()

    def list_of_customer(self, sort_params: list) -> list:
        """
        Searches for all customers in the storage
        and returns the result
        :param sort_params: list of parameters for sorting
        :return: List
        """
        if len(sort_params) == 0:
            query = """
            SELECT * 
            FROM customers;
            """
        else:
            param = ",".join(sort_params)
            query = f"""
            SELECT * 
            FROM customers 
            ORDER BY 
                {param};
            """
        with create_connection(self.db_name, self.db_user, self.db_password, self.db_host, self.db_port) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result


class StorageFactory:
    @staticmethod
    def get_storage(sys_arguments) -> StorageStrategy:
        """
        Selects storage based on input arguments
        """
        if sys_arguments.path is not None:
            return XMLStorage(sys_arguments.path)
        elif sys_arguments.db is not None:
            return DataBaseStorage(
                sys_arguments.db,
                sys_arguments.user,
                sys_arguments.password,
                sys_arguments.host,
                sys_arguments.port
            )
        else:
            return InMemoryStorage()


class CustomerService:
    def __init__(self, storage: StorageStrategy) -> None:
        self._storage = storage

    def create_customer(self, customer_id: str, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        """
        Checks for the existence of a customer
        Raises 'CustomerException' exception if the customer exists
        Calls the 'insert_customer' command to insert the customer into the storage
        :param customer_id: customer ID
        :param full_name: surname, name, patronymic of the customer
        :param position: customer position
        :param name_of_the_organization: name of company
        :param email: Customer email address
        :param phone: customer's phone number
        :return: None
        """
        expected_customer = self._storage.find_customer("customer_id", customer_id)
        if expected_customer is not None:
            raise CustomerException("Customer already exists")
        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self._storage.insert_customer(customer)

    def find_customer(self, argument_name: str, argument_value: str) -> Customer:
        """
        Calls the 'find_customer' command to find the customer into the storage
        and return result
        :param argument_name: the name of the argument to search for
        :param argument_value: the value of the argument to search for
        :return:
        """
        customer = self._storage.find_customer(argument_name, argument_value)
        return customer

    def update_customer(self, customer_id: str, full_name: str, position: str, name_of_the_organization: str,
                        email: str, phone: str) -> None:
        """
        Searches for a customer by ID  and
        calls the 'update_customer' command to update the customer into the storage
        :param customer_id: customer ID
        :param full_name: surname, name, patronymic of the customer
        :param position: customer position
        :param name_of_the_organization: name of company
        :param email: Customer email address
        :param phone: customer's phone number
        :return: None
        """
        customer = self._storage.find_customer('customer_id', customer_id)
        self._storage.update_customer(customer, full_name, position, name_of_the_organization, email, phone)

    def remove_customer(self, customer_id: str) -> None:
        """
        Searches for a customer by ID  and
        calls the 'delete_customer' command to remove the customer into the storage
        :param customer_id: customer ID
        :return: None
        """
        customer = self._storage.find_customer('customer_id', customer_id)
        self._storage.delete_customer(customer)

    def get_list_of_customers(self, sort_params: list) -> list:
        """
        Calls the 'list_of_customer' command to find the customer into the storage
        and return result
        :param sort_params: list of parameters for sorting
        :return: List
        """
        customer_data = self._storage.list_of_customer(sort_params)
        return customer_data
