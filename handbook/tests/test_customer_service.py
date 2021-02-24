import unittest

from handbook.customer_service import InMemoryService, Customer


class TestCustomerService(unittest.TestCase):
    def setUp(self) -> None:
        self.customer_service = InMemoryService()

    def test_insert_customer(self):
        # GIVEN
        customer_id = "000000001"
        full_name = "Ivanov Vasyl"
        position = "developer"
        name_of_the_organization = "FGH-2000"
        email = "vasyl@mail.ru"
        phone = "79278763423"

        # WHEN
        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self.customer_service.insert_customer(customer)

        # THEN
        self.assertIn(customer, self.customer_service.customers)

    def test_find_customer(self):
        # GIVEN
        customer_id = "000000001"
        full_name = "Ivanov Vasyl"
        position = "developer"
        name_of_the_organization = "FGH-2000"
        email = "vasyl@mail.ru"
        phone = "79278763423"

        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self.customer_service.insert_customer(customer)

        # WHEN
        customer = self.customer_service.find_customer("customer_id", customer_id)

        # THEN
        self.assertIsNotNone(customer)

    def test_update_customer(self):
        # GIVEN
        customer_id = "000000001"
        full_name = "Ivanov Vasyl"
        position = "developer"
        name_of_the_organization = "FGH-2000"
        email = "vasyl@mail.ru"
        phone = "79278763423"

        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self.customer_service.insert_customer(customer)

        # WHEN
        new_phone = "79278763447"
        self.customer_service.update_customer(customer, full_name, position, name_of_the_organization, email,
                                              new_phone)

        # THEN
        customer = self.customer_service.find_customer("customer_id", customer_id)
        self.assertEqual(customer.phone, new_phone)

    def test_delete_customer(self):
        # GIVEN
        customer_id = "000000001"
        full_name = "Ivanov Vasyl"
        position = "developer"
        name_of_the_organization = "FGH-2000"
        email = "vasyl@mail.ru"
        phone = "79278763423"

        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self.customer_service.insert_customer(customer)

        # WHEN
        self.customer_service.delete_customer(customer)

        # THEN
        customer = self.customer_service.find_customer("customer_id", customer_id)
        self.assertIsNone(customer)

    def test_list_of_customer(self):
        # GIVEN
        customer_id = "000000001"
        full_name = "Ivanov Vasyl"
        position = "developer"
        name_of_the_organization = "FGH-2000"
        email = "vasyl@mail.ru"
        phone = "79278763423"

        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self.customer_service.insert_customer(customer)

        # WHEN
        list_of_customer = self.customer_service.list_of_customer([])

        # THEN
        self.assertIn(customer, list_of_customer)

    def test_list_of_customer_ordered(self):
        # GIVEN
        customer_id = "000000001"
        full_name = "Ivanov Vasyl"
        position = "developer"
        name_of_the_organization = "FGH-2000"
        email = "vasyl@mail.ru"
        phone = "79278763423"

        customer = Customer(customer_id, full_name, position, name_of_the_organization, email, phone)
        self.customer_service.insert_customer(customer)

        # WHEN
        list_of_customer = self.customer_service.list_of_customer(["full_name"])

        # THEN
        self.assertIn(customer, list_of_customer)


if __name__ == '__main__':
    unittest.main()
