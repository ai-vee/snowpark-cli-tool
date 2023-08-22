import os
import snowflake.snowpark as snowpark
from typing import List, Tuple

# from aivee_dev_tools.snowpark.node import get_all_imports_from_a_parent_node
from aivee_dev_tools.import_ import import_module
from aivee_dev_tools.snowpark.node import Node
from aivee_dev_tools.snowpark.dependencies import recursively_get_all_imports

def debug(
    session: snowpark.Session,
    node: Node
):
    all_imports = recursively_get_all_imports(node)
    print(all_imports)
    for import_ in all_imports:
        session.add_import(*import_)
        
    node = import_module(node.node_name, node.node_abs_path)
    
    node.debug(session=session)
