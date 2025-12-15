#!/usr/bin/env python3

# Author: sc0tfree
# Twitter: @sc0tfree
# Email: henry@sc0tfree.com

import os
import socket


def generate_random_hex(length):
    '''
    Generates a hex string of arbitrary length - 1, ending in a newline.
    '''
    if length <= 0:
        return b""
    hex_bytes = os.urandom(max(0, length - 1))
    hex_bytes += b"\x0a"
    return hex_bytes


host = '127.0.0.1'
port = 12345

s = socket.socket()

s.bind((host, port))

s.listen(5)

try:

    while True:

        c, addr = s.accept()

        print('Connection established from', addr[0], ':', addr[1])

        c.send(b'Hello from Test Server\n')

        # Echo Test
        c.send(b'Echo Test - enter string:')
        data = c.recv(1024)
        print('Echo Test - received: ', data)
        c.send(b'Echo Test - received: ' + data + b'\n')

        # Hex Test
        c.send(b'Hex Test - enter length:')
        data = c.recv(1024)

        try:
            hex_length = int(data.strip() or b"0")
        except ValueError:
            c.send(b'You must enter a number. Defaulting to 10.\n')
            hex_length = 10

        hex_string = generate_random_hex(hex_length)
        c.send(b'Sending hex string...\n\n')
        print('Hex Test - sending: ', hex_string)
        c.send(hex_string)

        c.close()
        print('Closed connection to ', addr[0], ':', addr[1])

except KeyboardInterrupt:
    c.close()
    print('\nExiting...')
    raise SystemExit(0)
