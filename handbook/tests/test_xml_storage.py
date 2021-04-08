import unittest
import os.path

from handbook.customer_service import XMLStorage, Customer


class TestXMLStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.path_file = "test_handbook.xml"
        self.xml_storage = XMLStorage(self.path_file)

    def tearDown(self) -> None:
        if os.path.exists(self.path_file):
            os.remove(self.path_file)

    def test_insert_customer(self) -> not None:
        # GIVEN
        arguments = "000000001,Ivanov Vasyl,developer,FGH,vasyl@mail.ru,79278763423".split(",")
        customer = Customer(*arguments)

        # WHEN
        self.xml_storage.insert_customer(customer)

        # THEN
        customer = self.xml_storage.find_customer("customer_id", "000000001")
        self.assertIsNotNone(customer)

    def test_find_customer(self) -> not None:
        # GIVEN
        arguments = "000000002,Ivanov Peter,manager,FGH,peter@mail.ru,79279826478".split(",")
        customer = Customer(*arguments)
        self.xml_storage.insert_customer(customer)

        # WHEN
        argument_name = "customer_id"
        argument_value = "000000002"
        customer = self.xml_storage.find_customer(argument_name, argument_value)

        # THEN
        self.assertIsNotNone(customer)

    def test_update_customer(self) -> True:
        # GIVEN)
        arguments = "000000003,Romanov Dmitriy,manager,FGH,dmitriy@mail.ru,79273987569".split(",")
        customer = Customer(*arguments)
        self.xml_storage.insert_customer(customer)

        # WHEN
        updatable_arguments = dict()
        updatable_arguments["position"] = "general manager"
        self.xml_storage.update_customer(customer, updatable_arguments)
        customer = self.xml_storage.find_customer("customer_id", "000000003")

        # THEN
        self.assertEqual(customer.position, "general manager")

    def test_delete_customer(self) -> None:
        # GIVEN
        arguments = "000000004,Green Alexandr,manager,FGH,alexandr@mail.ru,79056987458".split(",")
        customer = Customer(*arguments)
        self.xml_storage.insert_customer(customer)

        # WHEN
        self.xml_storage.delete_customer(customer)

        # THEN
        customer = self.xml_storage.find_customer("customer_id", "000000004")
        self.assertIsNone(customer)

    def test_get_everything(self) -> True:
        # GIVEN
        arguments = "000000004,Green Alexandr,manager,FGH,alexandr@mail.ru,79056987458".split(",")
        customer = Customer(*arguments)
        self.xml_storage.insert_customer(customer)

        arguments_sorted = ["position", "full_name"]

        # WHEN
        customers = self.xml_storage.list_of_customer(arguments_sorted)

        # THEN
        self.assertGreaterEqual(len(customers), 1)


if __name__ == "__main__":
    unittest.main()
