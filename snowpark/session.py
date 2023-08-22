import snowflake.snowpark as snowpark
from ..snowpark.connection import SnowflakeConnectionCredentials 

class Session_:
    @classmethod
    def get_or_create(
        cls, 
        conn_creds: SnowflakeConnectionCredentials
    ) -> snowpark.Session:
        return snowpark.Session.builder.configs(conn_creds).getOrCreate()