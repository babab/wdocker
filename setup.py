# vim: set et ts=4 sw=4 sts=4 ai:

from setuptools import setup
import wdocker

_description = 'Define docker commands in your Dockerfile'

setup(
    name='wdocker',
    version=wdocker.__version__,
    description=_description,
    author=wdocker.__author__,
    author_email='benjamin@babab.nl',
    url='http://github.com/babab/wdocker',
    download_url='https://pypi.python.org/pypi/wdocker',
    py_modules=['wdocker'],
    license='ISC',
    long_description='{}\n\n{}'.format(
        open('README.rst').read().replace(_description, ''),
        open('CHANGELOG.rst').read()
    ),
    platforms='any',
    scripts=['script/wdocker'],
    classifiers=[
        # 'BLOCK FOR UPLOAD',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Unix Shell',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: System Shells',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
)
