import unittest
from typing import Any, Dict, List

from src.gdtransform.introspect import get_module_transformation, is_batch_transformation
from src.gdtransform.transform import batch_transformation, transformation


@transformation(name='module-transformation')
def module_transformation(data: Dict[str, Any]):
    data['field'] = 'value'


@batch_transformation(name='transformation-2')
def transformation2(data_list: List[Dict[str, Any]]):
    for data in data_list:
        data['second'] = 'second_value'


class IntrospectTest(unittest.TestCase):

    def test_find_module(self):
        data = {}
        from tests import introspect_test as test_module
        func = get_module_transformation(test_module, 'module-transformation')
        func(data)
        self.assertEqual('value', data['field'])
        func = get_module_transformation(test_module, 'transformation-2')
        func([data])
        self.assertEqual('second_value', data['second'])

    def test_find_module_negative(self):
        from tests import introspect_test as test_module
        func = get_module_transformation(test_module, 'module-random')
        self.assertIsNone(func)

    def test_is_batch_transformation(self):
        self.assertTrue(is_batch_transformation(transformation2))
        self.assertFalse(is_batch_transformation(module_transformation))
