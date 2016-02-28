# Copyright (c) 2015-2016 Benjamin Althues <benjamin@althu.es>
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

try:
    from colors import green, magenta
except ImportError:
    def green(x):
        return x

    def magenta(x):
        return x

__docformat__ = 'restructuredtext'
__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2015-2016  Benjamin Althues"
__version_info__ = (0, 2, 0, 'beta', 0)
__version__ = '0.2.0'


def paddedColoredOutput(string, maxlen, color2=False):
    '''Fill string with spaces up to maxlen characters

    This is a workaround for setting padding using python str.format
    e.g. ``{:{padding}}`` which does not work properly when outputting
    ANSI colors
    '''
    div = maxlen - len(string)
    if sys.stdout.isatty():
        if color2:
            return '{}{}'.format(magenta(string), ' ' * div)
        return '{}{}'.format(green(string), ' ' * div)
    return '{}{}'.format(string, ' ' * div)


class ParserError(Exception):
    '''Raised when there are (syntax) errors parsing the Dockerfile'''


class Parser:
    '''Parses Dockerfile and finds variables and commands

    parse() is the only 'public' method. It tries file locations for
    `self.DOCKERFILE` and further completes parsing by calling private
    methods.
    '''

    DOCKERFILE = 'Dockerfile'
    '''The name of the file that must be parsed'''

    variables = {}
    '''OrderedDict of variables'''

    commands = {}
    '''OrderedDict of commands (expanded with variables)'''

    commands_raw = {}
    '''OrderedDict of raw commands'''

    lineno = 0
    '''The line number, used for printing helpful error messages'''

    path = None
    '''The path where the Dockerfile is found'''

    def __init__(self):
        '''Prepare OrderedDict's for variables and commands'''
        self.variables = collections.OrderedDict()
        self.commands = collections.OrderedDict()
        self.commands_raw = collections.OrderedDict()

    def parse(self):
        '''Main handler, find and parse Dockerfile'''
        dockerfile = self._findFile()
        if not dockerfile:
            raise ParserError(
                '{} does not exist at current directory or any of its parents'
                .format(self.DOCKERFILE)
            )
        with open(dockerfile) as f:
            self._parseFile(f)
        return self

    def _findFile(self):
        '''Find Dockerfile in curdir or any of its parent directories'''
        if os.path.exists(self.DOCKERFILE):
            return self.DOCKERFILE

        curpath = os.curdir
        lastpath = None
        while True:
            curpath = os.path.abspath(os.path.join(curpath, '..'))
            dockerfile = os.path.join(curpath, self.DOCKERFILE)
            if os.path.exists(dockerfile):
                self.path = curpath
                return dockerfile
            if curpath == lastpath:
                return False
            lastpath = curpath

    def _parseFile(self, fh):
        '''Check each line in `fh` for wd comments and parse them

        Call `_parseDirective` with the contents of the line when found
        and expand variables immediately after.'''
        for line in fh:
            self.lineno += 1
            if line.startswith('#wd#'):
                self._parseDirective(line)
                self._expandVariables()

    def _parseDirective(self, line):
        '''Differentiate between variables/commands in `line`

        Add the variable or command to the appropiate OrderedDict.'''
        new = line[4:].split()
        if new[0].endswith(':'):
            self.commands_raw[new[0][:-1]] = ' '.join(new[1:])
        elif new[1] == '=':
            self.variables[new[0]] = ' '.join(new[2:])

    def _expandVariables(self):
        '''Loop through variables and commands_raw and expand variables'''
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
    '''Shell command argument handling'''

    def __init__(self, args=sys.argv[1:]):
        '''Initialize `Parser` object and shell arguments'''
        self.args = args
        self.error = None
        try:
            self.parser = Parser().parse()
        except ParserError as error:
            self.parser = None
            self.error = error

    def run(self):
        '''Run the program'''
        # Internal commands that do not need a Dockerfile ####################
        # handle -h, -help, --help, -? and handle -version
        if self.args:
            if self.args[0] in ('-h', '-help', '--help'):
                self._usage(help=True)
                return 0
            elif self.args[0] == '-version':
                print('wdocker {}'.format(__version__))
                return 0

        # show parser errors if there are any and exit with exit code 2
        if self.error:
            self._usage(self.error)
            return 2

        # show usage when wdocker is run without arguments
        if not self.args:
            self._usage()
            return 0

        # Internal commands that do need a Dockerfile ########################
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
        '''Print variable `arg` if it can be found'''
        if arg in self.parser.variables.keys():
            print(self.parser.variables[arg])
            return 0
        self._usage('variable {} does not exist'.format(arg))
        return 3

    def _call(self, arg):
        '''Change to parser.path and run the defined wdocker `arg` command'''
        command = '{} {}'.format(self.parser.commands[arg],
                                 ' '.join(self.args[1:])).strip()
        print(':: ' + command)
        subprocess.call(command, shell=True, cwd=self.parser.path)
        return 0

    def _usage(self, error='', help=False):
        '''Print usage information'''
        if error:
            print('Error: {}\n'.format(error))
        print('Usage: wdocker [<command> | -help] [<program arguments> ...]')

        if help:
            print('\nInternal commands:')
            print('  -help, -h, --help      show full usage info and vars')
            print('  -version               show version info')
            print('  -print-var <variable>  print value of <variable>')

            if self.parser and self.parser.variables:
                varlen = max(len(i) for i in self.parser.variables.keys())
                print('\nVariables:')
                for k, v in self.parser.variables.items():
                    print('  {} = {}'.format(
                        paddedColoredOutput(k, varlen, True), v
                    ))

        if self.parser:
            if self.parser.commands:
                commandlen = max(len(i) for i in self.parser.commands.keys())
                print('\nCommands:')
                for k, v in self.parser.commands.items():
                    print('  {}  {}'.format(
                        paddedColoredOutput(k, commandlen), v
                    ))
            else:
                print('\nCommands: No commands defined in Dockerfile (yet)')

if __name__ == '__main__':
    sys.exit(WDocker().run())
