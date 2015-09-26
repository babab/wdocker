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

.PHONY: make install install-wheel install-dev install-src uninstall dist \
	clean cleanup

make:
	@echo 'make install        alias for install-wheel'
	@echo 'make install-wheel  install wdocker via wheel (default)'
	@echo 'make install-src    install via source package'
	@echo 'make install-dev    install via egg-link (for development)'
	@echo 'make uninstall      uninstall wdocker'
	@echo 'make dist           make distributions'
	@echo 'make clean          remove cache, and build files'
	@echo 'make cleanup        remove cache, build, egg and dist files'

install: install-wheel

install-wheel: dist
	pip install --upgrade dist/wdocker-0.1.0-py2.py3-none-any.whl
	make clean
install-src: dist
	pip install --upgrade dist/wdocker-0.1.0.tar.gz
	make clean
install-dev: cleanup
	pip install --upgrade -e .
	make clean
uninstall:
	pip uninstall wdocker
dist: cleanup
	python setup.py sdist bdist_wheel check
clean:
	rm -rf __pycache__ build
cleanup: clean
	rm -rf dist wdocker.egg-info
