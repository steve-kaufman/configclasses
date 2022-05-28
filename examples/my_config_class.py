from configclasses import configclass

@configclass
class MyConfigClass:
    """Check out the docstring in the CLI's help output!"""
    foo: str
    bar: int
    baz: bool

if __name__ == "__main__":
    MyConfigClass()