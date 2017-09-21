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
# netbyte.util.network module
#

import errno
import socket
import sys
import time
from Queue import Empty

import output as out
import text
from readasync import ReadAsync


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
        out.print_error('Could not establish connection to %s:%d' % address)
    except OverflowError:
        out.print_error('Port must be between 1 and 65535')

    out.print_info("Connection Established")

    try:
        connection.setblocking(0)
        stdin = ReadAsync(sys.stdin.readline)

        while True:
            try:
                data = connection.recv(4096)
                if not data:
                    raise socket.error
                out.print_raw(data)
                out.print_hex(text.to_hex(data))
            except socket.error, e:
                if e.errno != errno.EWOULDBLOCK:
                    raise
            try:
                connection.send(stdin.dequeue())
            except Empty:
                time.sleep(0.1)

    except KeyboardInterrupt:
        connection.close()
        out.print_error("\nExiting...")
    except socket.error:
        out.print_error("Connection closed")
