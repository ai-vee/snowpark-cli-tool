import json
from .logger import Logger
from .files import load_yaml_safe, load_file_as_text

logger = Logger.logger

class YamlData:
    def __init__(self, path: str, var_key: str = 'vars', **vars):
        self.path = path
        self.vars_ = vars
        self.var_key = var_key
    
    @property
    def obj(self) -> dict:
        text = load_file_as_text(self.path)
        obj = load_yaml_safe(text)
        return obj
    
    @property
    def contents(self):
        return json.dumps(self.obj)
    # load_file_as_text(self.path)
    
    @property
    def vars(self):
        vars_in_contents = self.obj.get(self.var_key)
        # update with given vars
        result = {**vars_in_contents, **self.vars_}
        logger.debug('Config vars: %s', json.dumps(result, indent=4))
        return result

# YamlConfig(r'C:\Users\binhn\.repositories\projects\snowpark_generate_relational_tables_from_nested_JSON\environments.yml', varA = 3, varB=2).vars