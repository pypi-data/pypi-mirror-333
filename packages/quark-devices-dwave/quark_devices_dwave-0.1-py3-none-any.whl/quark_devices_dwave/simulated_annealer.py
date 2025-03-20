from dataclasses import dataclass

import dwave.samplers

from quark.protocols import Core

@dataclass
class SimulatedAnnealer(Core):
    """
    A module for solving a qubo problem using simulated annealing

    :param num_reads: The number of reads to perform
    """

    num_reads: int = 100


    def preprocess(self, data: dict) -> None:
        device = dwave.samplers.SimulatedAnnealingSampler()
        self._result = device.sample_qubo(data["Q"], num_reads=self.num_reads)

    def postprocess(self, data: None) -> dict:
        return self._result.lowest().first.sample # type: ignore
