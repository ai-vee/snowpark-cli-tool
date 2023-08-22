import os
from typing import Any, Dict
from ..snowpark.connection import SnowflakeConnectionCredentials
from ..yaml_data import YamlData
from ..jinja_parser import JinjaEnvironment
from ..exceptions import ContentError, ValidationError
from dataclasses import dataclass, asdict

@dataclass
class TargetProfile():
    target_name: str
    credentials: SnowflakeConnectionCredentials
    
    def __dict__(self):
        return asdict(self)

@dataclass
class ProfilesConfig():
    default: str
    targets: Dict[str, TargetProfile] 
    
    def __dict__(self):
        return asdict(self)   


def load_profiles(
    profiles_dir: str
) -> ProfilesConfig:
    abs_path = os.path.join(profiles_dir, "profiles.yml")
    yaml_data = YamlData(abs_path)
    
    parsed_contents = JinjaEnvironment.parse_to_obj(yaml_data.contents, **yaml_data.vars)
    if not parsed_contents:
        msg = f"Empty profiles.yml at {abs_path}."
        raise ContentError
    else:
        try:
            profiles_obj = parsed_contents['profiles']
        except:
            msg = f"Config in profiles.yml is invalid."
            raise ValidationError(msg)
        else:
            profiles = ProfilesConfig(**profiles_obj).__dict__()
            return profiles

def get_target_profile(
    profiles: Dict[str, Any],
    target_name: str = None
) -> TargetProfile:
    target_name = target_name or profiles.get('default')
    if not target_name:
        msg = 'Please provide a target name or speicfy a default target name in profiles.yml'
        raise ValidationError(msg)
    else:
        try:
            target_config = profiles['targets'][target_name]
            creds = SnowflakeConnectionCredentials(**target_config)
            target_profile = TargetProfile(target_name, creds).__dict__()
            return target_profile
        except ValidationError as e:
            msg = f"Target {target_name} is not available."
            raise ValidationError(msg) from e