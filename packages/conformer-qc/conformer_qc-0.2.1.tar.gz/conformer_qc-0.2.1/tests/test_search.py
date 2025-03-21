#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest

from conformer.example_systems import read_example
from conformer.search import Seq, select_adjacent, select_hydrogens
from conformer.systems import System, chemical_formula


class SelectTests(unittest.TestCase):

    def test_select(self):
        """Test basic selections with benzene"""
        benzene = read_example("benzene.xyz", "benzene")

        # Create initial selection
        sel = System([benzene[0]], supersystem=benzene)

        # Expand selection
        select_hydrogens(sel)
        self.assertEqual(2, len(sel))
        self.assertEqual(sel[0].t, "C")
        self.assertEqual(sel[1].t, "H")

        # Select neighboring carbons
        select_adjacent(sel, 0, limit=1)
        self.assertEqual(4, len(sel))

        # Select remaining carbons
        select_adjacent(sel, [2, 3], kinds=["C"])
        self.assertEqual(7, len(sel))

        # Select everything
        select_adjacent(sel)
        self.assertEqual(12, len(sel))
    

class SequenceTestCases(unittest.TestCase):

    def test_Seq(self):
        """Constructor test of the sequence object"""
        # Test atom parsing
        s = Seq("He")
        self.assertListEqual(s.G.nodes[0]["t"], ["He"])
        self.assertListEqual(s.G.nodes[0]["exclude"], [])

        # Test group parsing
        s = Seq("[A, Bee, ^C]")
        self.assertListEqual(s.G.nodes[0]["t"], ["A", "Bee"])
        self.assertListEqual(s.G.nodes[0]["exclude"], ["C"])

        # Test connectivity
        s = Seq("AB(C)(DE(F)G)H")

        # Check we have correct number of nodes
        # 1 -> B
        self.assertEqual(s.G.out_degree(1), 3) # Connected to C, D, and H
        # 4 -> E
        self.assertEqual(s.G.out_degree(4), 2) # Connected to F, G

    def test_selection(self):
        """Applied tests of the Seq object"""
        # Again testing with benzene
        benzene = read_example("benzene.xyz", "benzene")

        # Select HCCH
        # Each C can go either left or right
        s = Seq("HCCH")
        HCCHs = s.find_all(benzene)
        self.assertEqual(12, len(HCCHs))
        for sel in HCCHs:
            self.assertEqual("H2C2", chemical_formula(sel))

        # Select the ring. Can go either way!
        s = Seq("CCCCCC")
        C6s = s.find(benzene[0])
        self.assertEqual(2, len(C6s))
        self.assertEqual("C6", chemical_formula(C6s[0]))

        s = Seq("CCCCCCC")
        C7s = s.find(benzene[0])
        # Again, could go either way
        self.assertEqual(0, len(C7s))

 
    def test_small_protein(self):
        """Example protein test"""
        protein = read_example("small_protien.pdb", "pro")

        # Backbone sequence
        s = Seq("NCCO")
        backbone = s.find_all(protein)

        # Include the R group in the selection 
        for b in backbone:
            # Alpha carbon
            select_adjacent(b, 1)
            select_hydrogens(b)

        self.assertEqual(7, len(backbone))
