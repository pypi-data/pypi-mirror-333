# coding=utf-8
"""
Decorator for callable objects
"""

import functools
from typing import Callable, Optional
from .handler_kind import HandlerKind
from .handlers import Handlers, Handler


# pylint: disable=too-few-public-methods
class CallWithHandlers:
    """
    Decorator that register handlers before and after callable object call.
    """
    def __init__(self, handlers: Optional[Handlers] = None):
        self.func = None
        self.handlers = handlers if isinstance(handlers, Handlers) else Handlers()

    def __call__(self, func) -> Callable:
        """
        Decorate function with handlers
        """
        functools.update_wrapper(self, func)
        self.func = func

        if self.func is not None:
            # decorate function call by at_time handlers
            for handler in self.handlers.at_time:
                self.func = handler(self.func)

        return self._wrapper

    def _wrapper(self, *args, **kwargs):
        """
        Decorator implementation.
        """
        result = None
        if self.func is not None:
            # prepare call of decorated function
            for handler in self.handlers.before:
                handler_result = handler(*args, **kwargs)
                if isinstance(handler, Handler):
                    match handler.kind:
                        # do not call callable object if handler result is negative
                        case HandlerKind.CHECK_CONDITION:
                            if not handler_result:
                                return None
                        # update positional and keyword arguments before call
                        case HandlerKind.RETURN_VALUE:
                            args, kwargs = handler_result
            # call
            result = self.func(*args, **kwargs)

            # process result of call
            for handler in self.handlers.after:
                handler_result = handler(result)
                if isinstance(handler, Handler):
                    match handler.kind:
                        # do not return result of call of callable object
                        # if handler result is negative
                        case HandlerKind.CHECK_CONDITION:
                            if not handler_result:
                                return None
                        # update result of call of callable object
                        case HandlerKind.RETURN_VALUE:
                            result = handler_result

        return result
