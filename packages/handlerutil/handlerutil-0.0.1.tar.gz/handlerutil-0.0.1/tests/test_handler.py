"""
Test Handler class
"""
import pytest

from handlerutil import Handler, HandlerKind


def test_handler_simple_init():
    a = Handler(lambda x: print(x))
    assert isinstance(a, Handler)
    assert a.kind == HandlerKind.NO_RETURN

def test_handler_full_init():
    a = Handler(lambda x: print(x), HandlerKind.RETURN_VALUE)
    assert isinstance(a, Handler)
    assert a.kind == HandlerKind.RETURN_VALUE

def test_handler_full_init_kwargs():
    a = Handler(func=lambda x: print(x), kind=HandlerKind.CHECK_CONDITION)
    assert isinstance(a, Handler)
    assert a.kind == HandlerKind.CHECK_CONDITION

@pytest.mark.parametrize(
    'kind',
    (
        HandlerKind.NO_RETURN,
        HandlerKind.RETURN_VALUE,
        HandlerKind.CHECK_CONDITION,
    ),
)
def test_call(kind):
    a = Handler(lambda x: x + 1, kind=kind)
    assert a(1) == 2
