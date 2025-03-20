"""Dummy configuration for AM2 model simulations. AM2 does not properly require a configuration"""
from typing import Optional

from apicutils.basic_io import combine_to_path, rw_jsonlike


class AM2Config:
    def __init__(self, name: Optional[str] = None):
        self._name = name

    @property
    def name(self):
        return self._name

    def as_dict(self) -> dict[str]:
        return {"name": self._name}

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save ADM1Config object to .json file"""
        path = combine_to_path(name, rw_jsonlike.ext, directory)
        rw_jsonlike.save(path, self.as_dict())
        return path

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Loading method"""
        return cls(
            **rw_jsonlike.load(combine_to_path(name, rw_jsonlike.ext, directory))
        )

    def __str__(self):
        if self._name is None:
            return "Unnamed digester"
        return f"Digester {self._name}"

    def __repr__(self):
        if self._name is None:
            return "Unnamed digester"
        return f"Digester {self._name}"
