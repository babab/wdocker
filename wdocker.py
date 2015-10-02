# Copyright (c) 2015  Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import collections
import os
import string
import subprocess
import sys

__docformat__ = 'restructuredtext'
__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2015  Benjamin Althues"
__version_info__ = (0, 2, 0, 'beta', 0)
__version__ = '0.2.0'

DOCKERFILE = 'Dockerfile'


class ParserError(Exception):
    '''Raised when there are (syntax) errors parsing the Dockerfile'''


class Parser:
    file_exists = None
    variables = {}
    commands = {}
    commands_raw = {}
    lineno = 0

    def __init__(self):
        self.file_exists = True
        self.variables = collections.OrderedDict()
        self.commands = collections.OrderedDict()
        self.commands_raw = collections.OrderedDict()

        if not os.path.exists(DOCKERFILE):
            self.file_exists = False
            raise ParserError('{} does not exist'.format(DOCKERFILE))
        with open(DOCKERFILE) as f:
            self._parseFile(f)

    def _parseFile(self, fh):
        for line in fh:
            self.lineno += 1
            if line.startswith('#wd#'):
                self._parseDirective(line)
                self._expandVariables()

    def _parseDirective(self, line):
        new = line[4:].split()
        if new[0].endswith(':'):
            self.commands_raw[new[0][:-1]] = ' '.join(new[1:])
        elif new[1] == '=':
            self.variables[new[0]] = ' '.join(new[2:])

    def _expandVariables(self):
        fmt = string.Formatter()
        for var, value in self.variables.items():
            self.variables[var] = fmt.vformat(value, [], self.variables)
        try:
            for command, value in self.commands_raw.items():
                self.commands[command] = fmt.vformat(value, [], self.variables)
        except KeyError as variable:
            raise ParserError('line {}: variable {} is not defined)'.format(
                self.lineno, variable
            ))


class WDocker:
    def __init__(self, args=sys.argv[1:]):
        self.args = args
        self.error = None
        try:
            self.parser = Parser()
        except ParserError as error:
            self.parser = None
            self.error = 'when parsing Dockerfile: {}'.format(error)

    def run(self):
        # Internal commands that do not need a Dockerfile ####################
        # handle -h, -help, --help, -?
        if self.args and self.args[0] in ('-h', '-help', '--help'):
            self._usage(help=True)
            return 0

        # show parser errors if there are any and exit with exit code 2
        if self.error:
            self._usage(self.error)
            return 2

        # show usage when wdocker is run without arguments
        if not self.args:
            self._usage()
            return 0

        # handle -version
        if self.args[0] == '-version':
            print('wdocker {}'.format(__version__))
            return 0

        # Internal commands that do not need a Dockerfile ####################
        # handle -print-var
        if self.args[0].startswith('-print-var'):
            if len(self.args) > 1:
                return self._printVar(self.args[1])
            self._usage('you must supply a variable name')
            return 1

        # handle regular commands
        if self.args[0] in self.parser.commands.keys():
            return self._call(self.args[0])

        # at this point, the argument is not found
        if self.args[0].startswith('-'):
            self._usage('internal command "{}" does not exist'
                        .format(self.args[0]))
        else:
            self._usage('command "{}" not found in Dockerfile'
                        .format(self.args[0]))
        return 1

    def _printVar(self, arg):
        if arg in self.parser.variables.keys():
            print(self.parser.variables[arg])
            return 0
        self._usage('variable {} does not exist'.format(arg))
        return 3

    def _call(self, arg):
        command = self.parser.commands[arg]
        print(':: ' + command)
        subprocess.call(command, shell=True)
        return 0

    def _usage(self, error='', help=False):
        if error:
            print('Error: {}\n'.format(error))
        print('Usage: wdocker [<command> | -help]')
        if help:
            print('\nInternal commands:')
            print('  -help, -h, --help      show full usage info and vars')
            print('  -version               show version info')
            print('  -print-var <variable>  print value of <variable>')

            if self.parser:
                if self.parser.variables:
                    print('\nVariables:')
                    for k, v in self.parser.variables.items():
                        print('  {:9} = {}'.format(k, v))
                    else:
                        print('\nVariables: No variables defined in '
                              'Dockerfile (yet)')

        if self.parser:
            if self.parser.commands:
                print('\nCommands:')
                for k, v in self.parser.commands.items():
                    print('  {:10}{}'.format(k, v))
            else:
                print('\nCommands: No commands defined in Dockerfile (yet)')

if __name__ == '__main__':
    sys.exit(WDocker().run())
