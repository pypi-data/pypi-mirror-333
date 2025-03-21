#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#


import numpy as np

from conformer.common import CAPPING_ATOM
from conformer.elements import get_covalent_radius
from conformer.spatial import bonding_graph, distance
from conformer.systems import AbstractAtom, Atom, BoundAtom, System, SystemKey
from conformer_core.stages import Stage, StageOptions

# TODO: What we really need is a method that gives atoms within r of a given
#       subsystem


class HCapsMod(Stage):
    """R Capper

    TODO: Add math for capping

    Attributes:
        name (str): name of the mod
        note (str): human-readable note on this mod
        tolerance (float): fudge factor used when determining if a bond exists
        cutoff (float): maximum distance to search for capping atoms
        k (int): Number of nearest neighbor atoms to consider
        ignore_charged (bool): prevents capping of atoms that are charged (i.g. metal centers)
    """

    H_radius = get_covalent_radius("H")

    class Options(StageOptions):
        k: int = 8
        tolerance: float | None = None
        cutoff: float | None = None
        ignore_charged: float = False

    opts: Options


    @staticmethod
    def keep_atom(atom: AbstractAtom):
        """Check it atom meets capping criteria"""
        if not atom.is_physical:
            return False
        if atom.charge != 0:
            return False
        return True


    def __init_stage__(self) -> None:
        super().__init_stage__()

        # Swap out capping criteria
        if not self.opts.ignore_charged:
            def keep_atom(atom: AbstractAtom) -> bool:
                return atom.is_physical
            self.keep_atom = keep_atom

    def cap_position(
        self,
        inner_atom: BoundAtom,
        outer_atom: BoundAtom,
    ) -> np.array:
        """
        Calculates cap hydrogen position. See Equation ? in DOI:
        """
        # Calculate contraction relative to covalent radius
        shortening = (outer_atom.covalent_radius + self.H_radius) / (
            distance(inner_atom, outer_atom)
        )

        # Calculate position
        return inner_atom.r + shortening * (outer_atom.r - inner_atom.r)

    def __call__(self, supersystem: System, key: SystemKey, system: System) -> System:
        if supersystem.unit_cell is not None:
            raise ValueError("Capping protocol is untested for periodic systems")
        # Supersystem graph is cached 
        G = bonding_graph(supersystem)

        caps: list[Atom] = []
        internal_atoms = set(system)
        for inner_a in system:

            if not self.keep_atom(inner_a):
                continue

            # All atoms which are bonded to an atom in internal_a
            # NOTE: Not suitable for periodic systems
            external_atoms = set(G.neighbors(inner_a))
            external_atoms.difference_update(internal_atoms)

            # NOTE: Older method used `atom in systerm` but this took way too
            # much time. Also not garunteed to work in periodic system

            # TODO: Validate with semi-periodic systems
            caps.extend((
                Atom(t="H", r=self.cap_position(inner_a, outer_a), charge=0)
                for outer_a in external_atoms if self.keep_atom(outer_a)
            ))
        system.add_atoms(*caps, role=CAPPING_ATOM)
        return system
    
