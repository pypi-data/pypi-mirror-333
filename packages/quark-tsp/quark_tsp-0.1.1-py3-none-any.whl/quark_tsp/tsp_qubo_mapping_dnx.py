from dataclasses import dataclass
from typing import Optional

import networkx as nx
import dwave_networkx as dnx

from quark.protocols import Core

@dataclass
class TspQuboMappingDnx(Core):
    """
    A module for mapping a graph to a QUBO formalism for the TSP problem
    """

    def preprocess(self, data: nx.Graph) -> dict:
        self._graph = data
        q = dnx.traveling_salesperson_qubo(data)
        return {"Q": q}


    def postprocess(self, data: dict) -> Optional[list[int]]:
        relevant_data = filter(lambda x: x[1] == 1, data.items())
        tuples = map(lambda x: x[0], relevant_data)
        sorted_tuples = sorted(tuples, key=lambda x: x[1])
        path = map(lambda x: x[0], sorted_tuples)
        time_steps = map(lambda x: x[1], sorted_tuples)

        if list(time_steps) != list(range(self._graph.number_of_nodes())):
            print("Invalid route")
            return None

        return list(path)
