import unittest
from typing import Any, Dict, List

from src.gdtransform.transform import batch_transformation, transformation


@transformation(name='my-transformation')
def add_field(data: Dict[str, Any]):
    data['field'] = 'value'


@batch_transformation(name='my-batch-transformation')
def add_batch_field(data_list: List[Dict[str, Any]]):
    for data in data_list:
        data['field'] = 'value'


class WrapperTest(unittest.TestCase):

    def test_wrapper(self):
        self.assertEqual(True, getattr(add_field, '__gd_transformation__'))
        self.assertEqual('my-transformation', getattr(add_field, '__gd_transformation_name__'))

    def test_transform(self):
        data = {}
        add_field(data)
        self.assertTrue('field' in data)
        self.assertEqual('value', data['field'])


class BatchWrapperTest(unittest.TestCase):

    def test_wrapper(self):
        self.assertEqual(True, getattr(add_batch_field, '__gd_batch_transformation__'))
        self.assertEqual('my-batch-transformation', getattr(add_batch_field, '__gd_transformation_name__'))

    def test_transform(self):
        data_list = [{}]
        add_batch_field(data_list)
        for data in data_list:
            self.assertTrue('field' in data)
            self.assertEqual('value', data['field'])
