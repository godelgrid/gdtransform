import unittest

from tests.builder_test import BuilderTest
from tests.introspect_test import IntrospectTest
from tests.test_test import TestBatchTest, TestTest
from tests.wrapper_test import BatchWrapperTest, WrapperTest

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(IntrospectTest))
test_suite.addTest(unittest.makeSuite(TestTest))
test_suite.addTest(unittest.makeSuite(TestBatchTest))
test_suite.addTest(unittest.makeSuite(WrapperTest))
test_suite.addTest(unittest.makeSuite(BatchWrapperTest))
test_suite.addTest(unittest.makeSuite(BuilderTest))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite)
