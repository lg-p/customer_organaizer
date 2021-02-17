from xml.etree import ElementTree
from operator import attrgetter
from collections import namedtuple


class XMLService:
    @staticmethod
    def create_file(file_name):
        root = ElementTree.Element('data')
        tree = ElementTree.ElementTree(root)
        tree.write(file_name)

    @staticmethod
    def insert_customer(file_name, arguments):
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        customer = ElementTree.Element("customer")
        root.append(customer)

        customer_id = ElementTree.SubElement(customer, 'customer_id')
        customer_id.text = arguments[0]

        full_name = ElementTree.SubElement(customer, 'full_name')
        full_name.text = arguments[1]

        position = ElementTree.SubElement(customer, 'position')
        position.text = arguments[2]

        name_of_the_organization = ElementTree.SubElement(customer, 'name_of_the_organization')
        name_of_the_organization.text = arguments[3]

        email = ElementTree.SubElement(customer, 'email')
        email.text = arguments[4]

        phone = ElementTree.SubElement(customer, 'phone')
        phone.text = arguments[5]

        tree.write(file_name)

    @staticmethod
    def find_customer(file_name, argument_name, argument_value):
        found = False
        Customer = namedtuple("Customer", "customer_id full_name position name_of_the_organization email phone")

        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        for customer in root:
            customer_id, full_name, position, name_of_the_organization, email, phone = '', '', '', '', '', ''
            for attr in customer:
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
        # f = tree.iterfind("customer/[@customer_id='000000001']")
        # for elem in f:
        #     print(elem.tag, elem.text)

    @staticmethod
    def update_customer(file_name, arguments):
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        for customer in root:
            for attr in customer:
                if attr.tag == 'customer_id' and attr.text == arguments[0]:
                    for attribute in customer:
                        if attribute.tag == 'customer_id':
                            attribute.text = arguments[0]
                        elif attribute.tag == 'full_name':
                            attribute.text = arguments[1]
                        elif attribute.tag == 'position':
                            attribute.text = arguments[2]
                        elif attribute.tag == 'name_of_the_organization':
                            attribute.text = arguments[3]
                        elif attribute.tag == 'email':
                            attribute.text = arguments[4]
                        elif attribute.tag == 'phone':
                            attribute.text = arguments[5]
        tree.write(file_name)

    @staticmethod
    def delete_customer(file_name, argument_value):
        found = False
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        for customer in root.findall('customer'):
            for attr in customer:
                if attr.tag == 'customer_id' and attr.text == argument_value:
                    found = True
            if found:
                root.remove(customer)
                tree.write(file_name)
                return

    @staticmethod
    def get_everything(file_name, sort_params):
        customers_all = []
        customer_id, full_name, position, name_of_the_organization, email, phone = '', '', '', '', '', ''
        Customer = namedtuple("Customer", "customer_id full_name position name_of_the_organization email phone")

        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        for customer in root:
            for attribute in customer:
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
