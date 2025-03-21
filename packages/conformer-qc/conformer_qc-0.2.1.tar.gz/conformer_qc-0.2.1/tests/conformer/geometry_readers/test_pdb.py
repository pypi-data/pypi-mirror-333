#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from conformer.example_systems import open_example, read_example
from conformer.geometry_readers.pdb import PDBRead


class PDBReadTestCases(TestCase):
    def test_pdb(self):
        with open_example("small_protien.pdb").open("r") as f:
            sys = PDBRead(f)

        self.assertEqual(len(sys), 51)
        self.assertEqual(sys.chemical_formula(), "C26N9O16")
        self.assertEqual(len({a.meta['frag_group'] for a in sys}), 7)

        # Check the first atom
        self.assertEqual(sys[0].t, "N")
        self.assertEqual(sys[0].charge, 1)
        self.assertEqual(sys[0].meta['pdb_entry_type'], "ATOM")
        self.assertEqual(sys[0].meta['pdb_residue_name'], "SER")
        self.assertEqual(sys[0].meta['pdb_atom_no'], 1)
        self.assertEqual(sys[0].meta['pdb_residue_no'], 1)
        self.assertEqual(sys[0].meta['pdb_chain'], "A")

    def test_charge(self):
        """Verify that charges and charge overrides are assigned correctly.
        Unlike xyz files where charges are assigned by location, PDB files
        use the atom number 
        """
        sys = read_example("charged_protein.pdb", "CP", charges={1: 0, 154: -1})
        self.assertEqual(sys[0].charge, 0) # Charge overridden
        self.assertEqual(sys[153].charge, -1) # Charge specified
        self.assertEqual(sys[1].charge, 2) # Charge parsed

    def test_frag_groups(self):
        """Verify that frag groups are assigned correctly."""

        sys = read_example("charged_protein.pdb", "CP")
        groups = {a.meta['frag_group'] for a in sys}
        self.assertEqual(len(groups), 20)

        # Check first residue
        a = sys[79]
        self.assertEqual(a.meta['pdb_atom_no'], 80)
        self.assertEqual(a.meta['frag_group'], 8)

        a = sys[80]
        self.assertEqual(a.meta['pdb_atom_no'], 81)
        self.assertEqual(a.meta['frag_group'], 8)

        # Check C and O from first residue. Make sure they are included in the next
        a = sys[81]
        self.assertEqual(a.meta['pdb_atom_no'], 82)
        self.assertEqual(a.meta['frag_group'], 9)

        a = sys[82]
        self.assertEqual(a.meta['pdb_atom_no'], 83)
        self.assertEqual(a.meta['frag_group'], 9)

        #C-terminus C & O residue no. should NOT be changed
        a = sys[276]
        self.assertEqual(a.meta['pdb_atom_no'], 277)
        self.assertEqual(a.meta['frag_group'], 20)
        a = sys[277]
        self.assertEqual(a.meta['pdb_atom_no'], 278)
        self.assertEqual(a.meta['frag_group'], 20)
        a = sys[278]
        self.assertEqual(a.meta['pdb_atom_no'], 279)
        self.assertEqual(a.meta['frag_group'], 20)
        a = sys[279]
        self.assertEqual(a.meta['pdb_atom_no'], 280)
        self.assertEqual(a.meta['frag_group'], 20)

    
    def test_1mmq(self):
        """Test reading a large, and complete, protein structure"""
        sys = read_example("1mmq.pdb", "CP")
        self.assertEqual(len(sys), 2613)

    def test_181l(self):
        """
        Test reading a large, and complete, protein structure

        This file does not have a chain ID which confuses the whitespace-base parser
        """
        sys = read_example("181l.pdb", "CP")
        self.assertEqual(len(sys), 2636)