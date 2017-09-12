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

import text

def launch_testserver():
    host = '127.0.0.1'
    port = 12345

    s = socket.socket()

    s.bind((host, port))

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
        c.close()
        print '\nExiting...'
        exit(0)
