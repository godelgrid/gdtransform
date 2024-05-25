import unittest
from typing import Any, Dict, List

from src.gdtransform.test import TransformationTest
from src.gdtransform.transform import batch_transformation, transformation


class TestTest(unittest.TestCase):

    def test_correct_case(self):
        @transformation(name='correct-case')
        def add_field(data: Dict[str, Any]):
            data['field'] = 'value'

        test = TransformationTest('correct-case', add_field)
        passed, errors = test.run_sanity_tests()
        self.assertTrue(passed)
        self.assertFalse(errors)

    def test_negative_valid_transformation(self):
        def func(data):
            pass

        test = TransformationTest('random', func)
        success, error = test.test_valid_transformation()
        self.assertFalse(success)
        self.assertTrue(error)

    def test_negative_empty_dict(self):
        @transformation(name='func')
        def func(data):
            if not data:
                raise Exception('received empty dict')

        test = TransformationTest('func', func)
        success, error = test.test_empty_dict()
        self.assertFalse(success)
        self.assertTrue(error.startswith("Error occurred while processing empty dict: "))

    def test_negative_empty_dict_json(self):
        def non_serializable_func(data):
            pass

        @transformation(name='func')
        def func(data):
            data['field'] = non_serializable_func

        test = TransformationTest('func', func)
        success, error = test.test_empty_dict_json()
        self.assertFalse(success)
        self.assertTrue(error.startswith("Error occurred while converting data to json after processing: "))


class TestBatchTest(unittest.TestCase):

    def test_correct_case(self):
        @batch_transformation(name='correct-case')
        def add_batch_field(data_list: List[Dict[str, Any]]):
            for data in data_list:
                data['field'] = 'value'

        test = TransformationTest('correct-case', add_batch_field)
        passed, errors = test.run_sanity_tests()
        self.assertTrue(passed)
        self.assertFalse(errors)

    def test_negative_valid_transformation(self):
        def func(data):
            pass

        test = TransformationTest('random', func)
        success, error = test.test_valid_transformation()
        self.assertFalse(success)
        self.assertTrue(error)

    def test_negative_empty_dict(self):
        @batch_transformation(name='func')
        def func(data_list: List[Dict[str, Any]]):
            for data in data_list:
                if not data:
                    raise Exception('received empty dict')

        test = TransformationTest('func', func)
        success, error = test.test_empty_dict()
        self.assertFalse(success)
        self.assertTrue(error.startswith("Error occurred while processing empty dict: "))

    def test_negative_empty_dict_json(self):
        def non_serializable_func(data):
            pass

        @batch_transformation(name='func')
        def func(data_list):
            for data in data_list:
                data['field'] = non_serializable_func

        test = TransformationTest('func', func)
        success, error = test.test_empty_dict_json()
        self.assertFalse(success)
        self.assertTrue(error.startswith("Error occurred while converting data to json after processing: "))
