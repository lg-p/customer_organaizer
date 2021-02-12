import unittest

from handbook.command_parser import Command, Parser


class TestCommand(unittest.TestCase):

    def test_get_by_value(self):
        # GIVEN
        command_name = 'insert'

        # WHEN
        result = Command.get_by_value(command_name)

        # THEN
        self.assertEqual(result, Command.INSERT)


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()

    def parse_command_insert(self):
        # GIVEN
        command = 'insert'
        arguments = '000000001,Ivanov Vasyl,developer,FGH,vasyl@mail.ru,79278763423'

        # WHEN
        self.parser.parse_command(command, arguments)

        # THEN
        self.assertEqual(len(self.parser.customer_service), 1)

    def parse_command_update(self):
        # GIVEN
        command = 'insert'
        arguments = '000000001,Ivanov Vasyl,developer,FGH,vasyl@mail.ru,79278763423'
        self.parser.parse_command(command, arguments)

        command_test = 'update'
        arguments_test = '000000001,Ivanov Vasyl,senior developer,FGH,vasyl@mail.ru,79273275285'

        # WHEN
        self.parser.parse_command(command_test, arguments_test)

        # THEN
        self.assertEqual(self.parser.customer_service[0].position, 'senior developer')

    def parse_command_delete(self):
        # GIVEN
        command = 'insert'
        arguments = '000000001,Ivanov Vasyl,developer,FGH,vasyl@mail.ru,79278763423'
        self.parser.parse_command(command, arguments)

        command_test = 'delete'
        arguments_test = '000000001'

        # WHEN
        self.parser.parse_command(command_test, arguments_test)

        # THEN
        self.assertEqual(len(self.parser.customer_service), 0)

    def parse_command_list(self):
        # GIVEN
        command = 'insert'
        arguments = '000000001,Ivanov Vasyl,developer,FGH,vasyl@mail.ru,79278763423'
        self.parser.parse_command(command, arguments)

        command_test = 'list'
        arguments_test = 'customer_id'

        # WHEN
        self.parser.parse_command(command_test, arguments_test)

        # THEN
        self.assertEqual(self.parser.customer_service[0].customer_id, '000000001')

    def parse_command_find(self):
        # GIVEN
        command = 'insert'
        arguments = '000000001,Ivanov Vasyl,developer,FGH,vasyl@mail.ru,79278763423'
        self.parser.parse_command(command, arguments)

        command_test = 'find'
        arguments_test = 'customer_id,000000001'

        # WHEN
        self.parser.parse_command(command_test, arguments_test)

        # THEN
        self.assertEqual(self.parser.customer_service[0].customer_id, '000000001')


if __name__ == "__main__":
    unittest.main()
