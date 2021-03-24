import unittest
from operator import eq
from unittest.mock import patch, Mock


from handbook.customer_service import Customer, CustomerService


class TestCustomerService(unittest.TestCase):
    def setUp(self) -> None:
        self.customer_id = "000000001"
        self.full_name = "Ivanov Vasyl"
        self.position = "developer"
        self.name_of_the_organization = "FGH-2000"
        self.email = "vasyl@mail.ru"
        self.phone = "79278763423"

    @patch('handbook.customer_service.StorageStrategy')
    def test_create_customer(self, MockStorageStrategy: Mock) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        customer_storage_mock = MockStorageStrategy()
        customer_service = CustomerService(customer_storage_mock)

        # WHEN
        customer_service.create_customer(self.customer_id,
                                         self.full_name,
                                         self.position,
                                         self.name_of_the_organization,
                                         self.email,
                                         self.phone
                                         )

        # THEN
        self.assertTrue(customer_storage_mock.insert_customer.assert_called_once)

        customer_to_insert = customer_storage_mock.insert_customer.call_args.args[0]
        self.assertTrue(eq(expected_customer, customer_to_insert))

    @patch('handbook.customer_service.StorageStrategy')
    def test_display_customer_details(self, MockStorageStrategy: Mock) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        customer_storage_mock = MockStorageStrategy()
        customer_storage_mock.find_customer.return_value = expected_customer
        customer_service = CustomerService(customer_storage_mock)

        # WHEN
        customer_service.display_customer_details("customer_id", self.customer_id)

        # THEN
        self.assertTrue(customer_storage_mock.find_customer.assert_called_once)

    @patch('handbook.customer_service.StorageStrategy')
    def test_update_customer(self, MockStorageStrategy: Mock) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        new_phone = "79278763447"

        customer_storage_mock = MockStorageStrategy()
        customer_storage_mock.find_customer.return_value = expected_customer
        customer_service = CustomerService(customer_storage_mock)

        # WHEN
        customer_service.update_customer(self.customer_id,
                                         self.full_name,
                                         self.position,
                                         self.name_of_the_organization,
                                         self.email,
                                         new_phone
                                         )

        # THEN
        self.assertTrue(customer_storage_mock.update_customer.assert_called_once)

        updated_phone = customer_storage_mock.update_customer.call_args.args[5]
        self.assertEqual(updated_phone, new_phone)

        customer_to_update = customer_storage_mock.update_customer.call_args.args[0]
        self.assertTrue(eq(expected_customer, customer_to_update))

    @patch('handbook.customer_service.StorageStrategy')
    def test_remove_customer(self, MockStorageStrategy: Mock) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        customer_storage_mock = MockStorageStrategy()
        customer_storage_mock.find_customer.return_value = expected_customer
        customer_service = CustomerService(customer_storage_mock)

        # WHEN
        customer_service.remove_customer(self.customer_id)

        # THEN
        self.assertTrue(customer_storage_mock.delete_customer.assert_called_once)

        customer_to_remove = customer_storage_mock.delete_customer.call_args.args[0]
        self.assertTrue(eq(expected_customer, customer_to_remove))

    @patch('handbook.customer_service.StorageStrategy')
    def test_display_customer_data(self, MockStorageStrategy: Mock) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        customer_storage_mock = MockStorageStrategy()
        customer_storage_mock.list_of_customer.return_value = [expected_customer]
        customer_service = CustomerService(customer_storage_mock)

        # WHEN
        customer_service.display_customer_data([])

        # THEN
        self.assertTrue(customer_storage_mock.list_of_customer.assert_called_once)

    @patch('handbook.customer_service.StorageStrategy')
    def test_display_customer_data_ordered(self, MockStorageStrategy: Mock) -> None:
        # GIVEN
        expected_customer = Customer(self.customer_id,
                                     self.full_name,
                                     self.position,
                                     self.name_of_the_organization,
                                     self.email,
                                     self.phone
                                     )
        customer_storage_mock = MockStorageStrategy()
        customer_storage_mock.list_of_customer.return_value = [expected_customer]
        customer_service = CustomerService(customer_storage_mock)

        # WHEN
        list_options = ["full_name"]
        customer_service.display_customer_data(list_options)

        # THEN
        self.assertTrue(customer_storage_mock.list_of_customer.assert_called_once)

        params = customer_storage_mock.list_of_customer.call_args.args[0]
        self.assertEqual(params, list_options)


if __name__ == '__main__':
    unittest.main()
