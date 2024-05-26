from inspect import getmembers, isfunction

from .constants import GRID_BATCH_TRANSFORMATION_FLAG, GRID_TRANSFORMATION_BUILDER_FLAG, \
    GRID_TRANSFORMATION_BUILDER_NAME, GRID_TRANSFORMATION_FLAG, \
    GRID_TRANSFORMATION_NAME


def has_transformation_flag(function):
    return (hasattr(function, GRID_TRANSFORMATION_FLAG) and
            getattr(function, GRID_TRANSFORMATION_FLAG)) or \
        (hasattr(function, GRID_BATCH_TRANSFORMATION_FLAG) and
         getattr(function, GRID_BATCH_TRANSFORMATION_FLAG))


def has_builder_flag(function):
    return hasattr(function, GRID_TRANSFORMATION_BUILDER_FLAG) and \
        getattr(function, GRID_TRANSFORMATION_BUILDER_FLAG)


def is_valid_transformation(function, name):
    return has_transformation_flag(function) and \
        hasattr(function, GRID_TRANSFORMATION_NAME) and \
        getattr(function, GRID_TRANSFORMATION_NAME) == name


def is_valid_builder(function, name):
    return has_builder_flag(function) and \
        hasattr(function, GRID_TRANSFORMATION_BUILDER_NAME) and \
        getattr(function, GRID_TRANSFORMATION_BUILDER_NAME) == name


def get_module_transformation(module, name: str):
    members = getmembers(module, isfunction)
    if not members:
        return None
    for (_, member_func) in members:
        if is_valid_transformation(member_func, name) or is_valid_builder(member_func, name):
            return member_func

    return None


def is_batch_transformation(function):
    return hasattr(function, GRID_BATCH_TRANSFORMATION_FLAG) and \
        getattr(function, GRID_BATCH_TRANSFORMATION_FLAG)


def is_transformation_builder(function):
    return has_builder_flag(function)
