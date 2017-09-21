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
# netbyte.util.text module
#

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
