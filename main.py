# import argparse

from handbook.command_parser import Parser, Command


def main():
    # parser = argparse.ArgumentParser(description='The program is designed to store, view and edit customer data')
    # parser.add_argument('path', type=str, help='XML file path')
    # args = parser.parse_args()
    parser = Parser()

    while True:
        commands = input().split()
        command = Command.get_by_value(commands[0])
        parser.parse_command(command, commands[1:])


if __name__ == '__main__':
    main()
