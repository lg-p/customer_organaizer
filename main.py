# import argparse

from handbook.command_parser import Parser, Command


def main():
    # parser = argparse.ArgumentParser(description='The program is designed to store, view and edit customer data')
    # parser.add_argument('path', type=str, help='XML file path')
    # args = parser.parse_args()
    parser = Parser()

    print("Please enter the command:")

    while True:
        commands = input().split(maxsplit=1)

        command = Command.get_by_value(commands[0])
        arguments = []
        if len(commands) > 1:
            arguments = commands[1].split(',')

        parser.parse_command(command, arguments)


if __name__ == '__main__':
    main()
