import unittest
from typing import Any, Dict, List

from src.gdtransform.test import TransformationTest
from src.gdtransform.transform import transformation_builder


@transformation_builder(name='builder1', is_batch=False)
def my_transformation_builder(*args, **kwargs):
    def add_field(data: Dict[str, Any]):
        data['field'] = 'value'

    return add_field


@transformation_builder(name='builder2', is_batch=True)
def my_batch_transformation_builder(*args, **kwargs):
    def add_field(data_list: List[Dict[str, Any]]):
        for data in data_list:
            data['field'] = 'value'

    return add_field


class BuilderTest(unittest.TestCase):

    def test_builder_sanity(self):
        transformation = my_transformation_builder('my-transformation')
        passed, error = TransformationTest('my-transformation', transformation).run_sanity_tests()
        self.assertTrue(passed)
        self.assertFalse(error)

    def test_builder_singleton(self):
        transformation = my_transformation_builder('my-transformation')
        data = {}
        transformation(data)
        self.assertTrue('field' in data)
        self.assertEqual('value', data['field'])

    def test_builder_batch(self):
        transformation = my_batch_transformation_builder('my-transformation')
        data_list = [{}, {}]
        transformation(data_list)
        for data in data_list:
            self.assertTrue('field' in data)
            self.assertEqual('value', data['field'])
