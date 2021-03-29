import unittest

from handbook.validator import Validator


class TestValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = Validator()

    def test_validate_string_true(self) -> True:
        # GIVEN
        value = 'Validate'

        # WHEN
        valid_string = self.validator.validate_string(value)

        # THEN
        self.assertTrue(valid_string)

    def test_validate_string_false(self) -> False:
        # GIVEN
        value = '1231_+=!@#$%^&*()<>'

        # WHEN
        valid_string = self.validator.validate_string(value)

        # THEN
        self.assertFalse(valid_string)

    def test_validate_limited_length_string_true(self) -> True:
        # GIVEN
        value = '"COMPANY-3567"'

        # WHEN
        valid_string = self.validator.validate_limited_length_string(value)

        # THEN
        self.assertTrue(valid_string)

    def test_validate_number_true(self) -> True:
        # GIVEN
        value = '256469628'

        # WHEN
        valid_string = self.validator.validate_number(value)

        # THEN
        self.assertTrue(valid_string)

    def test_validate_number_false(self) -> False:
        # GIVEN
        value = '2564696_R'

        # WHEN
        valid_string = self.validator.validate_number(value)

        # THEN
        self.assertFalse(valid_string)

    def test_validate_email_true(self) -> True:
        # GIVEN
        value = 'my_mail@mail.ru'

        # WHEN
        valid_string = self.validator.validate_email(value)

        # THEN
        self.assertTrue(valid_string)

    def test_validate_email_false(self) -> False:
        # GIVEN
        value = 'my_mail65mail.ru'

        # WHEN
        valid_string = self.validator.validate_email(value)

        # THEN
        self.assertFalse(valid_string)

    def test_validate_phone_true(self) -> False:
        # GIVEN
        value = '79863452345'

        # WHEN
        valid_string = self.validator.validate_phone(value)

        # THEN
        self.assertTrue(valid_string)

    def test_validate_phone_len_false(self) -> False:
        # GIVEN
        value = '798634523'

        # WHEN
        valid_string = self.validator.validate_phone(value)

        # THEN
        self.assertFalse(valid_string)

    def test_validate_phone_false(self) -> False:
        # GIVEN
        value = '798634523_R'

        # WHEN
        valid_string = self.validator.validate_phone(value)

        # THEN
        self.assertFalse(valid_string)

    def test_validate_data_true(self) -> True:
        # GIVEN
        argument_name = 'customer_id'
        argument_value = '000000001'

        # WHEN
        result = self.validator.validate_data(argument_name, argument_value)

        # THEN
        self.assertTrue(result.isSuccess)

    def test_validate_data_false(self) -> False:
        # GIVEN
        argument_name = 'customer_id'
        argument_value = 'RE0000001'

        # WHEN
        result = self.validator.validate_data(argument_name, argument_value)

        # THEN
        self.assertFalse(result.isSuccess)

    def test_validate_data_for_list_true(self) -> True:
        # GIVEN
        arguments = ['customer_id']

        # WHEN
        result = self.validator.validate_data_for_list(arguments)

        # THEN
        self.assertTrue(result)

    def test_validate_data_for_list_false(self) -> False:
        # GIVEN
        arguments = ['customer']

        # WHEN
        result = self.validator.validate_data_for_list(arguments)

        # THEN
        self.assertFalse(result.isSuccess)


if __name__ == '__main__':
    unittest.main()
