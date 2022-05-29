from typing import Any

class ConfigType:
    _primitive: type
    _cli_args: list[str]
    _cli_kwargs: dict[str, Any]
    _env_var: str

def cfgtype(primitive: type, cli_args: list[str] = None, env_var: str = None, **cli_kwargs) -> type:
    """Creates a custom type with the provided metadata, where:
        - `primitive`: The primitive type that you would like the field to 
            be. This is explicitly called 'primitive' and not 'type', because it's not 
            really possible to derive a class from string input. You can still have 
            complex types in your `configclass`, but you'll always need to pass them in 
            the constructor.
            - **required**
        - `cli_args`: The various names for this field in the command
            line interface.
            - ex: `['--foo', 'f', '--my-foo]`
            - defaults to `['--field-name']` where the field is called `field_name`
        - `env_var`: The name for this field's environment variable
            - defaults to `FIELD_NAME` where the field is called `field_name`
        - `**kwargs`: passed directly to `parser.add_argument()`;
            using the `argparse`(https://docs.python.org/3/library/argparse.html)
            library.
            - ex: `cfgtype(str, help="Help text for this argument" default="some default 
            value")`
            - defaults to: `{"type": <primitive>}`, unless primitive is `bool`; then the
            default is: `{"action": "store_true"}`. This makes bools behave like flags
            and not values, which is generally more intuitive.
    """
    type_name = f"Config{primitive.__name__.capitalize()}"
    base_types = (ConfigType,)
    namespace = dict(
        _primitive=primitive,
        _cli_args=cli_args,
        _cli_kwargs=cli_kwargs,
        _env_var=env_var
    )
    return type(type_name, base_types, namespace)
    
