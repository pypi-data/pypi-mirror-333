# coding=utf-8
"""
Handler class
"""

from dataclasses import dataclass
from typing import Callable
from .handler_kind import HandlerKind


@dataclass
class Handler:
    """
    Handler class helps to understand that handler management system has to do with handler result
    because of HandlerKind.
    """
    func: Callable
    kind: HandlerKind = HandlerKind.NO_RETURN

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
