from os import getenv

# Environment variable error class
class EnvironmentVariableNotDefined(Exception):
    """An error specification.
    This is thrown when an environment variable is required and expected to be
    defined, pre-launch, but is not defined.

    Attributes
    ---------
    required : Required variable
        The environment variable that was expected to be defined but was missing.
    """
    def __init__(self, name: str, required: bool = True):
        super().__init__('Environment variable not defined: ' + name)
        self.required = required

# PSQL constants
PSQL_USERNAME = ('PSQL_USERNAME')
PSQL_PASSWORD = ('PSQL_PASSWORD')
