import argparse
from os import environ

from handbook.command_parser import ExitCommand, HelpCommand, InsertCommand, FindCommand, UpdateCommand, \
    DeleteCommand, ListCommand
from handbook.customer_service import CustomerException, CustomerService, StorageFactory
from handbook.validator import ValidateException

EXPECTED_COMMANDS = {
    'exit': ExitCommand,
    'help': HelpCommand,
    'insert': InsertCommand,
    'find': FindCommand,
    'update': UpdateCommand,
    'delete': DeleteCommand,
    'list': ListCommand,
}


def main():
    arg_parser = argparse.ArgumentParser(description='The program is designed to store, view and edit customer data')
    arg_parser.add_argument('--path', type=str, default=environ.get('path'), help='XML file path')
    arg_parser.add_argument('--db', type=str, default=environ.get('db'), help='database name')
    arg_parser.add_argument('--user', type=str, default=environ.get('user'), help='user name')
    arg_parser.add_argument('--password', type=str, default=environ.get('password'), help='password user')
    arg_parser.add_argument('--host', type=str, default=environ.get('host'), help='host')
    arg_parser.add_argument('--port', type=str, default=environ.get('port'), help='port')
    args = arg_parser.parse_args()

    storage = StorageFactory.get_storage(args)
    customer_service = CustomerService(storage)

    while True:
        input_command = input("Please enter the command:").split(maxsplit=1)

        if len(input_command) == 0:
            continue

        try:
            command = EXPECTED_COMMANDS[input_command[0]]()
            command.execute(customer_service)
        except KeyError:
            print("INVALID COMMAND!\n")
            EXPECTED_COMMANDS["help"]().execute(customer_service)
        except ValidateException as e:
            print(e)
        except CustomerException as e:
            print("ERROR:", e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
