import argparse

from handbook.command_parser import ExitCommand, HelpCommand, InsertCommand, FindCommand, UpdateCommand, \
    DeleteCommand, ListCommand
from handbook.customer_service import CustomerService


def main():
    arg_parser = argparse.ArgumentParser(description='The program is designed to store, view and edit customer data')
    arg_parser.add_argument('--path', type=str, help='XML file path')
    args = arg_parser.parse_args()

    storage = CustomerService.storage(args.path)
    customer_service = CustomerService(storage())

    expected_commands = {
        'exit': ExitCommand(),
        'help': HelpCommand(),
        'insert': InsertCommand(),
        'find': FindCommand(),
        'update': UpdateCommand(),
        'delete': DeleteCommand(),
        'list': ListCommand(),
    }

    while True:
        input_command = input("Please enter the command:").split(maxsplit=1)
        command = expected_commands[input_command[0]]
        command.execute(customer_service)


if __name__ == '__main__':
    main()
