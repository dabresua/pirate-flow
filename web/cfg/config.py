import os
from typing import Any, Type, TypeVar

# TODO: enable loading from file or dotenv

# This is the config definition
# All property that need to be accessible through config must be specified here
_CONFIG_DEF = {
    "LISTEN_ADDR": {
        "default_value": "0.0.0.0"
    },
    "PORT": {
        "default_value": 8080,
        "type": int
    },
    "DEBUG": {
        "default_value": False,
        "type": bool
    },
    "DEV_THREADED": {
        "default_value": False,
        "type": bool
    },
    "DOWNLOADS": {
        "default_value": "../Downloads"
    }
}

R = TypeVar('R')

class Config:
    """Config engine that give and access to get upload, get optional config, mandatory config props, etc.

    Implementation is based on __dict__ internal, then you can access to config properties using config as object.

    Parameters
    ----------
    default_definition : optional
        Definition of the config properties available

        Default value is loaded from `_CONFIG_DEF`

        Next example define a mandatory boolean variable and a optional string config prop with 0.0.0.0` as default
        value

            {
                "DEBUG": {
                    "type": bool
                },
                "LISTEN_ADDR": {
                    "default_value": "0.0.0.0"
                }
            }

    Examples
    --------
        app = Config()
        print(app.PORT)
        print(app.get('OTHER_PROP', "foo_bar")) # Returns 'foo_bar' it OTHER_PROP was not defined

    Use app.props() to get all available properties
    """

    def __init__(self, default_definition: dict = _CONFIG_DEF):
        self.__dict__ = {}
        self._default_definition = default_definition
        self.config_loaded = False

    def load(self) -> None:
        """ Load the configuration parameters
        """

        for name in self._default_definition:
            self._load_prop(name, self._default_definition[name])
        self.config_loaded = True

    def _load_prop(self, name, definition) -> None:
        value = None
        env_var_name = f"{name.upper()}"
        if 'default_value' in definition:
            mandatory = False
    
        th_type = str
        if 'type' in definition:
            th_type = definition['type']

        env_var_present = env_var_name in os.environ
        if mandatory and not env_var_present:
            raise EnvironmentError(f"Mandatory property {name} was not defined. Expected environment variable: {env_var_name}")
        elif env_var_present:
             value = self._typed_data(os.environ[env_var_name], th_type)
        else:
            value = definition['default_value']

        self.__dict__[name] = value

    def _typed_data(self, value: str, th_type: Type[R]) -> R:
        if th_type == str:
            return value
        elif th_type == bool:
            return value.lower() in ["yes", "true", "1"]
        else:
            return th_type(value)
