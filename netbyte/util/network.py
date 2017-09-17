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

import socket
import errno
import sys
import time
from Queue import Empty

import text
import output as out
from readasync import ReadAsync


def connect(args):
    '''
    Connects to server and port based on argparse namespace object
    '''
    if args.udp:
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connection.settimeout(2)

    address = (args.hostname, int(args.port))

    try:
        connection.connect(address)

    except socket.error:
        out.print_error("Could not establish connection to " + address[0] + ":" + str(address[1]))

    out.print_info("Connection Established")

    try:
        connection.setblocking(0)
        stdin = ReadAsync(sys.stdin.readline)

        while True:
            try:
                data = connection.recv(4096)
                if not data:
                    raise socket.error
                out.print_ascii(data)
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
