import pytest

from pypiccolo.hello import hello as super_hello
from pypiccolo.sub_hello.hello import hello as sub_hello
import pypiccolo.math_utils as math_utils

def test_super_hello():
    assert super_hello() == 'Hello, universe!'

def test_sub_hello():
    assert sub_hello() == 'Hello, world!'

def test_random_array():
    for shape in [(3,), (2, 2,), (1, 1, 1,)]:
        assert math_utils.random_array(shape).shape == shape
