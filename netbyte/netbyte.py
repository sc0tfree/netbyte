#                __  __          __
#    ____  ___  / /_/ /_  __  __/ /____
#   / __ \/ _ \/ __/ __ \/ / / / __/ _ \
#  / / / /  __/ /_/ /_/ / /_/ / /_/  __/
# /_/ /_/\___/\__/_.___/\__, /\__/\___/
#                      /____/
#                       Author: sc0tfree
#                       Twitter: @sc0tfree
#                       Email: henry@sc0tfree.com

import util.cli as cli
import util.network as net
import util.testserver as ts


def main():
    '''
    Main function: Handles arguments, server:port connection and test server
    '''

    args = cli.parse_arguments()

    if args.testserver is not False:
        ts.launch_testserver(args.testserver)
    else:
        net.connect(args)