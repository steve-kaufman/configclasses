from typing import Type, TypeVar

class ConfigType:
    _primitive: type
    _parser_args: list[str]
    _parser_kwargs: dict
    _env_var: str

def cfgtype(primitive: type, parser_args: list[str] = None, parser_kwargs: dict = None, env_var: str = None) -> type:
    """Creates a custom type with the provided metadata, where:
        (primitive) is the intended type of the class field,
          - *required*
        (parser_args) is a list of args to pass to parser.add_argument(),
          - defaults to ['--field-name'] where the field is called `field_name`
        (parser_kwargs) is a dict of kwargs to pass to parser.add_argument(),
          - defaults to {"dest": "field_name", type=primitive}, unless
            primitive is bool: {"dest": "field_name", action="store_true"};
            this makes bools behave like flags instead of values
        (env_var) is a custom environment variable at which to find the value
          - defaults to FIELD_NAME where the field is called `field_name`
    """
    type_name = f"Config{primitive.__name__.capitalize()}"
    base_types = (ConfigType,)
    namespace = dict(
        _primitive=primitive,
        _parser_args=parser_args, 
        _parser_kwargs=parser_kwargs, 
        _env_var=env_var
    )
    return type(type_name, base_types, namespace)
    
