from typing import Any, Dict, List

from .constants import GRID_BATCH_TRANSFORMATION_FLAG, GRID_TRANSFORMATION_FLAG, GRID_TRANSFORMATION_NAME


def transformation(name: str):
    if not name:
        raise Exception('invalid transformation name')

    def __transformation(function):
        def wrapper(data: Dict[str, Any]):
            function(data)

        setattr(wrapper, GRID_TRANSFORMATION_FLAG, True)
        setattr(wrapper, GRID_TRANSFORMATION_NAME, name)

        return wrapper

    return __transformation


def batch_transformation(name: str):
    if not name:
        raise Exception('invalid batch transformation name')

    def __transformation(function):
        def wrapper(data_list: List[Dict[str, Any]]):
            if not data_list:
                return
            function(data_list)

        setattr(wrapper, GRID_BATCH_TRANSFORMATION_FLAG, True)
        setattr(wrapper, GRID_TRANSFORMATION_NAME, name)

        return wrapper

    return __transformation
