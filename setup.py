import os, sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    """
    A test command to run pytest on a the full repository.
    This means that any function name test_XXXX
    or any class named TestXXXX will be found and run.
    """
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main([".", "-vv"])
        sys.exit(errno)

setup(
    name="neasqc-qrbs",
    version=os.getenv("TAG_NAME", "0.4.1"),
    author="Samuel Magaz-Romero",
    author_email="s.magazr@udc.es",
    license="European Union Public License 1.2",

    packages=find_packages(),
    install_requires=["numpy", "myqlm"],
    # Don't change these two lines
    tests_require=["pytest"],
    cmdclass={'test': PyTest},
)
