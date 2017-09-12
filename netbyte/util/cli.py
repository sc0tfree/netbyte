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
# netbyte.util.cli module
#

import argparse


def description():
    '''
    argparse description text
    '''
    return '''
Netbyte is a Netcat-style tool that facilitates probing proprietary TCP and UDP services.
It is lightweight, fully interactive and provides formatted output in both hexadecimal and ASCII.'''


def parse_arguments():
    '''
    Parse command line arguments

    Returns:
        argparse Namespace object
    '''
    parser = argparse.ArgumentParser(description=description(), formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('hostname', metavar='HOSTNAME', help='Host or IP to connect to')
    parser.add_argument('port', metavar='PORT', help='Connection port')
    parser.add_argument('-u', dest='udp', action="store_true", default=False, help='Use UDP instead of default TCP')

    if len(sys.argv) == 1:

        parser.print_help()

        exit(1)

    args = parser.parse_args()
    return args
