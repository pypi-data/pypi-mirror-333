from random import choice
from typing import List

from ga4qc.circuit import Circuit
from .interface import ISelection


class BestSelection(ISelection):

    def select(self, circuits: List[Circuit], k: int, generation: int) -> List[Circuit]:
        sorted_circuits = sorted(
            circuits, key=lambda circuit: circuit.fitness_values[0]
        )

        selection = [circuit.copy() for circuit in sorted_circuits[:k]]
        return selection
