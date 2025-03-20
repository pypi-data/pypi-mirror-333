"""Abstract Base Class for Anaerobic Digester Model."""
import os
from abc import ABC, abstractmethod
from typing import Optional

from anaerodig.pyad.config import DigesterConfig
from anaerodig.pyad.feed import DigesterFeed
from anaerodig.pyad.states import DigesterState, DigesterStates
from apicutils.basic_io import combine_to_path

class NoObservationError(Exception):
    """Exception class when trying to evaluate a method requiring
    observations on an AnaerobicDigesterModel instance with no
    obs field"""

class AnaerobicDigesterModel(ABC):
    """Abstract Base Class for Anaerobic Digester Model.
    AnaerobicDigesterModel class organizes the data in:
    - Feed data
    - Initial state data
    - Configuration data
    - An optional Observation data (necessary for calibration)
    """

    def __init__(
        self,
        dig_config: DigesterConfig,
        feed: DigesterFeed,
        ini_state: DigesterState,
        obs: Optional[DigesterStates] = None,
    ):
        self.dig_config = dig_config
        self.feed = feed
        self.ini_state = ini_state
        self.obs = obs

    def has_obs(self) -> bool:
        """Return True if observation data is present"""
        return self.obs is not None

    @abstractmethod
    def simulate(self, param) -> DigesterStates:
        """Simulate digester behavior"""

    def score(self, param) -> float:
        """Score a parameter simulation"""
        preds = self.simulate(param)
        return self.error(preds)

    @abstractmethod
    def error(self, predictions: DigesterStates) -> float:
        """Compute error between predictions and observations"""

    FEED_PATH = "FEED"
    DIG_CONFIG_PATH = "DIG_CONFIG"
    INI_STATE_PATH = "INI_STATE"
    OBS_PATH = "OBS"

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save digester to file"""
        path = combine_to_path(name, "", directory)
        os.makedirs(path, exist_ok=True)

        self.feed.save(self.FEED_PATH, directory=path)
        self.dig_config.save(self.DIG_CONFIG_PATH, directory=path)
        self.ini_state.save(self.INI_STATE_PATH, directory=path)

        if self.has_obs():
            self.obs.save(self.OBS_PATH, directory=path)

        return path

    @classmethod
    @abstractmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load Digester object from name in directory"""
