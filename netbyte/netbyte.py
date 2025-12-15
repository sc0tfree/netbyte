#                __  __          __
#    ____  ___  / /_/ /_  __  __/ /____
#   / __ \/ _ \/ __/ __ \/ / / / __/ _ \
#  / / / /  __/ /_/ /_/ / /_/ / /_/  __/
# /_/ /_/\___/\__/_.___/\__, /\__/\___/
#                      /____/
#                       Author: sc0tfree
#                       Twitter: @sc0tfree
#                       Email: henry@sc0tfree.com

import socket
import errno
import argparse
import sys
import time
from colorama import Fore, Style, init as colorama_init
from threading import Thread
from queue import Queue, Empty

from netbyte.core import to_hex, parse_hex_bytes


def is_symbol(character):
    '''
    Checks to see if a character is a symbol.

    Returns:
        bool: True if character is symbol
    '''
    symbols = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
    if character not in symbols:
        return False
    else:
        return True


def print_ascii(data):
    '''
    Print string with ASCII color configuration
    '''
    if isinstance(data, (bytes, bytearray)):
        text = bytes(data).decode("utf-8", errors="replace")
    else:
        text = str(data)

    if text.isspace():
        # Add a space to show colors on a non-ASCII line
        text = ' ' + text
    print(Fore.MAGENTA + Style.BRIGHT + text + Style.RESET_ALL)


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
    raise SystemExit(1)


class ReadAsync(object):
    '''
    ReadAsync starts a queue thread to accept stdin
    '''
    def __init__(self, blocking_function, *args):
        self.args = args

        self.read = blocking_function

        self.thread = Thread(target=self.enqueue)

        self.queue = Queue()

        self.thread.daemon = True

        self.thread.start()

    def enqueue(self):
        while True:
            buffer = self.read(*self.args)
            self.queue.put(buffer)

    def dequeue(self):
        return self.queue.get_nowait()


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
    parser.add_argument(
        '--send-hex',
        dest='send_hex',
        action='store_true',
        default=False,
        help='Interpret stdin as hex bytes before sending (e.g. \"DE AD BE EF\" or \"0xDE,0xAD\")',
    )

    if len(sys.argv) == 1:

        parser.print_help()

        raise SystemExit(1)

    args = parser.parse_args()
    return args


def main():
    '''
    Main function: Connects to host/port and spawns ReadAsync
    '''

    colorama_init()
    args = parse_arguments()

    if args.udp:
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connection.settimeout(2)

    address = (args.hostname, int(args.port))

    try:
        connection.connect(address)
    except OSError:
        print_error("Could not establish connection to " + address[0] + ":" + str(address[1]))

    print(Fore.GREEN + Style.BRIGHT + "Connection established" + Style.RESET_ALL)

    try:
        connection.setblocking(0)
        stdin = ReadAsync(sys.stdin.readline)

        while True:
            try:
                data = connection.recv(4096)
                if not data:
                    raise OSError
                print_ascii(data)
                print_hex(to_hex(data))
            except OSError as e:
                if getattr(e, "errno", None) not in (errno.EWOULDBLOCK, errno.EAGAIN):
                    raise
            try:
                outbound = stdin.dequeue()
                if outbound == "":
                    # EOF on stdin
                    raise KeyboardInterrupt

                if args.send_hex:
                    try:
                        outbound_bytes = parse_hex_bytes(outbound.strip())
                    except ValueError as e:
                        print_error(f"Invalid hex input: {e}")
                    connection.send(outbound_bytes)
                else:
                    if isinstance(outbound, str):
                        outbound = outbound.encode("utf-8")
                    connection.send(outbound)
            except Empty:
                time.sleep(0.1)
            except (BlockingIOError, InterruptedError):
                time.sleep(0.01)

    except KeyboardInterrupt:
        connection.close()
        print_error("\nExiting...")
    except OSError:
        print_error("Connection closed")