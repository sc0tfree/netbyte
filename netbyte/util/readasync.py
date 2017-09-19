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
# netbyte.util.readasync module
#

import re
from threading import Thread
from Queue import Queue
import output as out


def eval_expressions(string):
    p = re.compile('^\s*!!([\s\S]*)')
    m = p.match(string)
    if m:
        try:
            evaluated = eval(m.group(1), {'__builtins__':None}, {})
        except (SyntaxError, ValueError, TypeError, NameError):
            out.print_info('Incorrectly formatted statement. Please try again.')
            return ''
        return evaluated
    else:
        return string


class ReadAsync(object):
    '''
    ReadAsync starts a queue thread to accept stdin
    '''
    def __init__(self, blocking_function, *args):
        self.args = args

        self.read = blocking_function

        self.thread = Thread(target=self.enqueue)

        self.queue = Queue()

        self.thread.daemon = True

        self.thread.start()

    def enqueue(self):
        while True:
            buffer = self.read(*self.args)
            buffer_e = eval_expressions(buffer)
            self.queue.put(buffer_e)

    def dequeue(self):
        return self.queue.get_nowait()
