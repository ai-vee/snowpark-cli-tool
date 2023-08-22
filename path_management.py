import fnmatch
import json
import os
import re
from typing import Optional, List

from aivee_dev_tools.logger import Logger

logger = Logger.logger

def find_paths(
    root: str = None,
    within_relative_paths: Optional[List[str]] = None,
    file_pattern: str = None
):
  
    """
    Find all paths (wiwtin the relative paths, if given) and match the provided pattern
    """
    matches = list()
    #return normalised path for the current os
    # / for unix, \ for windows
    root = os.path.normpath(root or os.getcwd()) 
    re_pattern = fnmatch.translate(file_pattern)
    path_containers = within_relative_paths or [root]
    
    for rel_container_path in path_containers:
        abs_container_path = os.path.join(root, rel_container_path)
        for root, subdirs, files in os.walk(abs_container_path):
            for file in files:
                abs_file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(abs_file_path,rel_container_path)
                if re.compile(re_pattern).match(rel_file_path):
                    matches.append(
                        {
                            "container": rel_container_path,
                            "abs_file_path": abs_file_path,
                            "rel_file_path": rel_file_path 
                        }
                    )
    
    logger.debug('Targets: %s', json.dumps(matches, indent=4, separators=(',', ': ')))
    return matches

def make_absolute_path_from_root(path_to_resolve: str, root: str = None) -> str:
    """
    If path-to_resolve is a relative path, create an absolute path
    with root as the base.

    If path_to_resolve is an absolute path or a user path (~), just
    resolve it to an absolute path and return.
    """
    root = os.path.normpath(root or os.getcwd())
    return os.path.abspath(os.path.join(root, os.path.expanduser(path_to_resolve)))



# find_paths(None,['aivee_dev_tools'],'*.yml')