import numpy as np
import sympy

from copul.families.archimedean.archimedean_copula import ArchimedeanCopula
from copul.families.other.pi_over_sigma_minus_pi import PiOverSigmaMinusPi
from copul.wrapper.sympy_wrapper import SymPyFuncWrapper


class Nelsen12(ArchimedeanCopula):
    ac = ArchimedeanCopula
    theta = sympy.symbols("theta", positive=True)
    theta_interval = sympy.Interval(1, np.inf, left_open=False, right_open=True)
    special_cases = {1: PiOverSigmaMinusPi}

    @property
    def is_absolutely_continuous(self) -> bool:
        return True

    @property
    def _generator(self):
        return (1 / self.t - 1) ** self.theta

    @property
    def inv_generator(self):
        gen = 1 / (self.y ** (1 / self.theta) + 1)
        return SymPyFuncWrapper(gen)

    @property
    def cdf(self):
        cdf = (
            1
            + ((self.u ** (-1) - 1) ** self.theta + (self.v ** (-1) - 1) ** self.theta)
            ** (1 / self.theta)
        ) ** (-1)
        return SymPyFuncWrapper(cdf)

    def lambda_L(self):
        return 2 ** (-1 / self.theta)

    def lambda_U(self):
        return 2 - 2 ** (1 / self.theta)
