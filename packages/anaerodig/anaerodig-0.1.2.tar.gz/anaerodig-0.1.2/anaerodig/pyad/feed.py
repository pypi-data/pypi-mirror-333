"""Type hint for DigesterFeed"""
from typing import Optional, Protocol


class DigesterFeed(Protocol):
    """Digester Feed protocol and type hint. A Digester Feed must have a save and load function"""

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save DigesterFeed at 'name' in 'directory'"""

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load DigesterFeed 'name' from 'directory'"""
