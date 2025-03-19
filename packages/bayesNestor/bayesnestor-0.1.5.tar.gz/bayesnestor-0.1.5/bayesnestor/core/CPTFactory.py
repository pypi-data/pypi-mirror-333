from typing import Union

import numpy as np
import pyAgrum as gum
from pgmpy.factors.discrete import DiscreteFactor as pgmpyDiscreteFactor
from pgmpy.factors.discrete import TabularCPD as pgmpyCPT
from pyAgrum import LabelizedVariable

from bayesnestor.core.ConditionalProbabilityTable import CPT


class CPTFactory:
    """
    A factory class for converting between internal CPT representations and external pgmpy/pyAgrum CPTs.
    """

    @staticmethod
    def to_pgmpy_cpt(cpt: CPT) -> pgmpyCPT:
        """Convert an internal CPT to a pgmpy version of it.

        Args:
            cpt (CPT): Internal CPT to convert

        Raises:
            TypeError: Raised if the provied CPT is not an CPT-class object.

        Returns:
            pgmpyCPT: Converted CPT as a pgmpy-TabularCPD object.
        """

        if not isinstance(cpt, CPT):
            raise TypeError(
                f"Provided cpt needs to be a CPT-class object but an object with type {type(cpt)} was passed."
            )

        return pgmpyCPT(
            variable=cpt.name,
            variable_card=cpt.variable_card,
            values=cpt.values,
            evidence=cpt.evidence,
            evidence_card=cpt.evidence_card,
            state_names=cpt.state_names,
        )

    @staticmethod
    def from_pgmpy_cpt(pgmpy_cpt: pgmpyCPT) -> CPT:
        """Convert a pgmpy-TabularCPD to an internal CPT version of it.

        Args:
            pgmpy_cpt (pgmpy-TabularCPD): pgmpy-TabluarCPD object to convert.

        Raises:
            TypeError: Raised if provided CPT is not a pgmpy-TabularCPD.

        Returns:
            cpt (CPT): Internal CPT object.
        """

        if not isinstance(pgmpy_cpt, pgmpyCPT):
            raise TypeError(
                f"Provided cpt needs to be a pgmpy TabularCPD-class object but an object with type {type(pgmpy_cpt)} was passed."
            )

        return CPT(
            name=pgmpy_cpt.variables[0],
            variable_card=int(pgmpy_cpt.variable_card),
            values=pgmpy_cpt.get_values().tolist(),
            evidence=pgmpy_cpt.get_evidence()[::-1],
            evidence_card=pgmpy_cpt.cardinality[1:],
            state_names=pgmpy_cpt.state_names,
        )

    @staticmethod
    def from_pgmpy_factor(pgmpy_factor: pgmpyDiscreteFactor) -> CPT:
        """Convert a pgmpy-DiscreteFactor object to an internal CPT version of it.

        Args:
            pgmpy_factor (pyAgrum-pgmpy-DiscreteFactor): pgmpy-DiscreteFactor object to convert.

        Raises:
            TypeError: Raised if provided factor is not a pgmpy-DiscreteFactor object.

        Returns:
            cpt (CPT): Internal CPT object.
        """

        if not isinstance(pgmpy_factor, pgmpyDiscreteFactor):
            raise TypeError(
                f"Provided factor needs to be a pgmpy DiscreteFactor-class object but an object with type {type(pgmpy_factor)} was passed."
            )

        if len(pgmpy_factor.cardinality) != 1:
            raise ValueError(
                f"Provided factor has a cardinality of {pgmpy_factor.cardinality} instead of 1 and therefore cannot be converted to a valid CPT."
            )

        return CPT(
            name=pgmpy_factor.variables[0],
            variable_card=int(pgmpy_factor.cardinality),
            values=pgmpy_factor.values.reshape(
                np.prod(int(pgmpy_factor.cardinality)), 1
            ),
            evidence=None,
            evidence_card=None,
            state_names=pgmpy_factor.state_names,
        )

    @staticmethod
    def to_pyagrum_cpt(cpt: CPT) -> gum.Potential:
        """Convert an internal CPT to a pyAgrum version of it.

        Args:
            cpt (CPT): Internal CPT to convert.

        Raises:
            TypeError: Raised if provided cpt is not a CPT-class object.

        Returns:
            pyAgrum-Potential: Converted CPT as a pyAgrum-Potential object.
        """

        if not isinstance(cpt, CPT):
            raise TypeError(
                f"Provided cpt needs to be a CPT-class object but an object with type {type(cpt)} was passed."
            )

        pyagrum_pot = gum.Potential()

        if cpt.evidence_card is not None and len(cpt.evidence_card) >= 1:

            variables = [cpt.name] + cpt.evidence[::-1]
            cardinalitites = [cpt.variable_card] + cpt.evidence_card[::-1]
            cpt.state_names = cpt.state_names if cpt.state_names else {}

            for var, card in zip(variables, cardinalitites):
                lable_var = gum.LabelizedVariable(var, var, int(card))

                if var in cpt.state_names:
                    states = cpt.state_names[var]
                    for i, state_name in enumerate(states):
                        lable_var.changeLabel(i, state_name)
                else:
                    for i in range(card):
                        lable_var.changeLabel(i, f"s_{i}")

                pyagrum_pot.add(lable_var)

            pyagrum_pot[:] = (
                np.transpose(cpt.values)
                .ravel()
                .reshape(cpt.evidence_card + [cpt.variable_card])
            )

        else:
            lable_var = LabelizedVariable(cpt.name, cpt.name, int(cpt.variable_card))
            cpt.state_names = cpt.state_names if cpt.state_names else {}

            states = cpt.state_names.get(cpt.name, [])
            for i, state_name in enumerate(states):
                lable_var.changeLabel(i, state_name)

            pyagrum_pot.add(lable_var)
            pyagrum_pot.fillWith(np.ravel(cpt.values).tolist())

        return pyagrum_pot

    @staticmethod
    def from_pyagrum_potential(pyagrum_pot: gum.Potential) -> CPT:
        """Convert a pyAgrum-Potential to an internal CPT version of it.

        Args:
            pgmpy_factor (pyAgrum-Potential): pyAgrum-Potential object to convert.

        Raises:
            TypeError: Raised if provided CPT is not a pyAgrum-Potential.

        Returns:
            cpt (CPT): Internal CPT object.
        """
        if not isinstance(pyagrum_pot, gum.Potential):
            raise TypeError(
                f"Provided cpt needs to be a pyAgrum Potential-class object but an object with type {type(pyagrum_pot)} was passed."
            )

        name = pyagrum_pot.names[0]
        variable_card = None
        evidence = [] if len(pyagrum_pot.variablesSequence()) > 1 else None
        evidence_card = (
            [] if len(pyagrum_pot.variablesSequence()) > 1 else []
        )  # default value to support marginal cpts
        state_names = dict()

        for var in pyagrum_pot.variablesSequence():
            if var.name() != name:
                evidence.append(var.name())
                evidence_card.append(var.domainSize())

            else:
                variable_card = var.domainSize()

            if len(var.labels()) > 0:
                state_names[var.name()] = list(var.labels())

        first_pot_shape = (
            (np.prod(evidence_card), -1) if len(evidence_card) > 0 else (1, -1)
        )
        reordered_values = np.ravel(
            pyagrum_pot.toarray().reshape(first_pot_shape), "F"
        ).reshape(variable_card, -1)

        return CPT(
            name=name,
            variable_card=variable_card,
            values=reordered_values,
            evidence=evidence,
            evidence_card=evidence_card,
            state_names=state_names,
        )

    @staticmethod
    def convert_pgmpy_to_pyagrum(pgmpy_cpt: pgmpyCPT) -> gum.Potential:
        """Convenience function to convert a pgmpy-TabularCPD to a pyAgrum-Potential.

        Args:
            pgmpy_cpt (pgmpy-TabularCPD): pgmpy-TabularCPD object to convert.

        Raises:
            TypeError: Raised if provided CPT is not a pgmpy-TabularCPD

        Returns:
            pyAgrum-Potential: Converted pyAgrum-Potential object.
        """

        if not isinstance(pgmpy_cpt, pgmpyCPT):
            raise TypeError(
                f"Provided cpt needs to be a pgmpy TabularCPD-class object but an object with type {type(pgmpy_cpt)} was passed."
            )

        intermediate_cpt = CPTFactory.from_pgmpy_cpt(pgmpy_cpt)
        pyagrum_pot = CPTFactory.to_pyagrum_cpt(intermediate_cpt)
        return pyagrum_pot

    @staticmethod
    def convert_pyagrum_to_pgmpy(pyagrum_pot: gum.Potential) -> pgmpyCPT:
        """Convenience function to convert a pyAgrum-Potential to a pgmpy-TabularCPD.

        Args:
            pyagrum_pot (pyAgrum-Potential): pyAgrum-Potential object to convert.

        Raises:
            TypeError: Raised if provided cpt is not a pyAgrum-Potential.

        Returns:
            pgmpy-TabularCPD: Converted pgmpy-TabularCPD object.
        """
        if not isinstance(pyagrum_pot, gum.Potential):
            raise TypeError(
                f"Provided cpt needs to be a pyAgrum Potential-class object but an object with type {type(pyagrum_pot)} was passed."
            )
        intermediate_cpt = CPTFactory.from_pyagrum_potential(pyagrum_pot)
        pgmpy_cpt = CPTFactory.to_pgmpy_cpt(intermediate_cpt)
        return pgmpy_cpt

    @staticmethod
    def are_equal(
        reference: Union[CPT, pgmpyCPT, gum.Potential],
        other: Union[CPT, pgmpyCPT, gum.Potential],
    ) -> bool:
        """Static method to check if two CPT instances contain equal information.

        Args:
            reference (Union[CPT, pgmpyCPT, gum.Potential]): Reference instance of a CPT.
            other (Union[CPT, pgmpyCPT, gum.Potential]): Another instance of a CPT.

        Returns:
            bool: True if the instances contain equal information, False otherwise.
        """
        try:
            match reference:
                case CPT():
                    pass
                case pgmpyCPT():
                    reference = CPTFactory.from_pgmpy_cpt(reference)
                case gum.Potential():
                    reference = CPTFactory.from_pyagrum_potential(reference)

            match other:
                case CPT():
                    pass
                case pgmpyCPT():
                    other = CPTFactory.from_pgmpy_cpt(other)
                case gum.Potential():
                    other = CPTFactory.from_pyagrum_potential(other)

            return reference == other
        except ValueError as e:
            print(e)
            return False
