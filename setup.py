#!/usr/bin/env python

import sys
import os
from os.path import abspath, join, dirname
from distutils.core import setup
from distutils.command.install_scripts import install_scripts

try:
    import setuptools    # use setuptools when available
except ImportError:
    pass

CURDIR = dirname(abspath(__file__))

with open(join(CURDIR, 'src', 'robot', 'version.py')) as f:
    exec(f.read())
    VERSION = get_version()
with open(join(CURDIR, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()
    base_url = 'https://github.com/robotframework/robotframework/blob/master'
    for text in ('INSTALL', 'CONTRIBUTING'):
        search = '`<{0}.rst>`__'.format(text)
        replace = '`{0}.rst <{1}/{0}.rst>`__'.format(text, base_url)
        if search not in LONG_DESCRIPTION:
            raise RuntimeError('{} not found from README.rst'.format(search))
        LONG_DESCRIPTION = LONG_DESCRIPTION.replace(search, replace)
CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
""".strip().splitlines()
KEYWORDS = 'robotframework testing testautomation acceptancetesting atdd bdd'
# Maximum width in Windows installer seems to be 70 characters -------|
WINDOWS_DESCRIPTION = """
Robot Framework is a generic test automation framework for acceptance
testing and acceptance test-driven development (ATDD). It has
easy-to-use tabular test data syntax and utilizes the keyword-driven
testing approach. Its testing capabilities can be extended by test
libraries implemented either with Python or Java, and users can create
new keywords from existing ones using the same syntax that is used for
creating test cases.
""".strip()
PACKAGES = ['robot', 'robot.api', 'robot.conf', 'robot.htmldata',
            'robot.libdocpkg', 'robot.libraries', 'robot.model',
            'robot.output', 'robot.output.console', 'robot.parsing',
            'robot.reporting', 'robot.result', 'robot.running',
            'robot.running.arguments', 'robot.running.timeouts',
            'robot.utils', 'robot.variables', 'robot.writer']
PACKAGE_DATA = [join('htmldata', directory, pattern)
                for directory in ('rebot', 'libdoc', 'testdoc', 'lib', 'common')
                for pattern in ('*.html', '*.css', '*.js')]
WINDOWS = os.sep == '\\'
if sys.platform.startswith('java'):
    SCRIPTS = ['jybot', 'jyrebot', 'robot', 'rebot']
    INTERPRETER = 'jython'
elif sys.platform == 'cli':
    SCRIPTS = ['ipybot', 'ipyrebot', 'robot', 'rebot']
    INTERPRETER = 'ipy'
else:
    SCRIPTS = ['pybot', 'rebot', 'robot']
    INTERPRETER = 'python'
SCRIPTS = [join('src', 'bin', s) for s in SCRIPTS]
if WINDOWS:
    SCRIPTS = [s+'.bat' for s in SCRIPTS]
if 'bdist_wininst' in sys.argv:
    SCRIPTS.append('robot_postinstall.py')
    LONG_DESCRIPTION = WINDOWS_DESCRIPTION


def replace_interpreter(filepath):
    with open(filepath, 'r') as input:
        replaced = input.read().replace('python', INTERPRETER)
    with open(filepath, 'w') as output:
        output.write(replaced)


class install_scripts_and_replace_bat_interpreter(install_scripts):
    def run(self):
        install_scripts.run(self)
        if not WINDOWS or INTERPRETER == 'python':
            return
        print("replacing interpreter in robot.bat and rebot.bat.")
        for filepath in self.get_outputs():
            if filepath.endswith('robot.bat'):
                replace_interpreter(filepath)
            if filepath.endswith('rebot.bat'):
                replace_interpreter(filepath)


setup(
    name         = 'robotframework',
    version      = VERSION,
    author       = 'Robot Framework Developers',
    author_email = 'robotframework@gmail.com',
    url          = 'http://robotframework.org',
    download_url = 'https://pypi.python.org/pypi/robotframework',
    license      = 'Apache License 2.0',
    description  = 'A generic test automation framework',
    long_description = LONG_DESCRIPTION,
    keywords     = KEYWORDS,
    platforms    = 'any',
    classifiers  = CLASSIFIERS,
    cmdclass = {'install_scripts': install_scripts_and_replace_bat_interpreter},
    package_dir  = {'': 'src'},
    package_data = {'robot': PACKAGE_DATA},
    packages     = PACKAGES,
    scripts      = SCRIPTS,
)
