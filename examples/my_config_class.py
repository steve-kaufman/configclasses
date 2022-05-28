from configclasses import configclass

@configclass
class MyConfigClass:
    """Example config class"""
    foo: str
    bar: int
    baz: bool

if __name__ == "__main__":
    MyConfigClass()