from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name="aivee_dev_tools",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "snowflake-connector-python",
        "snowflake-snowpark-python",
        "snowflake-snowpark-python[pandas]",
        "colorlog",
        "click",
        "jinja2"
    ],
    entry_points={
        "console_scripts": [
            "snowtools=aivee_dev_tools.snowpark.cmd:debug"
        ]
    }
)
