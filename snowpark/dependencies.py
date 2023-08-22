import os
from aivee_dev_tools.import_ import import_module
from aivee_dev_tools.snowpark.node import Node
from aivee_dev_tools.path_management import make_absolute_path_from_root


def recursively_get_all_imports(node: Node):
    imports_ = []
    
    def get_imports(_node: Node):
        module = import_module(
            module_name = _node.node_name,
            module_file = _node.node_abs_path
        )
        imports = []
        try:
            imports = module.config['imports']
        except AttributeError:
            print(f'No imports config at {_node.node_name}')

        for import_, import_path in imports:
            # todo: remove hardcorded procedures
            abs_import = make_absolute_path_from_root(
                f"procedures/{import_}"
            )
            imports_.append((abs_import, import_path))
            print('Appended', imports_)
            new_node_name = os.path.basename(import_).replace('.py','')
            new_node = Node(_node.node_scope, new_node_name)
            get_imports(new_node)
    
    get_imports(node)
    return imports_ 