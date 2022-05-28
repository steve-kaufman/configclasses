import os
from re import S
import sys
from configclasses import configclass
from .util import retain_environ, retain_sys_args

@configclass
class MyConfigClass:
    foo: str
    bar: int
    baz: bool

@retain_sys_args
def test_with_cli_args():
    sys.argv = [sys.argv[0], '--foo', 'apple', '--bar', '5', '--baz']

    my_config_class = MyConfigClass()

    assert(my_config_class.foo == "apple")
    assert(my_config_class.bar == 5)
    assert(my_config_class.baz == True)

@retain_environ
def test_with_env():
    os.environ["FOO"] = "banana"
    os.environ["BAR"] = "6"
    os.environ["BAZ"] = "true"

    my_config_class = MyConfigClass()

    assert(my_config_class.foo == "banana")
    assert(my_config_class.bar == 6)
    assert(my_config_class.baz == True)

@retain_sys_args
@retain_environ
def test_with_args_and_env():
    sys.argv = [sys.argv[0], '--bar', '7', '--baz']
    os.environ["FOO"] = "orange"

    my_config_class = MyConfigClass()
    assert(my_config_class.foo == "orange")
    assert(my_config_class.bar == 7)
    assert(my_config_class.baz == True)

def test_with_constructor_args():
    my_config_class = MyConfigClass(foo="grape", bar=8, baz=False)

    assert(my_config_class.foo == "grape")
    assert(my_config_class.bar == 8)
    assert(my_config_class.baz == False)

@retain_sys_args
@retain_environ
def test_with_all_three():
    sys.argv = [sys.argv[0], '--baz']
    os.environ["BAR"] = "9"
    my_config_class = MyConfigClass(foo="pear")

    assert(my_config_class.foo == "pear")
    assert(my_config_class.bar == 9)
    assert(my_config_class.baz == True)
