from dataclasses import dataclass

class ConfigType:
    _primitive: type
    _parser_args: list[str]
    _parser_kwargs: dict
    _env_var: str

def cfgtype(primitive: type, parser_args: list[str] = None, parser_kwargs: dict = None, env_var: str = None) -> type:
    type_name = f"Config{primitive.__name__.capitalize()}"
    base_types = (ConfigType,)
    namespace = dict(
        _primitive=primitive,
        _parser_args=parser_args, 
        _parser_kwargs=parser_kwargs, 
        _env_var=env_var
    )
    return type(type_name, base_types, namespace)
    
