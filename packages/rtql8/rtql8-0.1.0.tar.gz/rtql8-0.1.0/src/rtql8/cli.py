"""Command-line interface for the rtql8 package."""

import argparse
from . import Cron

__version__ = "1.1"

def main():
    """Parse the command-line arguments and describe the given cron expression."""

    parser = argparse.ArgumentParser(description=f"rtql8 v{__version__} - Describe a given cron expression")
    # add expression argument
    parser.add_argument(
        "-e",
        "--expr",
        required=True,
        help="Cron expression to parse",
    )
    # add logo argument
    parser.add_argument(
        "-l",
        "--logo",
        action="store_true",
        help="Display logo",
    )
    # add version argument
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"rtql8 v{__version__}", 
    )
    args = parser.parse_args()

    # print application branding
    if args.logo:
        logo()


    cron = Cron(args.expr)
    # print the description of the cron expression
    print(f"[ {args.expr} ] = {cron.description}")

    # convert datetime object to string
    # print(f"Next run: {cron.next_run.strftime("%Y-%m-%d %H:%M:%S")}")

def logo():
    """Print the application branding."""
    print(" ")
    print("⢰⣶⣶⣶⣶⣶⣦⣄⠀⣶⣶⣶⣶⣶⣶⣦⠀⣠⣶⣶⣶⣶⣶⣄⡀⠀⣶⣶⣶⡆⠀⠀⠀⣤⣶⣶⣶⣶⣤⠀")
    print("⢸⣿⣿⣿⡿⢿⣿⣿⣧⠿⢿⣿⣿⣿⠿⢿⣾⣿⣿⣿⠿⢿⣿⣿⣷⡀⣿⣿⣿⡇⠀⠀⠸⣿⣿⣏⣹⣿⣿⠂")
    print("⢸⣿⣿⣿⣶⣿⣿⣿⠃⠀⢸⣿⣿⣿⠀⢸⣿⣿⣿⣀⢠⣦⣿⣿⣿⡇⣿⣿⣿⣇⣀⡀⣰⣿⣿⡿⢿⣿⣿⣦")
    print("⢸⣿⣿⣿⣿⣿⣿⣿⣶⠀⢸⣿⣿⣿⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⢿⣿⣿⣷⣾⣿⣿⡟")
    print("⠸⠿⠿⠟⠈⠙⠻⠿⠟⠀⠘⠿⠿⠟⠀⠀⠀⠉⠛⠿⠿⠿⠛⠿⠿⠿⠻⠿⠿⠿⠿⠟⠀⠙⠿⠿⠿⠟⠋⠀")
    print(f"          a cron expression parser v{__version__}\n")


if __name__ == "__main__":
    main()
