import os

import click
from aivee_dev_tools.snowpark.profile import load_profiles, get_target_profile
from aivee_dev_tools.snowpark.session import Session_

PROJECT_ROOT = os.getcwd()
import sys
sys.path.append(PROJECT_ROOT)

@click.command()
@click.option('--project_root', default = None)
@click.option('--profiles_dir', default = None)
@click.option('--target_name', default = None)
@click.option('--procedure', default = None)
def debug(
    project_root: str,
    profiles_dir: str,
    target_name: str,
    procedure: str
):
    project_root = os.getcwd()
    profiles_dir = project_root
    target_name = None
    profiles = load_profiles(profiles_dir)
    profile = get_target_profile(profiles, target_name)
    
    session = Session_.get_or_create(profile['credentials'])
    
    from aivee_dev_tools.snowpark.tasks.debug import debug
    from aivee_dev_tools.snowpark.node import Node
    
    node = Node(['procedures'], procedure)
    debug(session, node)
    
# debug('unpack_json_document')