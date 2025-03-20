# coding=utf-8
"""
Kind of handler
"""

from enum import StrEnum


class HandlerKind(StrEnum):
    """
    Kind of handler.
    It helps to understand that handler management system has to do with handler result.
    """
    # no replace data by handler return
    NO_RETURN = 'NoReturn'
    # replace data by handler return
    RETURN_VALUE = 'ReturnValue'
    # handler must to return bool,
    # and if handler result is negative (False or None) then return None as callable object result
    CHECK_CONDITION = 'CheckCondition'
