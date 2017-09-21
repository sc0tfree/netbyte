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
# netbyte.output module
#

from colorama import Fore, Style

use_colors = True

def print_info(string):
    '''
    Print string with info color configuration
    '''
    if use_colors:
        print(Fore.GREEN + Style.BRIGHT + string + Style.RESET_ALL)
    else:
        print(string)


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
    if use_colors:
        print(Fore.MAGENTA + Style.BRIGHT + string + Style.RESET_ALL)
    else:
        print string


def print_hex(string):
    '''
    Print string with hex color configuration
    '''
    if use_colors:
        print(Fore.BLUE + Style.BRIGHT + string + Style.RESET_ALL)
    else:
        print string


def print_error_and_exit(string):
    '''
    Print string with error color configuration and exit with code 1
    '''
    if use_colors:
        print(Fore.RED + Style.BRIGHT + string + Style.RESET_ALL)
    else:
        print(string)
    exit(1)
