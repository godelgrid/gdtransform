from typing import Any, Dict, List

from .constants import GRID_BATCH_TRANSFORMATION_FLAG, \
    GRID_TRANSFORMATION_BUILDER_FLAG, GRID_TRANSFORMATION_BUILDER_NAME, GRID_TRANSFORMATION_FLAG, \
    GRID_TRANSFORMATION_NAME


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


def transformation_builder(name: str, is_batch: bool):
    if not name:
        raise Exception('name is mandatory')
    elif is_batch is None:
        raise Exception('is_batch option not specified')

    def __builder(operator):
        def wrapper(transformation_name: str, *args, **kwargs):
            operator_callable = operator(*args, **kwargs)

            if not is_batch:
                @transformation(name=transformation_name)
                def __wrapped_transformation(data: Dict[str, Any]):
                    operator_callable(data)

                return __wrapped_transformation
            else:
                @batch_transformation(name=transformation_name)
                def __wrapped_transformation(data_list: List[Dict[str, Any]]):
                    operator_callable(data_list)

                return __wrapped_transformation

        setattr(wrapper, GRID_TRANSFORMATION_BUILDER_FLAG, True)
        setattr(wrapper, GRID_TRANSFORMATION_BUILDER_NAME, name)

        return wrapper

    return __builder
