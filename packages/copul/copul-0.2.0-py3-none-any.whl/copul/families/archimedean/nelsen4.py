import numpy as np
import sympy

from copul.families.archimedean.archimedean_copula import ArchimedeanCopula
from copul.families.other.independence_copula import IndependenceCopula
from copul.wrapper.cdf_wrapper import CDFWrapper
from copul.wrapper.sympy_wrapper import SymPyFuncWrapper


class GumbelHougaard(ArchimedeanCopula):
    ac = ArchimedeanCopula
    theta = sympy.symbols("theta", positive=True)
    theta_interval = sympy.Interval(1, np.inf, left_open=False, right_open=True)
    special_cases = {1: IndependenceCopula}

    @property
    def is_absolutely_continuous(self) -> bool:
        return True

    @property
    def _generator(self):
        return (-sympy.log(self.t)) ** self.theta

    @property
    def inv_generator(self):
        gen = sympy.exp(-(self.y ** (1 / self.theta)))
        return SymPyFuncWrapper(gen)

    @property
    def cdf(self):
        if self.u == 0 or self.v == 0:
            return SymPyFuncWrapper(0)
        gen = sympy.exp(
            -(
                (
                    (-sympy.log(self.u)) ** self.theta
                    + (-sympy.log(self.v)) ** self.theta
                )
                ** (1 / self.theta)
            )
        )
        return CDFWrapper(gen)

    def lambda_L(self):
        return 0

    def lambda_U(self):
        return 2 - 2 ** (1 / self.theta)


Nelsen4 = GumbelHougaard

# B6 = GumbelHougaard
