from argparse import ArgumentParser, Namespace
from dataclasses import Field, dataclass, fields
import os
from .configtype import *

def configclass(cls: type):
    """Class annotation that extends dataclass and provides automatic
    configuration via CLI arguments, environment variables, or plain old
    constructor arguments, in that order."""

    dataclass(cls) # make it a dataclass

    # Override __init__() method
    def init_wrapper(self, **constructor_kwargs):
        # Initialize argparse and define CLI bindings for each class field
        parser = ArgumentParser(description=(cls.__doc__ or cls.__name__))
        for field in fields(cls):
            _setup_field(field, parser)
        cli_args = parser.parse_args()

        # Try to get each class field from the provided config
        for field in fields(cls):
            field_value = _get_field_value(field, constructor_kwargs, cli_args)
            # Make sure there's either a provided value or a default
            if field_value == None and not hasattr(self, field.name):
                raise Exception(f"No configuration for {field.name}!")
            setattr(self, field.name, field_value)

    cls.__init__ = init_wrapper
    return cls

def _setup_field(field: Field, parser: ArgumentParser):
    # Use custom type, even if primitive is provided
    if not issubclass(field.type, ConfigType):
        field.type = cfgtype(field.type)
    config = field.type

    parser_args = config._parser_args if config._parser_args else [f"--{field.name.replace('_','-')}"]
    parser_kwargs = {"dest": field.name}

    _add_defaults(config._primitive, parser_kwargs)
    if config._parser_kwargs:
        parser_kwargs.update(config._parser_kwargs) # override default config

    parser.add_argument(*parser_args, **parser_kwargs)

def _add_defaults(type: type, parser_kwargs: dict):
    if type == bool:
        parser_kwargs["action"] = "store_true"
    else:
        parser_kwargs["type"] = type

def _get_field_value(field: Field, constructor_kwargs: dict, cli_args: Namespace) -> any:
    # Check Constructor
    if field.name in constructor_kwargs.keys():
        return constructor_kwargs[field.name]

    # Check CLI Args
    arg_value = getattr(cli_args, field.name)
    if arg_value:
        return arg_value

    # Check Env. Vars
    try:
        env_value = field.type._primitive(os.environ.get(field.type._env_var or field.name.upper()))
    except ValueError:
        raise Exception(f"{field.name.upper()}: expected type {field.type.__name__}")
    if env_value:
        return env_value

    return None
