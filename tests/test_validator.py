import unittest

from handbook.validator import Validator


class TestValidator(unittest.TestCase):

    def setUp(self) -> None:
        self.validator = Validator()

    def test_validate_string_true(self):
        # GIVEN
        value = 'Validate'

        # WHEN
        valid_string = self.validator.validate_string(value)

        # THEN
        self.assertEqual(valid_string, True)

    def test_validate_string_false(self):
        # GIVEN
        value = '1231_+=!@#$%^&*()<>'

        # WHEN
        valid_string = self.validator.validate_string(value)

        # THEN
        self.assertEqual(valid_string, False)

    def test_validate_limited_length_string_true(self):
        # GIVEN
        value = '"COMPANY-3567"'

        # WHEN
        valid_string = self.validator.validate_limited_length_string(value)

        # THEN
        self.assertEqual(valid_string, True)

    def test_validate_number_true(self):
        # GIVEN
        value = '256469628'

        # WHEN
        valid_string = self.validator.validate_number(value)

        # THEN
        self.assertEqual(valid_string, True)

    def test_validate_number_false(self):
        # GIVEN
        value = '2564696_R'

        # WHEN
        valid_string = self.validator.validate_number(value)

        # THEN
        self.assertEqual(valid_string, False)

    def test_validate_email_true(self):
        # GIVEN
        value = 'my_mail@mail.ru'

        # WHEN
        valid_string = self.validator.validate_email(value)

        # THEN
        self.assertEqual(valid_string, True)

    def test_validate_email_false(self):
        # GIVEN
        value = 'my_mail65mail.ru'

        # WHEN
        valid_string = self.validator.validate_email(value)

        # THEN
        self.assertEqual(valid_string, False)

    def test_validate_phone_true(self):
        # GIVEN
        value = '79863452345'

        # WHEN
        valid_string = self.validator.validate_phone(value)

        # THEN
        self.assertEqual(valid_string, True)

    def test_validate_phone_len_false(self):
        # GIVEN
        value = '798634523'

        # WHEN
        valid_string = self.validator.validate_phone(value)

        # THEN
        self.assertEqual(valid_string, False)

    def test_validate_phone_false(self):
        # GIVEN
        value = '798634523_R'

        # WHEN
        valid_string = self.validator.validate_phone(value)

        # THEN
        self.assertEqual(valid_string, False)

    def test_validate_data_true(self):
        # GIVEN
        arguments = dict()
        arguments['customer_id'] = '000000001'

        # WHEN
        result = self.validator.validate_data(arguments)

        # THEN
        self.assertEqual(result, True)

    def test_validate_data_false(self):
        # GIVEN
        arguments = dict()
        arguments['customer_id'] = 'RE0000001'

        # WHEN
        result = self.validator.validate_data(arguments)

        # THEN
        self.assertEqual(result, False)

    def test_validate_data_for_list_true(self):
        # GIVEN
        arguments = ['customer_id']

        # WHEN
        result = self.validator.validate_data_for_list(arguments)

        # THEN
        self.assertEqual(result, True)

    def test_validate_data_for_list_false(self):
        # GIVEN
        arguments = ['customer']

        # WHEN
        result = self.validator.validate_data_for_list(arguments)

        # THEN
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
