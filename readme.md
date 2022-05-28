# Configclasses

The `@configclass` decorator works very much like the built-in `@dataclass`
decorator, with the additional functionality that it will automatically
retrieve values from either the command line, environment variables, or from
the constructor!

## Examples:
Here's some simple default behavior. Let's call the following class
`my_config_class.py`:

```python
from configclasses import configclass

@configclass
class MyConfigClass:
    foo: str
    bar: int,
    baz: bool

my_config_class = MyConfigClass()
print(my_config_class.foo)
print(my_config_class.bar)
print(my_config_class.baz)
```
And let's run it like this:
```bash
$ python my_config_class.py --foo apple --bar 5 --baz
```
Expected output:
```
apple
5
True
```

With environment variables:
```
$ FOO=banana BAR=6 BAZ=true python my_config_class.py
```
Expected output:
```
banana
6
True
```
<br>

Note, however, that the default behavior of a bool is to act as a flag, so any
value input to the $BAZ environment variable will result in the bool being true:
```
$ FOO=banana BAR=6 BAZ=false python my_config_class.py
```
Expected output:
```
banana
6
True
```

## Custom Config Types

The configclasses module provides some additional types that will allow you to
customize your configuration beyond the default. 

As shown in the above examples,
the default behavior is to accept a command line argument that is the same as
the field name but with hyphens instead of underscores, or an environment
variable that is the same as the field name but in all caps.

Currently there are three custom types supported: `ConfigBool`, `ConfigInt`, and
`ConfigStr`.
For each of these, there's a utility function for generating the type based on
some custom configuration: `cfgbool()`, `cfgint()`, and `cfgstr()` respectively.

### Configuring With the Utility Functions:

Here's another version of `my_config_class.py`:
```python
from configclasses import configclass, cfgbool, cfgint, cfgstr

@configclass
class MyConfigClass:
    foo: cfgstr(env_var="MY_FOO", parser_args=["--my-foo"])
    bar: cfgint(parser_kwargs={"default": 7})
    baz: cfgbool(env_var="SHOULD_BAZ", parser_args=["-b", "--should-baz"])

my_config_class = MyConfigClass()
print(my_config_class.foo)
print(my_config_class.bar)
print(my_config_class.baz)
```
Let's run it:
```
$ python my_config_class --my-foo apple -b
```
Expected Output:
```
apple
7
True
```
The `parser_args` and `parser_kwargs` arguments correspond to the args and
kwargs passed to `parser.add_argument()` with the 
[**`argparse`**](https://docs.python.org/3/library/argparse.html) library. 