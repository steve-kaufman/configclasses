from configclasses import configclass
from configclasses.configtype import cfgtype

@configclass
class MyConfigClass:
    """Check out the docstring in the CLI's help output!"""
    foo: cfgtype(str, help="input foo")
    bar: cfgtype(int, help="how many bar to use")
    baz: cfgtype(bool, cli_args=['-b', '--use-baz'], help="enable baz")

if __name__ == "__main__":
    MyConfigClass()