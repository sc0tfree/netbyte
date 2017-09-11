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


def to_hex(string):
    '''
    Converts string to formatted hex and ASCII reference values

    Returns:
        str: Formatted hex & ASCII reference
    '''

    results = []

    new_line = True

    for character in string:

        # Convert ASCII to unicode
        unicode_value = ord(character)

        # Convert unicode to hex
        hex_value = hex(unicode_value).replace('0x', '')

        # Add a preceding 0
        if len(hex_value) == 1:
            hex_value = '0' + hex_value

        # Make upper case
        hex_value = hex_value.upper()

        # Add reference ASCII for readability
        if character.isalpha() or character.isdigit() or is_symbol(character):
            hex_value = hex_value + '(' + character + ')'

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

    full_hex = ''
    for result in results:
        full_hex += result

    return full_hex
