# Copyright (c) 2010 Jean-Paul Calderone
# See LICENSE file for details.

from distutils.core import Extension, setup, Command
import sys, distutils.util
from unittest import TextTestRunner, TestLoader

class TestCommand(Command):
    user_options = [ ]

    def initialize_options(self):
        pass
    def finalize_options(self):
        sys.path.append(
            'build/lib.%s-%s/signalfd' %
            ( distutils.util.get_platform(), sys.version[0:3]))

    def run(self):
        '''Run unittests'''
        import signalfd.test.test_signalfd
        # testfiles = [ 'signalfd/test/test_signalfd.py' ]
        # tests = TestLoader().loadTestsFromNames(testfiles)
        # import signalfd.test
        # tests = TestLoader().loadTestsFromModule(signalfd.test.test_signalfd)
        # t = TextTestRunner(verbosity = 1)
        # t.run(tests)


setup(
    name="python-signalfd",
    description="Python bindings for sigprocmask(2) and signalfd(2)",
    version="0.2",
    author="Jean-Paul Calderone",
    author_email="exarkun@twistedmatrix.com",
    url="http://launchpad.net/python-signalfd",
    packages=["signalfd", "signalfd.test"],
    ext_modules=[Extension(
            name="signalfd._signalfd",
            sources=["signalfd/_signalfd.c"]),
                 ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    cmdclass = { 'test': TestCommand },
    )

