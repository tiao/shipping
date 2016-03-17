# -*- coding: utf-8 -*-
import sys

from setuptools import setup
from setuptools.command.test import test


class Tox(test):
    def initialize_options(self):
        test.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        sys.exit(tox.cmdline())

if __name__ == '__main__':
    setup(
        name='axado.py',
        version='1.0',
        description='Makes the shipping calculation based in input parameters',
        author='Filipe Almeida',
        author_email='f.almeida87@gmail.com',
        url='https://github.com/tiao/shipping',
        py_modules=['axado'],
        tests_require=['tox'],
        cmdclass={'test': Tox},
    )
