import json
from typing import Any, Dict, Optional

import yaml



def load_file_as_text(path: str, *, encoding: str = None, strip: bool = True) -> str:
    content: str
    try:
        with open(path, 'rb',  encoding=encoding) as file:
            content = file.read()
        
        if strip:
            content.strip()
    except FileNotFoundError as fnfe:
        raise fnfe
    except:
        pass
    
    return content

def load_yaml_safe(contents) -> Optional[Dict[str, Any]]:
    return yaml.load(contents, Loader=yaml.SafeLoader)

# def to_yaml(string: str) -> object:
#     try:
#         content = yaml.safe_load(string)
#         return content
#     except yaml.YAMLError as ye:
#         raise ye(f"YAML '{content[:50]}' is invalid with error: {ye}")

# def write_json_file(path, content):
#     with open(path, 'w') as file:
#         json.dump(content, file)
        


