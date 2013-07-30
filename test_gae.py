#!/usr/bin/python
import optparse
import sys
import unittest

USAGE = """%prog SDK_PATH
Runs the unit tests.

SDK_PATH    Path to the SDK installation"""


def setUpGAE(sdk_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 1:
        print 'The SDK path should be the only argument.'
        parser.print_help()
        sys.exit(1)
    setUpGAE(args[0])
    loader = unittest.TestLoader()
    suites = loader.discover('./tests')
    runner = unittest.TextTestRunner()
    runner.run(suites)
