# Configclasses

The `@configclass` decorator works very much like the built-in `@dataclass`
decorator, with the additional functionality that it will automatically
retrieve values from either the constructor, the command line, environment
variables, or any assigned defaults, in that order!

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

<pre><code>&#36; FOO=banana BAR=6 <span style="color:cyan;">BAZ=false</span> python my_config_class.py</code></pre>

Expected output:
<pre><code>banana
6
<span style="color:cyan">True</span> <span style="color: gray"># still</span>
</code></pre>

## Custom Config Types

The configclasses module provides some additional types that will allow you to
customize your configuration beyond the default. 

As shown in the above examples,
the default behavior is to accept a command line argument that is the same as
the field name but with hyphens instead of underscores, or an environment
variable that is the same as the field name but in all caps.

In order to create a custom type, use the `cfgtype()` utility function. This
function accepts the following arguments:

- `primitive`: ( `type` ) The primitive type that you would like the field to 
    be. This is explicitly called 'primitive' and not 'type', because it's not 
    really possible to derive a class from string input. You can still have 
    complex types in your `configclass`, but you'll always need to pass them in 
    the constructor.
    - **required**
- `cli_args`: ( `list[str]` ) The various names for this field in the command
    line interface.
    - ex: `['--foo', 'f', '--my-foo]`
    - defaults to `['--field-name']` where the field is called `field_name`
- `env_var`: ( `str` ) The name for this field's environment variable
    - defaults to `FIELD_NAME` where the field is called `field_name`
- `**kwargs`: ( `dict[str, Any]` ) passed directly to `parser.add_argument()`;
    using the [**`argparse`**](https://docs.python.org/3/library/argparse.html)
    library.
    - ex: `cfgtype(str, help="Help text for this argument" default="some default 
    value")`
    - defaults to: `{"type": <primitive>}`, unless primitive is `bool`; then the
    default is: `{"action": "store_true"}`. This makes bools behave like flags
    and not values, which is generally more intuitive.

### Configuring With `cfgtype()`:

Here's another version of `my_config_class.py`:
```python
from configclasses import configclass, cfgbool, cfgint, cfgstr

@configclass
class MyConfigClass:
    foo: cfgtype(str, env_var="MY_FOO", cli_args=["--my-foo"])
    bar: cfgtype(int, default=7)
    baz: cfgtype(bool, env_var="SHOULD_BAZ", cli_args=["-b", "--should-baz"])

my_config_class = MyConfigClass()
print(my_config_class.foo)
print(my_config_class.bar)
print(my_config_class.baz)
```
Let's run it:
```
$ python my_config_class.py --my-foo apple -b
```
Expected Output:
```
apple
7
True
```

## Additional Features
### Docstring for help text
In order to customize the help text for the CLI, simply add a docstring to the
config class:
```python
from configclasses import configclass

@configclass
class MyConfigClass:
    """Check out the docstring in the CLI's help output!"""
    foo: str
    bar: int
    baz: bool

if __name__ == "__main__":
    MyConfigClass()
```
```
$ python my_config_class.py --help
```
Output:
```
usage: my_config_class.py [-h] [--foo FOO] [--bar BAR] [--baz]

Check out the docstring in the CLI's help output!

options:
  -h, --help  show this help message and exit
  --foo FOO
  --bar BAR
  --baz
```