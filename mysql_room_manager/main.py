"""Main application entry point."""
import sys
import os
from mysql_room_manager.cli.controller import Controller

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    controller = Controller() 
    controller.run()

if __name__ == '__main__':
    main()