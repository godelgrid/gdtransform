import json
import traceback
from typing import Callable, List, Tuple

from .constants import GRID_BATCH_TRANSFORMATION_FLAG, GRID_TRANSFORMATION_FLAG, GRID_TRANSFORMATION_NAME


class TransformationTest:

    def __init__(self, name: str, transformation: Callable):
        self._name = name
        self._transformation = transformation
        self._singleton_transform = hasattr(transformation, GRID_TRANSFORMATION_FLAG) and \
                                    getattr(transformation, GRID_TRANSFORMATION_FLAG)
        self._batch_transform = hasattr(self._transformation, GRID_BATCH_TRANSFORMATION_FLAG) and \
                                getattr(self._transformation, GRID_BATCH_TRANSFORMATION_FLAG)

    def test_valid_transformation(self) -> Tuple[bool, str]:
        if not self._singleton_transform and not self._batch_transform:
            return False, "Transformation flag not configured for function. Function might not be properly decorated with transformation operator."
        elif not hasattr(self._transformation, GRID_TRANSFORMATION_NAME) or \
                getattr(self._transformation, GRID_TRANSFORMATION_NAME) != self._name:
            return False, "Transformation name not set on function or is not equal to provided name"
        else:
            return True, ""

    def test_empty_dict(self) -> Tuple[bool, str]:
        try:
            if self._singleton_transform:
                self._transformation({})
            else:
                self._transformation([{}])
            return True, ""
        except Exception:
            message = traceback.format_exc()
            return False, "Error occurred while processing empty dict: " + message

    def test_empty_batch(self) -> Tuple[bool, str]:
        try:
            if self._batch_transform:
                self._transformation([])
            return True, ""
        except Exception:
            message = traceback.format_exc()
            return False, "Error occurred while processing empty batch: " + message

    def test_empty_dict_json(self) -> Tuple[bool, str]:
        try:
            data = {}
            if self._singleton_transform:
                self._transformation(data)
            else:
                self._transformation([data])
            json_data = json.dumps(data)
            return True, ""
        except Exception:
            message = traceback.format_exc()
            return False, "Error occurred while converting data to json after processing: " + message

    def run_sanity_tests(self) -> Tuple[bool, List[str]]:
        passed = True
        errors = []
        success, message = self.test_valid_transformation()
        if not success:
            passed = False
            errors.append(message)
        success, message = self.test_empty_dict()
        if not success:
            passed = False
            errors.append(message)
        success, message = self.test_empty_dict_json()
        if not success:
            passed = False
            errors.append(message)

        return passed, errors
