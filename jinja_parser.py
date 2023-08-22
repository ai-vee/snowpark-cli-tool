import json
import os
from jinja2 import Environment, FileSystemLoader
from .exceptions import ParsingError


class JinjaEnvironment():
    _environment = Environment()
    
    def _env_var(x: str):
        try:
            return os.getenv(x)
        except:
            msg = f"Failed to import environment variables."
            raise ParsingError(msg)
        
    @classmethod
    def parse(cls, str_stream: str = None, **kwargs) -> str:
        content = str_stream
        parsed_content = JinjaEnvironment._environment.from_string(content).render(**kwargs)
        return parsed_content
    
    @classmethod
    def parse_to_obj(cls, str_stream: str = None, **kwargs) -> dict:
        stream = cls.parse(str_stream, **kwargs)
        obj = json.loads(stream)
        return obj
    
    _environment.globals['env_var'] =  _env_var
    _environment.globals['is_empty'] = lambda x: True if x is None or len(x) == 0 else False
    
# env = Environment(loader=FileSystemLoader('input'))
# env.compile_templates('target', zip=None)