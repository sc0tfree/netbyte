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

import socket
import text
import output as out

def launch_testserver(port):
    '''
    Launches test server on infinite loop until interrupt
    '''
    host = '127.0.0.1'

    out.print_info('Starting test server on 127.0.0.1:' + str(port))

    s = socket.socket()

    try:
        s.bind((host, port))
    except socket.error as e:
        if e.errno == 13:
            out.print_error("Permission denied: try again as superuser")
        elif e.errno == 48:
            out.print_error("Port is already in use")
    except OverflowError:
            out.print_error("Port must be between 1 and 65535")

    s.listen(5)

    try:

        while True:

            c, addr = s.accept()

            print 'Connection established from', addr[0], ':', addr[1]

            c.send('Hello from Test Server\n')

            # Echo Test
            c.send('Echo Test - enter string:')
            data = c.recv(1024)
            print 'Echo Test - received: ', data
            c.send('Echo Test - received: ' + data + '\n')

            # Hex Test
            c.send('Hex Test - enter length:')
            data = c.recv(1024)

            try:
                hex_length = int(data)
            except ValueError:
                c.send('You must enter a number. Defaulting to 10.\n')
                hex_length = 10

            hex_string = text.generate_random_hex(hex_length)
            c.send('Sending hex string...\n\n')
            print 'Hex Test - sending: ', hex_string
            c.send(hex_string)

            c.close()
            print 'Closed connection to ', addr[0], ':', addr[1]

    except KeyboardInterrupt:
        try:
            c.close()
        except NameError:
            pass
        out.print_error('\nExiting...')
