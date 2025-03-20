# coding=utf-8
"""
Collection iterator
"""

from typing import Optional, Iterable
from .handler_kind import HandlerKind
from .handlers import Handlers, Handler


class IterateWithHandlers:
    """
    Collection with handlers iterator
    """
    def __init__(self, handlers: Optional[Handlers] = None):
        self.handlers = handlers if isinstance(handlers, Handlers) else Handlers()

    def __iter__(self):
        return self

    def __next__(self, iterable: Iterable):
        """
        Iterate collection with handlers
        """
        # prepare iteration
        for handler in self.handlers.before:
            handler_result = handler(iterable)
            if isinstance(handler, Handler):
                match handler.kind:
                    # return before iteration if is not passed by condition
                    case HandlerKind.CHECK_CONDITION:
                        if not handler_result:
                            return None
                    # update iterable
                    case HandlerKind.RETURN_VALUE:
                        iterable = handler_result

        # iterate
        for item in iterable:
            for handler in self.handlers.at_time:
                handler_result = handler(item)
                if isinstance(handler, Handler):
                    match handler.kind:
                        # break iteration if is not passed by condition
                        case HandlerKind.CHECK_CONDITION:
                            if not handler_result:
                                return None
                        # update returning element
                        case HandlerKind.RETURN_VALUE:
                            item = handler_result
                yield item

        # do work with iterable after iteration
        for handler in self.handlers.after:
            handler(iterable)
        return None
