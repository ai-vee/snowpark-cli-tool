import dataclasses
import sys
import types
import os
from typing import List, Tuple

from aivee_dev_tools.files import load_file_as_text
from aivee_dev_tools.path_management import  find_paths, make_absolute_path_from_root
from aivee_dev_tools.exceptions import ValidationError
from aivee_dev_tools.logger import Logger
from aivee_dev_tools.import_ import import_module

logger = Logger.logger

def resolve_path(
    scope: list,
    node_name: str = None
) -> types.ModuleType:
    
    # get all path matches
    abs_module_files = find_paths(
        within_relative_paths=scope,
        file_pattern=f'*{node_name}.py'
        )
    
    
    match_count = len(abs_module_files)
    if match_count:
        if match_count > 1:
            msg = f'Duplicated nodes are not allowed. {node_name}'
            raise ValidationError(msg)
        else:
            return abs_module_files[0]['abs_file_path']
    else:
        msg = f"No node matches '{node_name}'"
        raise ValidationError(msg)


class Node():
    def __init__(self, node_scope, node_name):
        self.node_scope = node_scope
        self.node_name = node_name
    
    @property
    def node_abs_path(self) -> str:
        return resolve_path(self.node_scope, self.node_name)


def get_all_imports_from_a_parent_node(node: Node) -> List[Tuple]:
    imports_ = []
    
    def get_imports(node: Node):
        node = import_module(
            module_name = node.node_name,
            module_file = node.node_abs_path
        )
        try:
            imports = node.config['imports']
            print('Node: ', node.node_name)
            print('Imports: ', imports)
            for import_, import_path in imports:
                # print(import_, import_path)
                # todo: remove hardcorded procedures
                abs_import = make_absolute_path_from_root(
                    f"procedures/{import_}"
                )
                imports_.append((abs_import, import_path))
                print('Appended', imports_)
                new_node_name = os.path.basename(import_)
                new_node = Node(node.node_scope, new_node_name)
                get_imports(new_node)
                
        except AttributeError:
            pass

    get_imports(node)
    # print(imports_)
    return imports_

# node = import_node(
#     module_name = 'my_custom_module',
#     module_file = r'json_unpacker\expand_object_subfields.py'
# )
# print(node.config)

# find_abs_module_files = find_paths(file_pattern=f'*expand_object_subfields*.py')