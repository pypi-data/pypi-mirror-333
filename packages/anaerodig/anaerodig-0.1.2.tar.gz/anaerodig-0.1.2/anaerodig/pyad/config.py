"""Type hint for DigesterConfig"""
from typing import Optional, Protocol


class DigesterConfig(Protocol):
    """Digester Configuration protocol and type hint. A Digester Configuration must have a save and load function"""

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save DigesterConfig at 'name' in 'directory'"""

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load DigesterConfig 'name' from 'directory'"""
