from __future__ import annotations
from pathlib import Path
import shutil
import typing as t
from urllib.parse import urlencode

import toml

from quickclone.remote.locators import LocatorBuilder
from .common import DEFAULTS_FOLDER, USER_CONFIG_FILE


class Configurator(object):
    """
    A wrapper around a configuration file meant for QuickClone. This class
    has special methods for retrieving nested items.
    """
    
    def __init__(self, configuration: t.Mapping[str, t.Any]) -> None:
        self.configuration = configuration
    
    def __getitem__(self, key: t.Union[str, t.Iterable[str]]) -> t.Any:
        if type(key) == str:
            return self.configuration.get(key)
        container = self.configuration
        for part in key:
            container = container.get(part)
            if container is None:
                return ""
        return container if container is not None else ""
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(configuration={self.configuration})"
    
    def from_dotted_string(self, key: str) -> t.Optional[t.Any]:
        """
        Retrieve an item using a dot-separated key.
        
        Parameters
        ----------
        key: str
            The dot-separated key to the item.
        
        Returns
        -------
        Any
            The item associated with the key.
        """
        return self[key.split(".")]
    
    def to_locator_builder(self) -> LocatorBuilder:
        """
        Create a `LocatorBuilder` from the configs stored in this object.
        
        Returns
        -------
        LocatorBuilder
            The final `LocatorBuilder` object.
        """
        scheme = self.from_dotted_string("options.remote.scheme")
        host = self.from_dotted_string("options.remote.host")
        username = self.from_dotted_string("options.remote.username")
        password = self.from_dotted_string("options.remote.password")
        if password != "":
            print("I might remove passwords because it's a safety hazard.")
        port = self.from_dotted_string("options.remote.port")
        base_path = self.from_dotted_string("options.remote.base_path")
        path = self.from_dotted_string("options.remote.path")
        query = self.from_dotted_string("options.remote.query")
        fragment = self.from_dotted_string("options.remote.fragment")
        if type(query) == dict:
            query = urlencode(query)
        return LocatorBuilder(
            scheme=scheme,
            host=host,
            username=username,
            password=password,
            port=port,
            base_path=base_path,
            path=path,
            query=query,
            fragment=fragment
        )
    
    def to_string(self, *args, **kwargs) -> str:
        """
        Dump the configuration into a string.
        
        Parameters
        ----------
        *args
            Extra arguments to be passed into toml.dumps().
        
        **kwargs
            Extra arguments to be passed into toml.dumps().
            
        Returns
        -------
        str
            Configuration as a string.
        """
        return toml.dumps(self.configuration, *args, **kwargs)

    def to_file(self, path: Path, *args, **kwargs) -> None:
        """
        Save the configuration to a file.
        
        Parameters
        ----------
        path: Path
            Path to the configuration file.
        
        *args
            Extra arguments to be passed into toml.dump().
        
        **kwargs
            Extra arguments to be passed into toml.dump().
        
        Returns
        -------
        None
        """
        with path.open("w") as f:
            toml.dump(self.configuration, f, *args, **kwargs)
    
    @classmethod
    def from_file(cls, path: Path, *args, **kwargs) -> Configurator:
        """
        Load the configuration from a file.
        
        Parameters
        ----------
        path: Path
            Path to the configuration file.
        
        *args
            Extra arguments to be passed into toml.load().
        
        **kwargs
            Extra arguments to be passed into toml.load().
        
        Returns
        -------
        Configurator
            The configuration loaded from the file stored as a `Configurator`
            object.
        """
        configuration = toml.load(path, *args, **kwargs)
        return cls(configuration)

DEFAULT_CONFIG_FILE: Path = DEFAULTS_FOLDER / "quickclone.toml"
"""
Path to default configs.
"""

DEFAULT_CONFIGURATION = Configurator.from_file(DEFAULT_CONFIG_FILE)
"""
An object storing the default configs for QuickClone.
"""


class SmartConfigurator(Configurator):
    """
    A child class of `Configurator` which can grab missing config items
    from `DEFAULT_CONFIGURATION`.
    """
    
    def __getitem__(self, key: t.Union[str, t.Iterable[str]]) -> t.Any:
        result = super().__getitem__(key)
        if result == "":
            return DEFAULT_CONFIGURATION[key]
        else:
            return result


def load_user_config(path: t.Optional[Path] = None) -> SmartConfigurator:
    """
    Load the user's config. If no config file is found, an empty
    `SmartConfigurator` will be returned and the defaults stored in
    `DEFAULT_CONFIGURATION` will be used instead.
    
    Parameters
    ----------
    path: Optional[Path] = None
        Path to the user's config files. The default argument should not be
        overridden unless necessary. If path is `None`, this function will
        try to look for the file at `USER_CONFIG_FILE`.
    
    Returns
    -------
    SmartConfigurator
        The user's configuration.
    """
    path = USER_CONFIG_FILE if path is None else path
    if path.exists() and path.is_file():
        return SmartConfigurator.from_file(path)
    else:
        return SmartConfigurator({})


def init_user_config_file() -> int:
    """
    Create '~/.config/quickclone.toml' if it does not exist.
    
    Returns
    -------
    status: int
        The status code indicates what operation was performed.
        0: '~/.config/quickclone.toml` detected, nothing has to be done.
        1: User doesn't want to create '~/.config/quickclone.toml'.
        2: '~/.config/quickclone.toml' created.
    """
    if USER_CONFIG_FILE.exists():
        return 0
    print(
        f"QuickClone couldn't find '{USER_CONFIG_FILE}'. "
        f"Do you want to create it now?"
    )
    answer = ""
    while True:
        answer = input("[Y/n] ==> ")
        if answer.lower() in {"y", "n", ""}:
            answer = answer.lower()
            break
        else:
            print(f"Invalid answer: {answer}")
    if answer == "y":
        print(f"Copying '{DEFAULT_CONFIG_FILE}' to '{USER_CONFIG_FILE}'...")
        shutil.copy2(DEFAULT_CONFIG_FILE, USER_CONFIG_FILE)
        print("Done!")
        return 2
    else:
        print(f"Not creating '{USER_CONFIG_FILE}'!")
        return 1
