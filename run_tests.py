import optparse
import os
import sys
import unittest2

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


def main(sdk_path, test_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    # tests/ directory
    if os.path.isdir(test_path):
        suite = unittest2.loader.TestLoader().discover(test_path)
    # test_file.py
    elif os.path.isfile(test_path):
        test_path, test_file = test_path.rsplit(os.path.sep, 1)
        suite = unittest2.loader.TestLoader().discover(test_path, test_file)
    # tests.module.TestCase
    else:
        module_name, class_name = test_path.rsplit('.', 1)
        module = __import__(module_name, fromlist=[module_name])
        testcase = getattr(module, class_name)
        suite = unittest2.loader.TestLoader().loadTestsFromTestCase(testcase)
    unittest2.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 2:
        print 'Error: Exactly 2 arguments required.'
        parser.print_help()
        sys.exit(1)
    SDK_PATH = args[0]
    TEST_PATH = args[1]
    main(SDK_PATH, TEST_PATH)
