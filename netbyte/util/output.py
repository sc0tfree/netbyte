#                __  __          __
#    ____  ___  / /_/ /_  __  __/ /____
#   / __ \/ _ \/ __/ __ \/ / / / __/ _ \
#  / / / /  __/ /_/ /_/ / /_/ / /_/  __/
# /_/ /_/\___/\__/_.___/\__, /\__/\___/
#                      /____/
#                       Author: sc0tfree
#                       Twitter: @sc0tfree
#                       Email: henry@sc0tfree.com
#
# netbyte.util.output module
#

from colorama import Fore, Style


def print_info(string):
    '''
    Print string with info color configuration
    '''
    print(Fore.GREEN + Style.BRIGHT + string + Style.RESET_ALL)


def print_flat(string):
    '''
    Print string with no colors
    '''
    print(string)


def print_raw(string):
    '''
    Print string with raw text color configuration
    '''
    if string.isspace():
        # Add a space to show colors on a non-raw text line
        string = ' ' + string
    print(Fore.MAGENTA + Style.BRIGHT + string + Style.RESET_ALL)


def print_hex(string):
    '''
    Print string with hex color configuration
    '''
    print(Fore.BLUE + Style.BRIGHT + string + Style.RESET_ALL)


def print_error(string):
    '''
    Print string with error color configuration and exit with code 1
    '''
    print(Fore.RED + Style.BRIGHT + string + Style.RESET_ALL)
    exit(1)
