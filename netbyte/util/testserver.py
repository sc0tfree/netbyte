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
# netbyte.util.testserver module
#

import re
import errno
import socket
import text
import output as out
from .. import __version__ as VERSION


class DisconnectedError(Exception):
    '''
    This indicates that the connection has been closed before completion of
    the tests.
    '''
    pass


end_pattern = re.compile('^\s*end\s*', re.IGNORECASE)


def handle_connection(connection, addr):
    '''
    A client has connected. Run through the tests and then disconnect.
    '''
    connection.send("Netbyte Test Server " + VERSION + "\n")

    def run_test(test_name, prompt, data_handler, initial_message=""):
        '''
        Runs a test repeatedly until the client ends it

        test_name: This is displayed as the test name
        prompt: This prompt string is sent for each test loop
        data_handler: A function to call on each line received from the client
        initial_message: This is used to pass on a remaining message from a
            previous call to run_test

        returns: Any remaining message recieved after the test is ended, or ""
        '''
        out.print_flat(test_name + ":")
        connection.send(test_name + ":\nType 'end' to exit\n")
        messages = []
        remaining_message = ""

        done = False
        while not done:
            if prompt:
                connection.send(prompt)

            if initial_message:
                message = initial_message
                initial_message = ""
            else:
                message = connection.recv(4096)

            if message:
                messages.append(message)
            else:
                raise DisconnectedError()

            if "\n" in message:
                # Consume the message line by line
                start_i = 0
                end_i = message.find("\n")
                while end_i != -1 and not done:
                    line = message[start_i: end_i]
                    if end_pattern.match(line):
                        done = True
                    else:
                        data_handler(line)

                    start_i = end_i + 1
                    end_i = message.find("\n", start_i)

                if start_i < len(message) - 1:
                    if done:
                        remaining_message = message[start_i:]
                    else:
                        messages = [message[start_i:]]

        return remaining_message

    def echo_handler(line):
        '''
        Receives a string, sends it back
        '''
        out.print_flat("Received: " + line.rstrip())
        connection.send(line + "\n")

    def hex_handler(line):
        '''
        Receives a number, sends back that number of random bytes
        '''
        try:
            hex_length = int(line)
            if hex_length <= 0:
                raise ValueError
        except ValueError:
            connection.send("You must enter a number larger than 0. Defaulting to 10.\n")
            hex_length = 10
        hex_string = text.generate_random_hex(hex_length)
        out.print_flat("Sending: " + hex_string)
        connection.send(hex_string)

    def byte_count_handler(line):
        '''
        Recieves a string, sends back the number of bytes in the string
        '''
        size = len(line)
        response = "Received %d bytes." % size
        out.print_flat(response)
        connection.send(response + "\n")

    remaining_msg = run_test("Echo Test", "", echo_handler)
    remaining_msg = run_test("Hex Test", "Number of bytes to send:",
                             hex_handler, remaining_msg)
    remaining_msg = run_test("Byte Count Test", "Bytes to count:",
                             byte_count_handler, remaining_msg)

    if remaining_msg:
        info = "Received unexpected data after all tests ended:" + remaining_msg
        out.print_info(info)
        connection.send(info)

    connection.send("Closing connection to test server\n")
    connection.close()
    out.print_info("Closed connection to " + str(addr[0]) + ':' + str(addr[1]))


def launch_testserver(port):
    '''
    Launches test server on infinite loop until interrupt
    '''
    host = '127.0.0.1'

    out.print_info("Starting test server on %s:%d" % (host, port))

    s = socket.socket()

    # allow quick restarts of the server
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((host, port))
    except socket.error as e:
        if e.errno == errno.EACCES:
            out.print_error("Permission denied: try again as superuser")
        elif e.errno == errno.EADDRINUSE:
            out.print_error("Port is already in use")
    except OverflowError:
        out.print_error("Port must be between 1 and 65535")

    s.listen(5)

    try:
        while True:
            try:
                c, addr = s.accept()
                out.print_info("Connection established from %s:%d" % addr)
                handle_connection(c, addr)

            except socket.error as e:
                if e.errno == errno.EPIPE:
                    out.print_info("Connection closed by user.")
                else:
                    out.print_info("Socket error: %s" % errno.errorcode[e.errno])

            except DisconnectedError:
                out.print_info("Connection closed.")
                c.close()

    except KeyboardInterrupt:
        s.close()
        out.print_error("\nExiting...")
