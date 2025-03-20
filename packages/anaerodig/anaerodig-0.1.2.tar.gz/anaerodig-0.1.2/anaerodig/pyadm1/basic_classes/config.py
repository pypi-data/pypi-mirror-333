"""
ADM1 Digester Configuration class.

The necessary information about the digester configuration for the ADM1 routine to work is the
liquid phase volume, gas phase volume and Temperature.

The digester information can be loaded from a json file using load_dig_info.
The digester information can be saved to a json file using the .save method.
"""
from typing import Optional

from apicutils.basic_io import combine_to_path, rw_jsonlike

class NegativeVolume(Exception):
    def __init__(self, volume):
        self.volume = volume
        super().__init__(f"Got negative volume: {self.volume}")

class ADM1Config:
    """
    ADM1 Digester Configuration.

    Initialisation:
    Args:
        V_liq: volume of liquid phase (in m3)
        V_gas: volume of gas phase (in m3)
    """

    def __init__(self, V_liq: float, V_gas: float):
        if V_liq < 0:
            raise NegativeVolume(V_liq)
        if V_gas < 0:
            raise NegativeVolume(V_gas)

        self.V_liq = float(V_liq)
        self.V_gas = float(V_gas)

    @property
    def V_liq(self) -> float:
        """Liquid volume (in m3)"""
        return self._V_liq

    @V_liq.setter
    def V_liq(self, val):
        x = float(val)
        if x <= 0.0:
            raise ValueError(f"V_liq should be positive (passed {x})")
        self._V_liq = x

    @property
    def V_gas(self) -> float:
        """Gas volume (in m3)"""
        return self._V_gas

    @V_gas.setter
    def V_gas(self, val):
        x = float(val)
        if x <= 0.0:
            raise ValueError(f"V_gas should be positive (passed {x})")
        self._V_gas = x

    def as_dict(self) -> dict[str, float]:
        """View of Digester Info as a dictionnary"""
        return {
            "V_liq": self.V_liq,
            "V_gas": self.V_gas,
        }

    def save(self, name: str, directory: Optional[str] = None) -> str:
        """Save ADM1Config object to .json file 'name' in 'directory'"""

        path = combine_to_path(name, rw_jsonlike.ext, directory)
        rw_jsonlike.save(path, self.as_dict())
        return path

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load ADM1Config from 'name' in 'directory'"""
        return cls(
            **rw_jsonlike.load(combine_to_path(name, rw_jsonlike.ext, directory))
        )

    def __str__(self):
        return str.join(
            "\n",
            [
                f"Liquid volume: {self.V_liq} m3",
                f"Gas volume: {self.V_gas} m3",
            ],
        )

    def __repr__(self):
        return str.join(
            "\n",
            [
                f"Liquid volume: {self.V_liq} m3",
                f"Gas volume: {self.V_gas} m3",
            ],
        )
