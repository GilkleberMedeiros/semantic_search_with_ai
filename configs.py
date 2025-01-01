import os
import getpass
import json
from pathlib import Path
from typing import TypeVar


AnyEmptyClass = TypeVar("AnyEmptyClass")


class ConfigObj:
    """
    Empty config class to be filled with configs attrs.
    """

__configs: ConfigObj | None = None

def get_configs() -> ConfigObj:
    global __configs

    if __configs:
        return __configs
    
    configs_fp = Path("./configs.json").open()
    configs_dict = json.load(configs_fp)

    __configs = parse_dict_to_obj(ConfigObj, configs_dict)

    return __configs

def get_google_api_key() -> str:
    configs = get_configs()
    GOOGLE_API_KEY = os.environ.get(configs.google_api_key.name, "") # type: ignore

    if not GOOGLE_API_KEY:
        GOOGLE_API_KEY = getpass.getpass("Provide your google ai api key: ")

    return GOOGLE_API_KEY 

def parse_dict_to_obj(cls: type[AnyEmptyClass], d: dict[str, any]) -> AnyEmptyClass:
    """
    Receive a class and a dict.
    If some key in the dict leads to another dict, func will parse the inner dict
    to an second object and assign it to the first object with key as attr name, recursively. 
    Otherwise it will parse key as the name of the object attr and put respective value on it.
    """
    obj = cls()

    for k, v in d.items():
        if isinstance(v, dict):
            inner_obj = parse_dict_to_obj(cls, v)
            setattr(obj, k, inner_obj)
        else:
            setattr(obj, k, v)

    return obj