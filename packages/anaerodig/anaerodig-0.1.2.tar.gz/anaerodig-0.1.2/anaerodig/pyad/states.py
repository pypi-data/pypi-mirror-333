"""Type hint for DigesterStates and DigesterState"""
from typing import Optional, Protocol


class DigesterState(Protocol):
    """Digester State protocol and type hint.
    A Digester State must have a save and load function"""

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save DigesterState at 'name' in 'directory'"""

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load DigesterState 'name' from 'directory'"""


class DigesterStates(Protocol):
    """Digester States protocol and type hint.
    A Digester States must have a save and load function"""

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save DigesterStates at 'name' in 'directory'"""

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load DigesterStates 'name' from 'directory'"""

    def __len__(self) -> int:
        pass
