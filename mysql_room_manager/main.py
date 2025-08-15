import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mysql_room_manager.cli.cli_controller import CLIController


def main():
    controller = CLIController()
    controller.run()


if __name__ == '__main__':
    main()
