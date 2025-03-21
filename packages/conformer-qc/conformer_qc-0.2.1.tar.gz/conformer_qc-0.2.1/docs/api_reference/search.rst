===================
Substructure Search
===================

Often you may need to find a substructure within a larger system. The  :py:mod:`conformer.search` module allows you to search for structural motifs using `SMILES-style <https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_System>`_ strings. Think of this as regular expressions for molecules.

Searching is done through the :py:class:`~conformer.search.Seq` class which requires a SMILES-style query string as an argument. For a :py:class:`~conformer.systems.System`, you can query that sequence using the :py:meth:`~conformer.search.Seq.find` by providing the starting atom for you search. Alternatively you can use the :py:meth:`~conformer.search.Seq.find_all` to find all occurrences of that sequence in the system. Optionally, you may provide a connectivity graph for your system using the ``bongG`` keyword argument, but if you don't bonding is determined with the :py:func:`bonding_graph` function.

Both the :py:meth:`~conformer.search.Seq.find` and :py:meth:`~conformer.search.Seq.find_all` methods returns an uncannonized subsystem.

.. warning::
   This module is still under development. The API may change slightly as common usage patterns are established. This API has not been intensively performance tested and may struggle in scenarios involving thousands of queries/fragments. Please open an issue with suggestions or bugs as they arise.  

Query Strings
=============

Query strings are a sequence of elemental symbols matching the sequence of atoms you will be searching for. For example, to search for a peptide backbone you may use the sequence ``Seq("NCCO")`` to search for the nitrogen-carbon-carbon-oxygen motif.

Branches in :py:class:`~conformer.search.Seq` query strings are indicated using parenthesis. Using our amino acid example, alanine could be queried for using ``Seq("NC(C(H)(H)(H))CO")``. Note that cycles are not explicitly supported.

If more than on atom type is acceptable, you can include these groups in square brackets. For example ``Seq("[H,C]")`` will match a carbon OR a hydrogen. You can negate atom types with ``^``. For example ``Seq("[^C]")`` will match any atom which is NOT a carbon. If included and excluded atoms appear in the same bracket set, the included atoms take precedence and the excluded atoms are ignored. 

Selections
==========

A selection is simply a system with atoms ordered in the same sequence as they appear in the query string. This system is a subsystem of the argument of ``find`` and ``find_all``

The :py:mod:`conformer.search` module provides two functions, :py:func:`~conformer.search.select_adjacent` and :py:func:`~conformer.search.select_hydrogens` for expanding the current selection to include connected atoms. See the examples for how this is used.

Visualization
-------------

The :py:func:`conformer.export.visualize` function supports selections! Pass your selection along using the ``selection`` keyword argument to highlight those atoms in blue!

Examples
========

For these examples, let's consider benzene with the structure:

.. code-block:: text

   12
   Benzene
   C          0.00000        1.39904        0.00000
   C          1.21161        0.69952        0.00000
   C          1.21161       -0.69952        0.00000
   C         -0.00000       -1.39904        0.00000
   C         -1.21161       -0.69952        0.00000
   C         -1.21161        0.69952        0.00000
   H          2.14894        1.24069        0.00000
   H          2.14894       -1.24069        0.00000
   H         -2.14894        1.24069        0.00000
   H          0.00000        2.48138        0.00000
   H         -2.14894       -1.24069        0.00000
   H          0.00000       -2.48138        0.00000

Let's select two adjacent carbons and their protons. We'll use the :py:func:`conformer.export.visualize` method to see what's going on.

.. code-block:: python

   search = Seq("HCCH") # create sequence search
   C2H2.find(benzene[9]) # Select the hydrogen bound to the first carbon
   visualize(benzene, selection=C2H2[0]) # Look at the first match

.. figure:: benzene_HCCH.jpeg
   :scale: 50%

   The first "HCCH" selection starting from H9

Note that ``C2H2`` contains TWO selections. One going clockwise and the other counterclockwise.

.. code-block:: python

   visualize(benzene, selection=C2H2[1]) # Look at the second match

.. figure:: benzene_HCCH2.jpeg
   :scale: 50%

   The other "HCCH" selection starting from H9.

If you ran ``search.find_all(benzene)``, you would end up with TWELVE matches. Starting at each hydrogen you would go clockwise and then counterclockwise.

The search sequence ``Seq("CHCH")`` does not match any sequences in this molecule; no hydrogen is bound to two carbons. The sequence ``Seq("C(H)CH")`` is valid as it accounts for the branching.

Manipulating Selections
-----------------------

Let's start by selecting carbon 0.

.. code-block:: python

        search = Seq("C") # Look for carbon
        s = search.find(benzene[0])[0] # Start searching at carbon 0
        visualize(benzene, s)

.. figure:: benzene_C.jpeg
   :scale: 50%

   Initial C selection.

Atom selections are expanded with the :py:func:`conformer.search.select_adjacent` method using a connectivity graph optionally provided with the ``bondG`` keyword argument. In this case it uses the default bonding graph from ``System.supersystem``. The first argument indicates where you want to start selecting from. The indices are relative to the order the atoms appear in the selection, and not the order they appear in the system. You may provide an atom index, a list of atom indices, or no argument to select from all currently selected atoms.

You can specify how many bonds to expand by with the ``limit`` keyword argument.

.. code-block:: python

        # Expand our selection including all atoms one bond away 
        select_adjacent(s, limit=1)
        visualize(benzene, s)

.. figure:: benzene_CCCH.jpeg
   :scale: 50%

   Carbon 0 and all adjacent atoms

You can specify the ``kinds`` keyword argument to limit what types atoms are selected. Leaving this blank select any type of atoms. Query-string style NOT selection is not supported yet.

.. code-block:: python

        select_adjacent(s, kinds=["C"]) # Select only adjacent carbons
        visualize(benzene, s)

.. figure:: benzene_CHCCCCC.jpeg
   :scale: 50%

   Expanded selection to include all carbons.

Selected atoms will 'block' additional selections. Running

.. code-block:: python

        # Select any carbons attached through bonding to the second carbon 
        # in our selection (carbon 1)
        select_adjacent(s, 0)
        visualize(benzene, s)

will select all atoms connected to carbon 0; however, we have already selected carbons 1 and 5 and so no more atoms are added even though we have unselected hydrogens.

We can select from carbons 3 and 4, the last and second to last atoms added to our selection, to select their hydrogens.

.. code-block:: python

        # Select any carbons attached through bonding to the second carbon 
        # in our selection (carbon 1)
        select_adjacent(s, [5, 6])
        visualize(benzene, s)

.. figure:: benzene_CHCCCCCHH.jpeg
   :scale: 50%

   The protons for carbons 3 and 4 added to the selection.

If you would like to select just the protons attached to your current selection, you can run

.. code-block:: python
 
        select_hydrogens(s) # select adjacent protons
        # Shorthand for s.select_adjacent(kinds=["H"], limit=1)
        visualize(benzene, s)

which is shorthand for ``select_adjacent(kinds=["H"], limit=1)``

.. figure:: benzene_all.jpeg
   :scale: 50%

   Selected expanded to include all bonded protons.

API
===

.. automodule:: conformer.search
   :members: