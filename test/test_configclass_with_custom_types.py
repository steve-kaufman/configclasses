import os
import sys
from configclasses import configclass
from configclasses.configtype import cfgtype

from .util import retain_environ, retain_sys_args

@configclass
class MyConfigClass1:
    foo: cfgtype(str)
    bar: cfgtype(int)
    baz: cfgtype(bool)

@retain_sys_args
def test_with_no_custom_params():
    sys.argv = [sys.argv[0], '--foo', 'apple', '--bar', '5', '--baz']

    my_class = MyConfigClass1()

    assert(my_class.foo == 'apple')
    assert(my_class.bar == 5)
    assert(my_class.baz == True)

@configclass
class MyConfigClass2:
    foo: cfgtype(str, cli_args=["--my-foo"])
    bar: cfgtype(int, default=6)
    baz: cfgtype(bool, cli_args=["-b"])

@retain_sys_args
def test_with_custom_cli_config():
    sys.argv = [sys.argv[0], '--my-foo', 'banana', '-b']

    my_class = MyConfigClass2()

    assert(my_class.foo == 'banana')
    assert(my_class.bar == 6)
    assert(my_class.baz == True)

@configclass
class MyConfigClass3:
    foo: cfgtype(str, env_var="MY_FOO")
    bar: cfgtype(int, env_var="MY_BAR")
    baz: cfgtype(bool, env_var="MY_BAZ")

@retain_environ
def test_with_custom_env_config():
    os.environ["MY_FOO"] = "orange"
    os.environ["MY_BAR"] = "7"
    os.environ["MY_BAZ"] = "true"

    my_class = MyConfigClass3()

    assert(my_class.foo == "orange")
    assert(my_class.bar == 7)
    assert(my_class.baz == True)

@configclass
class MyConfigClass4:
    foo: cfgtype(str, cli_args=["--my-foo"])
    bar: cfgtype(int, env_var="MY_BAR")
    baz: cfgtype(bool, cli_args=["-b"])

@retain_environ
@retain_sys_args
def test_with_custom_env_and_cli_config():
    sys.argv = [sys.argv[0], '--my-foo', 'lemon', '-b']
    os.environ["MY_BAR"] = "8"

    my_class = MyConfigClass4()

    assert(my_class.foo == "lemon")
    assert(my_class.bar == 8)
    assert(my_class.baz == True)

def test_with_constructor_args():
    my_class = MyConfigClass4(foo="lime", bar=9, baz=False)

    assert(my_class.foo == "lime")
    assert(my_class.bar == 9)
    assert(my_class.baz == False)
