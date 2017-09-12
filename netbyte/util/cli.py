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

import sys
import argparse
from .. import __version__ as VERSION


def description():
    '''
    argparse description text
    '''
    heading = 'Netbyte ' + VERSION + ' (by @sc0tfree)'
    body = '''
    Netbyte is a Netcat-style tool that facilitates probing proprietary TCP and UDP services.
    It is lightweight, fully interactive and provides formatted output in both hexadecimal and ASCII.
    '''
    return heading + body


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
    parser.add_argument('--testserver', nargs='?',  metavar='PORT', default=False, help='Launch test server [default port: 12345]')

    if len(sys.argv) == 1:

        parser.print_help()

        exit(1)

    if '--testserver' in sys.argv:
        testserver_parser = argparse.ArgumentParser()
        testserver_parser.add_argument('--testserver', nargs='?', type=int, const=12345)
        args = testserver_parser.parse_args()
    else:
        args = parser.parse_args()

    return args
