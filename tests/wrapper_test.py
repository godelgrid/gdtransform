import unittest
from typing import Any, Dict

from src.gdtransform.transform import transformation


@transformation(name='my-transformation')
def add_field(data: Dict[str, Any]):
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
