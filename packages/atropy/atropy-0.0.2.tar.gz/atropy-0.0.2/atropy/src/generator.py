import math
import os
import sys
import tempfile
import site

import numpy as np
import sympy as sp

import atropy_core_pybind11

from atropy_core.grid import GridParms
from atropy_core.index_functions import incrVecIndex
from atropy_core.initial_condition import InitialCondition
from atropy_core.reaction import Reaction, ReactionSystem
from atropy_core.tree import Tree


def species(symbol_string):
    return sp.symbols(symbol_string)


class Model:
    def __init__(self, _species):
        self.reactions = []
        self.species = _species

    """
    Different function to add single or multiple reactions to our model
    """

    def add_reaction(self, reactants, products, propensities):
        num_symbols = len(self.species)
        eq_sp = products - reactants

        nu_vec = np.zeros(num_symbols)
        for i, sym in enumerate(self.species):
            nu_vec[i] = eq_sp.coeff(sym)

        prop_dict = {}
        # Test if we only have coefficient as variable,
        # if so, generate propensity in non factorised form
        if type(propensities) is int or type(propensities) is float:
            for sym in self.species:
                for i in range(reactants.coeff(sym)):
                    propensities *= sym - i
                propensities /= math.factorial(reactants.coeff(sym))

        # If propensites in non factorised form, factorise it and generate a dictionary
        if isinstance(propensities, sp.Expr):
            propensities = sp.simplify(propensities)

            n, d = sp.fraction(propensities)

            after_factor_n = sp.factor_list(n)
            after_factor_d = sp.factor_list(d)

            propensities = {}

            num_factors_n = len(after_factor_n[1])
            num_factors_d = len(after_factor_d[1])

            if num_factors_n != 0:
                coefficient_n = after_factor_n[0] ** (1.0 / num_factors_n)

                for i in range(num_factors_n):
                    factor = sp.Pow(after_factor_n[1][i][0], after_factor_n[1][i][1])
                    elements = list(factor.atoms(sp.Symbol))

                    if len(elements) != 1:
                        print("ERROR: Propensity non factorizable")
                        sys.exit()

                    if elements[0] in propensities:
                        propensities[elements[0]] *= factor * coefficient_n
                    else:
                        propensities[elements[0]] = factor * coefficient_n

            if num_factors_d != 0:
                coefficient_d = after_factor_d[0] ** (1.0 / num_factors_d)

                for i in range(num_factors_d):
                    factor = sp.Pow(after_factor_d[1][i][0], after_factor_d[1][i][1])
                    elements = list(factor.atoms(sp.Symbol))

                    if len(elements) != 1:
                        print("ERROR: Propensity non factorizable")
                        sys.exit()

                    if elements[0] in propensities:
                        propensities[elements[0]] *= 1 / (factor * coefficient_d)
                    else:
                        propensities[elements[0]] = 1 / (factor * coefficient_d)

        # Using the dictionary, generate the lambda functions to append the reactions
        for key, value in list(propensities.items()):
            for i, sym in enumerate(self.species):
                if key == sym:
                    prop_dict[i] = sp.lambdify(sym, value)

        self.reactions.append(Reaction(prop_dict, nu_vec))

    def add_reactions(self, reactants_list, products_list, propensities_list):
        for reactants, products, propensities in zip(
            reactants_list, products_list, propensities_list, strict=False
        ):
            self.add_reaction(reactants, products, propensities)

    def generate_reaction_system(self):
        species_names = [str(species_name) for species_name in self.species]
        self.reaction_system = ReactionSystem(self.reactions, species_names)


class Partitioning:
    def __init__(self, _partition, _r, _model):
        self.r = _r
        self.model = _model
        self.partition = _partition
        for i, sym in enumerate(self.model.species):
            self.partition = self.partition.replace(str(sym), str(i))

    def add_grid_params(self, n, binsize, liml):
        self.grid = GridParms(n, binsize, liml)

    def generate_tree(self):
        self.tree = Tree(self.partition, self.grid)
        self.tree.initialize(self.model.reaction_system, self.r)

    def generate_initial_condition(self, n_basisfunctions):
        self.initial_conditions = InitialCondition(self.tree, n_basisfunctions)

    def set_initial_condition(self, polynomials_dict):
        polynomials = []
        for sym in self.model.species:
            for key, value in list(polynomials_dict.items()):
                if key == sym:
                    polynomials.append(sp.lambdify(sym, value))

        for Q in self.initial_conditions.Q:
            Q[0, 0, 0] = 1.0

        species_idx = 0
        for node in range(self.tree.n_external_nodes):
            vec_index = np.zeros(self.initial_conditions.external_nodes[node].grid.d())
            for i in range(self.initial_conditions.external_nodes[node].grid.dx()):
                self.initial_conditions.X[node][i, :] = 1
                for j in range(self.initial_conditions.external_nodes[node].grid.d()):
                    self.initial_conditions.X[node][i, :] *= polynomials[
                        species_idx + j
                    ](vec_index[j])
                incrVecIndex(
                    vec_index,
                    self.initial_conditions.external_nodes[node].grid.n,
                    self.initial_conditions.external_nodes[node].grid.d(),
                )
            species_idx += len(vec_index)


def run(partitioning, output, tau, tfinal, snapshot=2, substeps=1, method="RK4"):
    with tempfile.NamedTemporaryFile(suffix=".nc", delete=True) as temp_file:
        file_name = temp_file.name
        partitioning.tree.write(fname=file_name)
        snap = int(np.floor((tfinal / tau) / snapshot))
        if method == "implicit_Euler":
            m = "i"
        elif method == "explicit_Euler":
            m = "e"
        elif method == "Crank_Nicolson":
            m = "c"
        elif method == "RK4":
            m = "r"
        else:
            print(
                "Possible inputs for method: "
                "implicit_Euler, explicit_Euler, Crank_Nicolson, RK4"
            )
        # site_packages_path = site.getsitepackages()[0]
        # cmd = (
        #     site_packages_path + "/atropy/core/build/atropy_core "
        #     f"""-i {file_name} -o {output} -s {snap} -t {tau} -f {tfinal}
        #      -n {substeps} -m {m}"""
        # )
        # os.system(cmd)
        atropy_core_pybind11.IntegrateTTN(file_name, output, snap, tau, tfinal, substeps, m)
