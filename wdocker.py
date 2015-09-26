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
import shlex
import string
import subprocess
import sys

__docformat__ = 'restructuredtext'
__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2015  Benjamin Althues"
__version_info__ = (0, 1, 0, 'alpha', 0)
__version__ = '0.1.0'

DOCKERFILE = 'Dockerfile'


class Parser:
    file_exists = None
    variables = {}
    commands = {}
    commands_raw = {}

    def __init__(self):
        self.file_exists = True
        self.variables = collections.OrderedDict()
        self.commands = collections.OrderedDict()
        self.commands_raw = collections.OrderedDict()

        if not os.path.exists(DOCKERFILE):
            self.file_exists = False
            return
        with open(DOCKERFILE) as f:
            self._parseFile(f)
        self._expandVariables()

    def _parseFile(self, fh):
        for line in fh:
            if line.startswith('#wd#'):
                self._parseDirective(line)

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
        for command, value in self.commands_raw.items():
            self.commands[command] = fmt.vformat(value, [], self.variables)


class WDocker:
    def __init__(self, args=sys.argv[1:]):
        self.parser = Parser()
        self.args = args

    def run(self):
        if not self.parser.file_exists:
            self._usage('no Dockerfile found in current directory')
            return 1

        # show usage when wdocker is run without arguments
        if not self.args:
            self._usage()
            return 0

        # handle -h, -help, --help, -?
        if self.args[0] in ('-h', '-help', '--help'):
            self._usage(help=True)
            return 0

        # handle -print-var
        if self.args[0].startswith('-print-var'):
            if len(self.args) > 1:
                return self._printVar(self.args[1])
            self._usage('you must supply a variable name')
            return 2

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
        return 2

    def _printVar(self, arg):
        if arg in self.parser.variables.keys():
            print(self.parser.variables[arg])
            return 0
        self._usage('variable {} does not exist'.format(arg))
        return 3

    def _call(self, arg):
        commands = self.parser.commands[arg].split(';;')
        for cmd in commands:
            print(':: ' + cmd)
            subprocess.call(shlex.split(cmd))
        return 0

    def _usage(self, error='', help=False):
        print('Usage: wdocker [<command> | -help]')
        if error:
            print('\nError: {}'.format(error))
        if help:
            print('\nInternal commands:')
            print('  -help, -h, --help      show full usage info and vars')
            print('  -print-var <variable>  print value of <variable>')
            if self.parser.variables:
                print('\nVariables:')
                for k, v in self.parser.variables.items():
                    print('  {:9} = {}'.format(k, v))
            else:
                print('\nVariables: No variables defined in Dockerfile (yet)')

        if self.parser.commands:
            print('\nCommands:')
            for k, v in self.parser.commands.items():
                print('  {:10}{}'.format(k, v))
        else:
            print('\nCommands: No commands defined in Dockerfile (yet)')

if __name__ == '__main__':
    sys.exit(WDocker().run())
