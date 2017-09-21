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
# netbyte.network module
#

import errno
import socket
import sys
import time
from Queue import Empty

import output as out
from readasync import ReadAsync


def to_hex(string):
    '''
    Converts byte string to formatted hex and ASCII reference values

    Returns:
        str: Formatted hex & ASCII reference
    '''

    symbols = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"

    results = []

    new_line = True

    for byte in string:
        # Convert to upper-case hexadecimal with two places
        hex_value = '%02X' % ord(byte)

        # Add reference ASCII for readability
        if byte.isalpha() or byte.isdigit() or byte in symbols:
            hex_value = hex_value + '(' + byte + ')'

        # Add a space in between hex values (not to a new line)
        if not new_line:
            hex_value = ' ' + hex_value

        # Add a newline for readability (corresponding to ASCII)
        if '0A' in hex_value and not string.isspace():
            hex_value = hex_value + '(\\n)\n'
            # Next line will be a newline
            new_line = True
        else:
            new_line = False

        results.append(hex_value)

    return ''.join(results)


def connect(args):
    '''
    Connects to server and port based on argparse namespace object
    '''
    if args.udp:
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if args.no_colors:
        out.use_colors = False

    connection.settimeout(2)
    
    address = (args.hostname, args.port)

    try:
        connection.connect(address)

    except socket.error:
        out.print_error_and_exit('Could not establish connection to %s:%d' % address)
    except OverflowError:
        out.print_error_and_exit('Port must be between 1 and 65535')

    out.print_info('Connection Established')

    try:
        connection.setblocking(0)
        stdin = ReadAsync(sys.stdin.readline)

        while True:
            try:
                data = connection.recv(4096)
                if not data:
                    raise socket.error
                out.print_raw(data)
                out.print_hex(to_hex(data))
            except socket.error, e:
                if e.errno != errno.EWOULDBLOCK:
                    raise
            try:
                connection.send(stdin.dequeue())
            except Empty:
                time.sleep(0.1)

    except KeyboardInterrupt:
        connection.close()
        out.print_error_and_exit('\nExiting...')
    except socket.error:
        out.print_error_and_exit('Connection closed')
