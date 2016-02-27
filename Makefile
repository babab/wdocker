# Copyright (c) 2015-2016  Benjamin Althues <benjamin@althu.es>
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

DESTDIR			= /
PIP			= pip
PYTHON			= python
VERSION			= 0.2.0
ZSH_SITE_FUNCS_PATH	= $(DESTDIR)/usr/share/zsh/site-functions

.PHONY: make install install-pip install-src install-zsh dist clean

make:
	@echo 'make install        alias for install-pip'
	@echo 'make install-pip    install wdocker wheel pkg with pip (default)'
	@echo 'make install-src    install via setup.py install --root=$$DESTDIR'
	@echo ''
	@echo 'make install-zsh    only install shell completion for Zsh'
	@echo ''
	@echo 'make dist           make distributions'
	@echo 'make clean          remove cache, build, egg and dist files'

install: install-pip

install-pip: dist install-zsh
	$(PIP) install --upgrade dist/wdocker-$(VERSION)-py2.py3-none-any.whl
install-src: install-zsh
	$(PYTHON) setup.py install --root='$(DESTDIR)'

install-zsh:
	install -Dm 644 zsh/_wdocker "$(ZSH_SITE_FUNCS_PATH)/_wdocker"

dist:
	$(PIP) install -r requirements-dev.txt
	$(PYTHON) setup.py sdist bdist_wheel check
clean:
	rm -rf __pycache__ build dist wdocker.egg-info
