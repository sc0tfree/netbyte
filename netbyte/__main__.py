#                __  __          __
#    ____  ___  / /_/ /_  __  __/ /____
#   / __ \/ _ \/ __/ __ \/ / / / __/ _ \
#  / / / /  __/ /_/ /_/ / /_/ / /_/  __/
# /_/ /_/\___/\__/_.___/\__, /\__/\___/
#                      /____/
#                       Author: sc0tfree
#                       Twitter: @sc0tfree
#                       Email: henry@sc0tfree.com

import sys
import argparse

import network
import testserver
from . import __version__ as VERSION


def description():
    '''
    argparse description text
    '''
    heading = 'Netbyte v%s (by sc0tfree)' % VERSION
    body = '''
    Netbyte is a Netcat-style tool that facilitates manual probing, fuzzing and
    exploitation of TCP and UDP services. It is lightweight, fully interactive
    and supports input and output in both plain text and hexadecimal.'''
    return heading + body


def parse_arguments():
    '''
    Parse command line arguments

    Returns:
        argparse Namespace object
    '''
    parser = argparse.ArgumentParser(description=description(), formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('hostname', metavar='HOSTNAME', help='Host or IP to connect to')
    parser.add_argument('port', metavar='PORT', type=int, help='Connection port')
    parser.add_argument('-u', dest='udp', action='store_true', default=False, help='Use UDP instead of default TCP')
    parser.add_argument('--testserver', nargs='?',  metavar='PORT', default=False, help='Launch test server [default port: 12345]')
    parser.add_argument('--no-colors', action='store_true', default=False, help='Do not use colors in the output')

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


def main():
    '''
    Main function: Handles arguments, server:port connection and test server
    '''

    args = parse_arguments()

    if args.testserver is not False:
        testserver.launch_testserver(args.testserver)
    else:
        net.connect(args)

if __name__ == '__main__':
    main()
