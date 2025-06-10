from dataclasses import dataclass

from model.sighting import Sighting


@dataclass

class Arco():
    Sighting1: Sighting
    Sighting2: Sighting
    peso = float


    def __str__(self):
        return f"{self.Sighting1} - {self.Sighting2}"

    def __hash__(self):
        return hash((self.Sighting1, self.Sighting2))