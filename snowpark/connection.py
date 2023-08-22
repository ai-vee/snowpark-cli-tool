from dataclasses import dataclass, asdict

@dataclass
class SnowflakeConnectionCredentials:
    account: str
    user: str
    password: str 
    role: str  
    warehouse: str
    database: str
    schema: str
    
    def _connection_dict_config(self):
        return asdict(self)