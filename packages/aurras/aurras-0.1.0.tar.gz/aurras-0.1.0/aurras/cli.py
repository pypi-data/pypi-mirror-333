"""
Command Line Interface

This module provides the command-line interface for the Aurras music player.
"""

import sys
from pathlib import Path

from .utils.decorators import handle_exceptions
from .ui.input_handler import HandleUserInput


class AurrasApp:
    """
    Main Aurras application class for the command-line interface.
    
    This class handles the main application loop and user input.
    """
    
    def __init__(self):
        """Initialize the AurrasApp class."""
        self.handle_input = HandleUserInput()
        
    @handle_exceptions
    def run(self):
        """Run the Aurras application."""
        print("Welcome to Aurras Music Player!")
        print("Type '?' followed by a feature name for help or start typing to search for a song.")
        
        try:
            while True:
                self.handle_input.handle_user_input()
        except KeyboardInterrupt:
            print("\nThanks for using Aurras!")
            sys.exit(0)


def main():
    """Main entry point for the Aurras application."""
    app = AurrasApp()
    app.run()


if __name__ == "__main__":
    main()
