#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#

from conformer.common import GHOST_ATOM
from conformer.spatial import primitive_neighbor_graph
from conformer.systems import System, SystemKey
from conformer_core.stages import Stage, StageOptions


class CounterpoiseSubsystemMod(Stage):
    """
    Creates counterpoise-corrected subsystem

    If the `r` option is < 0 Å all atoms in `supersystem` are included.
    
    If the `r` option is > 0 Å only atoms within `r` of the selected atoms are included
    """

    class Options(StageOptions):
        r: float = -1.0 
        
    opts: Options
    
    def __call__(self, supersystem: System, key: SystemKey, system: System) -> System:
        # TODO: Periodic (MIC atoms? How do we displace them?)
        # TODO: Handle proxys

        if self.opts.r < 0:
            ghost_idxs = set(range(len(supersystem))).difference(key)
            system.add_atoms(*supersystem[ghost_idxs], role=GHOST_ATOM)
            return system
        else:
            G = primitive_neighbor_graph(supersystem, r = self.opts.r) 
            
            for i in key:
                for neighbor in G.neighbors(supersystem[i]):
                    if neighbor not in supersystem[key]:
                        system.add_atoms(neighbor, role = GHOST_ATOM)

            return system