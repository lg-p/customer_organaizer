import os.path
import unittest

from handbook.xml_service import XMLService


class TestXMLFile(unittest.TestCase):
    def setUp(self) -> None:
        self.xml_service = XMLService()

    # def test_create_file(self):
    #     # GIVEN
    #     path_file = "handbook.xml"
    #
    #     # WHEN
    #     self.xml_file.create_file(path_file)
    #
    #     # THEN
    #     self.assertEqual("", "")

    def test_insert_customer(self):
        # GIVEN
        path_file = "../handbook.xml"
        if not os.path.exists(path_file):
            self.xml_service.create_file(path_file)
        arguments = '000000001,Ivanov Vasyl,developer,FGH,vasyl@mail.ru,79278763423'.split(',')

        # WHEN
        self.xml_service.insert_customer(path_file, arguments)

        # THEN
        self.assertEqual("", "")

    def test_find_customer(self):
        # GIVEN
        path_file = "../handbook.xml"
        if not os.path.exists(path_file):
            self.xml_service.create_file(path_file)
        arguments = '000000002,Ivanov Peter,manager,FGH,peter@mail.ru,79279826478'.split(',')
        self.xml_service.insert_customer(path_file, arguments)

        # WHEN
        argument_name = 'customer_id'
        argument_value = '000000002'
        customer = self.xml_service.find_customer(path_file, argument_name, argument_value)

        # THEN
        self.assertEqual(customer.customer_id, "000000002")

    def test_update_customer(self):
        # GIVEN
        path_file = "../handbook.xml"
        if not os.path.exists(path_file):
            self.xml_service.create_file(path_file)
        arguments = '000000003,Romanov Dmitriy,manager,FGH,dmitriy@mail.ru,79273987569'.split(',')
        self.xml_service.insert_customer(path_file, arguments)

        # WHEN
        arguments_new = '000000003,Romanov Dmitriy,general manager,FGH,dmitriy@mail.ru,79273987569'.split(',')
        self.xml_service.update_customer(path_file, arguments_new)
        customer = self.xml_service.find_customer(path_file, 'customer_id', '000000003')

        # THEN
        self.assertEqual(customer.position, "general manager")

    def test_delete_customer(self):
        # GIVEN
        path_file = "../handbook.xml"
        if not os.path.exists(path_file):
            self.xml_service.create_file(path_file)
        arguments = '000000004,Komarov Alexandr,manager,FGH,alexandr@mail.ru,79056987458'.split(',')
        self.xml_service.insert_customer(path_file, arguments)

        argument_value = '000000004'

        # WHEN
        self.xml_service.delete_customer(path_file, argument_value)

        # THEN
        self.assertEqual("", "")

    def test_get_everything(self):
        # GIVEN
        path_file = "../handbook.xml"
        if not os.path.exists(path_file):
            self.xml_service.create_file(path_file)
        arguments_sorted = ['position', 'full_name']

        # WHEN
        customers = self.xml_service.get_everything(path_file, arguments_sorted)
        print(*customers, sep='\n')

        # THEN
        self.assertEqual("", "")


if __name__ == "__main__":
    unittest.main()
