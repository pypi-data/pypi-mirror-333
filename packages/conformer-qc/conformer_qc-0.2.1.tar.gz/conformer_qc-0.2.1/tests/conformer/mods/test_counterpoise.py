#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from conformer.mods.counterpoise import CounterpoiseSubsystemMod
from conformer.systems import GHOST_ATOM, PHYSICAL_ATOM, System


class CounterpoiseTestCases(TestCase):
   
    def setUp(self):
        self.supersystem = System.from_tuples(
            [
                ("H", 0, 0, 0),
                ("H", 0, 0, 1),
                ("H", 0, 0, 2),
                ("H", 1, 1, 4),
            ]
        )


    def test_mod(self):
        # TEST DEFAULT (no cuttoff)
        cpm = CounterpoiseSubsystemMod()
        s = self.supersystem.subsystem([0], mods=[cpm])
        s_ref = System([])
        s_ref.add_atoms(self.supersystem[0], role=PHYSICAL_ATOM)
        s_ref.add_atoms(*self.supersystem[1, 2, 3], role=GHOST_ATOM)

        self.assertEqual(s, s_ref)

        # TEST FOR r = 2 A
        cpm = CounterpoiseSubsystemMod.from_options(r=1.0)
        s = self.supersystem.subsystem([0], mods=[cpm])

        s_ref = System([])
        s_ref.add_atoms(self.supersystem[0], role=PHYSICAL_ATOM)
        s_ref.add_atoms(self.supersystem[1], role=GHOST_ATOM)
        self.assertEqual(s, s_ref)

        # TEST FOR r = 10 A
        cpm= CounterpoiseSubsystemMod.from_options(r=3)
        s = self.supersystem.subsystem([0], mods=[cpm])

        s_ref = System([])
        s_ref.add_atoms(self.supersystem[0], role=PHYSICAL_ATOM)
        s_ref.add_atoms(*self.supersystem[1,2], role=GHOST_ATOM)

        self.assertEqual(s, s_ref)
