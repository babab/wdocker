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

VERSION			= 0.2.0
ZSH_SITE_FUNCS_PATH	= /usr/share/zsh/site-functions

.PHONY: make install install-wheel install-dev install-src install-zsh \
	uninstall depends dist clean cleanup

make:
	@echo 'make install        alias for install-wheel'
	@echo 'make install-wheel  install wdocker via wheel (default)'
	@echo 'make install-src    install via source package'
	@echo 'make install-dev    install via egg-link (for development)'
	@echo 'make install-zsh    only install shell completion for Zsh'
	@echo 'make uninstall      uninstall wdocker'
	@echo ''
	@echo 'make dist           make distributions'
	@echo 'make clean          remove cache, and build files'
	@echo 'make cleanup        remove cache, build, egg and dist files'

install: install-wheel

install-wheel: dist install-zsh
	pip install --upgrade dist/wdocker-$(VERSION)-py2.py3-none-any.whl
	make clean
install-src: dist install-zsh
	pip install --upgrade dist/wdocker-$(VERSION).tar.gz
	make clean
install-dev: cleanup install-zsh
	pip install --upgrade -e .
	make clean
install-zsh:
	install -Dm 644 zsh/_wdocker $(ZSH_SITE_FUNCS_PATH)
uninstall:
	pip uninstall wdocker
depends:
	pip install -r requirements-dev.txt
dist: cleanup depends
	python setup.py sdist bdist_wheel check
clean:
	rm -rf __pycache__ build
cleanup: clean
	rm -rf dist wdocker.egg-info
