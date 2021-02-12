import unittest
from handbook.customer_service import *


class TestCustomerService(unittest.TestCase):
    def setUp(self) -> None:
        self.customer_service = CustomerService()

    def test_insert_customer(self):
        # GIVEN
        customer_id = '000000001'
        full_name = 'Ivanov Vasyl'
        position = 'developer'
        name_of_the_organization = 'FGH'
        email = 'vasyl@mail.ru'
        phone = '79278763423'

        # WHEN
        self.customer_service.insert_customer(customer_id, full_name, position, name_of_the_organization, email, phone)

        # THEN
        self.assertEqual(len(self.customer_service.customers), 1)

    def test_find_customer(self):
        # GIVEN
        customer_id = '000000001'
        full_name = 'Ivanov Vasyl'
        position = 'developer'
        name_of_the_organization = 'FGH'
        email = 'vasyl@mail.ru'
        phone = '79278763423'

        self.customer_service.insert_customer(customer_id, full_name, position, name_of_the_organization, email, phone)

        # WHEN
        customer = self.customer_service.find_customer('customer_id', customer_id)

        # THEN
        self.assertEqual(customer.customer_id, customer_id)

    def test_update_customer(self):
        # GIVEN
        customer_id = '000000001'
        full_name = 'Ivanov Vasyl'
        position = 'developer'
        name_of_the_organization = 'FGH'
        email = 'vasyl@mail.ru'
        phone = '79278763423'

        self.customer_service.insert_customer(customer_id, full_name, position, name_of_the_organization, email, phone)

        # WHEN
        new_phone = '79278763447'

        self.customer_service.update_customer(customer_id, full_name, position, name_of_the_organization, email,
                                              new_phone)

        # THEN
        customer = self.customer_service.find_customer('customer_id', customer_id)
        self.assertEqual(customer.phone, new_phone)

    def test_delete_customer(self):
        # GIVEN
        customer_id = '000000001'
        full_name = 'Ivanov Vasyl'
        position = 'developer'
        name_of_the_organization = 'FGH'
        email = 'vasyl@mail.ru'
        phone = '79278763423'

        self.customer_service.insert_customer(customer_id, full_name, position, name_of_the_organization, email, phone)

        # WHEN
        self.customer_service.delete_customer(customer_id)

        # THEN
        customer = self.customer_service.find_customer('customer_id', customer_id)
        self.assertEqual(customer, None)

    def test_list_of_customer(self):
        # GIVEN
        customer_id = '000000001'
        full_name = 'Ivanov Vasyl'
        position = 'developer'
        name_of_the_organization = 'FGH'
        email = 'vasyl@mail.ru'
        phone = '79278763423'

        self.customer_service.insert_customer(customer_id, full_name, position, name_of_the_organization, email, phone)

        # WHEN
        list_of_customer = self.customer_service.list_of_customer([])

        # THEN
        self.assertEqual(len(list_of_customer), 1)

    def test_list_of_customer_ordered(self):
        # GIVEN
        customer_id = '000000001'
        full_name = 'Ivanov Vasyl'
        position = 'developer'
        name_of_the_organization = 'FGH'
        email = 'vasyl@mail.ru'
        phone = '79278763423'

        self.customer_service.insert_customer(customer_id, full_name, position, name_of_the_organization, email, phone)

        # WHEN
        list_of_customer = self.customer_service.list_of_customer(['full_name'])

        # THEN
        self.assertEqual(len(list_of_customer), 1)


if __name__ == '__main__':
    unittest.main()
