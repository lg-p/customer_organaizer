import unittest

from handbook.customer_service import InMemoryStorage, Customer


class TestCustomerStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.customer_storage = InMemoryStorage()

        self.customer_id = "000000001"
        self.full_name = "Ivanov Vasyl"
        self.position = "developer"
        self.name_of_the_organization = "FGH-2000"
        self.email = "vasyl@mail.ru"
        self.phone = "79278763423"

    def test_insert_customer(self) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )

        # WHEN
        self.customer_storage.insert_customer(expected_customer)

        # THEN
        self.assertIn(expected_customer, self.customer_storage.customers.values())

    def test_find_customer(self) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        self.customer_storage.insert_customer(expected_customer)

        # WHEN
        customer = self.customer_storage.find_customer("customer_id", self.customer_id)

        # THEN
        self.assertIsNotNone(customer)

    def test_update_customer(self) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        self.customer_storage.insert_customer(expected_customer)

        # WHEN
        new_phone = "79278763447"
        self.customer_storage.update_customer(expected_customer, self.full_name, self.position,
                                              self.name_of_the_organization, self.email, new_phone)

        # THEN
        customer = self.customer_storage.find_customer("customer_id", self.customer_id)
        self.assertEqual(customer.phone, new_phone)

    def test_delete_customer(self) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        self.customer_storage.insert_customer(expected_customer)

        # WHEN
        self.customer_storage.delete_customer(expected_customer)

        # THEN
        customer = self.customer_storage.find_customer("customer_id", self.customer_id)
        self.assertIsNone(customer)

    def test_list_of_customer(self) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        self.customer_storage.insert_customer(expected_customer)

        # WHEN
        list_of_customer = self.customer_storage.list_of_customer([])

        # THEN
        self.assertIn(expected_customer, list_of_customer)

    def test_list_of_customer_ordered(self) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        self.customer_storage.insert_customer(expected_customer)

        # WHEN
        list_of_customer = self.customer_storage.list_of_customer(["full_name"])

        # THEN
        self.assertIn(expected_customer, list_of_customer)


if __name__ == '__main__':
    unittest.main()
