import os
import sys

def retain_sys_args(func):
    """Puts sys.argv back the way it was when the function is done"""
    def wrapper(*args, **kwargs):
        old_sys_arg = sys.argv.copy()
        func(*args, **kwargs)
        sys.argv = old_sys_arg
    return wrapper

def retain_environ(func):
    """Puts os.environ back the way it was when the function is done"""
    def wrapper(*args, **kwargs):
        old_environ = os.environ.copy()
        func(*args, **kwargs)
        os.environ = old_environ
    return wrapper