# Copyright (c) 2015 Benjamin Althues <benjamin@babab.nl>
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

from nose.tools import eq_
from collections import OrderedDict

import wdocker


def test_parser_noinit():
    '''Parser: file_exists is None when not initialized'''
    parser = wdocker.Parser
    eq_(parser.file_exists, None)


def test_parser_init():
    '''Parser: file_exists is False when initialized (in main dir)'''
    parser = wdocker.Parser()
    eq_(parser.file_exists, False)


def test_parser_collections():
    '''Parser: variables and commands(_raw) are of type OrderedDict'''
    parser = wdocker.Parser()
    eq_(parser.variables, OrderedDict())
    eq_(parser.commands, OrderedDict())
    eq_(parser.commands_raw, OrderedDict())


def test_parser_parse_var():
    '''Parser: parsing a variable'''
    parser = wdocker.Parser()
    parser._parseDirective('#wd# testvar = testvalue')
    eq_(parser.variables, OrderedDict([('testvar', 'testvalue')]))


def test_parser_parse_multiple_vars():
    '''Parser: parsing multiple variables'''
    parser = wdocker.Parser()
    parser._parseDirective('#wd# testvar1 = testvalue1')
    parser._parseDirective('#wd# testvar2 = testvalue2')
    eq_(parser.variables,
        OrderedDict([
            ('testvar1', 'testvalue1'),
            ('testvar2', 'testvalue2'),
        ]))


def test_parser_parse_command():
    '''Parser: parsing a command'''
    parser = wdocker.Parser()
    parser._parseDirective('#wd# testcmd: testvalue')
    eq_(parser.commands_raw, OrderedDict([('testcmd', 'testvalue')]))
    eq_(parser.commands, OrderedDict())


def test_parser_expanding_variables_in_variable():
    '''Parser: expanding variables in a variable'''
    parser = wdocker.Parser()
    parser._parseDirective('#wd# foo = bar')
    parser._parseDirective('#wd# bar = {foo}')
    eq_(parser.variables, OrderedDict([('foo', 'bar'), ('bar', '{foo}')]))
    parser._expandVariables()
    eq_(parser.variables, OrderedDict([('foo', 'bar'), ('bar', 'bar')]))


def test_parser_expanding_variables_in_command():
    '''Parser: expanding variables in a command'''
    parser = wdocker.Parser()
    parser._parseDirective('#wd# foo = fubar -foo bar')
    parser._parseDirective('#wd# mycommand: {foo}')
    eq_(parser.commands_raw, OrderedDict([('mycommand', '{foo}')]))
    parser._expandVariables()
    eq_(parser.commands, OrderedDict([('mycommand', 'fubar -foo bar')]))
