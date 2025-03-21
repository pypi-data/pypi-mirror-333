#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
"""The search module allows selecting and searching for atomic motifs in existing systems"""

from io import StringIO

import networkx as nx

from conformer.spatial import bonding_graph
from conformer.systems import BoundAtom, System


def select_adjacent(
    system: System,
    _selector: int | list[int] | None=None,
    bondG: nx.Graph | None=None,
    limit: int=0,
    kinds: list[str] | None = None
) -> list[BoundAtom]:
    """Selects atoms adjacent to the current selection"""

    if bondG is None and system.supersystem is not None:
        bondG = bonding_graph(system.supersystem)
    else:
        raise ValueError("System section must have supersystem data")

    # selector is always and iterator of ints
    if _selector is None:
        selector = range(len(system))
    elif isinstance(_selector, int):
        selector = [_selector]
    else:
        selector = _selector

    # Add the current selection
    existing_atoms = set(system)
    new_atoms = set(system)
    for a in (system[i] for i in selector):
        for n in nx.neighbors(bondG, a):
            _crawl(bondG, n, 1, new_atoms, limit, kinds)

    # Expand the list
    to_add = list(new_atoms.difference(existing_atoms))
    system.add_atoms(*to_add)
    return to_add


def select_hydrogens(
        system: System,
        _selector: int | list[int] | None=None,
        bondG: nx.Graph | None=None) -> list[BoundAtom]:
    """Selects hydrogens adjacent to the current selection"""
    return select_adjacent(
        system,
        _selector=_selector,
        bondG=bondG,
        limit=1,
        kinds=["H"]
    )
                

def _crawl(
    G: nx.Graph,
    a: BoundAtom,
    level,
    new_atoms,
    limit: int,
    kinds: list[str] | None
):
    """Helper method for recursivly selecting atoms"""
    # Check that we haven't seen it before
    if a in new_atoms:
        return # STOP!

    # Check that it's the right type
    if kinds and a.t not in kinds:
        return

    # Expand our selection
    new_atoms.add(a)

    # Check our limit. Don't go too far!
    if limit > 0 and level == limit:
        return

    # Find other connected atoms
    for n in nx.neighbors(G, a):
        _crawl(G, n, level + 1, new_atoms, limit, kinds)


class Seq:        
    """Sequence to search for atoms loosly based SMILES strings
    """

    def __init__(self, seq: str):
        self.G = nx.DiGraph()
        self.num_nodes = 0

        self._parse_branch(StringIO(seq))

        # Get traversal order from nodes
        self.order = list(nx.dfs_preorder_nodes(self.G, 0))
    
    def find(self, start: BoundAtom, bondG: nx.Graph | None = None) -> list[System]:
        """Find sequence starting at atom `start` in `start.supersystem`
        
        Args:
            start (BoundAtom): The start location for searching for the sequence
            bondG (nx.Graph | None): Bonding graph used to determine connectivity.
                                     The default bonding graph will be used if not
                                     provided. 
        
        Returns:
            list[Selection]: Returns a list of all Selections starting at `start` which match.
        """
        # Automatically select the graph
        if bondG is None:
            bondG = bonding_graph(start.system)

        selections = []

        # Interrogate first atom
        loc = 0
        node = self.order[0]
        if not self.acceptable(node, start):    
            return selections # Return all misses
        
        # Parse by neighbors
        self._search_neighbors(bondG, start, loc, [start], selections)

        # Return non-canonized systems to preserve ordering
        return [
            System(
                atoms=a,
                supersystem=start.system,
                unit_cell=start.system.unit_cell
            )
            for a in selections
        ]
    
    def find_all(self, sys: System, bondG: nx.Graph | None = None) -> list[System]:
        """Find all instances of the sequence in selection
        
        Args:
            sys (System): Structure to search for the sequence
        """
        if bondG is None:
            bondG = bonding_graph(sys)
        else:
            bondG = bondG
        selections = []
        for a in sys:
            selections.extend(self.find(a, bondG))
        return selections
    
    def _search_neighbors(self, G: nx.Graph, atom: BoundAtom, loc: int, sequence: list[BoundAtom], selections: list[list[BoundAtom]]):
        """Helper function for finding the next step in the sequence"""
        # Recursively traverse the bonding graph searching for matching sequences
        if loc >= len(self.order) - 1:
            # We've reached the end
            selections.append(sequence)
            return
        for n in nx.neighbors(G, atom):
            if n in sequence:
                continue
            if self.acceptable(self.order[loc + 1], n): # Move onto the next phase!
                self._search_neighbors(G, n, loc + 1, sequence + [n], selections)


    def acceptable(self, node: int, atom: BoundAtom) -> bool:
        """Returns True if this atom is acceptable for the sequence

        Args:
            node (int): The node index to compair against
            atom (BoundAtom): Prospective atom
        
        Returns:
            bool: Returns ``True`` if ``atom`` meets the criteria of ``node``
        """
        # Check for allowed 
        t = self.G.nodes[node]["t"]
        if t:
            return atom.t in t

        # Check for exclusions
        exclude = self.G.nodes[node]["exclude"]
        if exclude:
            return atom.t not in exclude 

        return True # No constraints were placed on this atom
        
    
    ########################
    # STRING PARSING METHODS
    ########################
    def _parse_branch(self, seq: StringIO) -> int:
        """Manages the parsing process"""
        nid = -1 # The start of this branch
        edge = -1
        move_edge = False
        while True:
            c = seq.read(1)
            if not c:
                break
            elif c.isupper():
                node_i = self._parse_single(c, seq)
                move_edge = True 
            elif c == "[":
                node_i = self._parse_group(seq)
                move_edge = True
            elif c == "(":
                node_i = self._parse_branch(seq)
                move_edge = False
            elif c == ")":
                break # Branch termination
            else:
                raise ValueError(f"Cannot parse '{c}'")
        
            # Handle linking new the new node
            if edge < 0:
                edge = node_i
                nid = node_i # The start of this branch and will be returned
            else:
                self.G.add_edge(edge, node_i)
                if move_edge:
                    edge = node_i
        
        # Error if we don't have an active edge
        if nid < 0:
            raise ValueError("Could not parse branch")
        return nid
            
    def _add_node(self, t: list[str], exclude: list[str] | None = None) -> int:
        """Adds a node to the sequnce graph and increments num_nodes"""
        # Always keep the exclude
        if exclude is None:
            exclude = []

        # Create a new node on the graph
        self.G.add_node(
            self.num_nodes,
            t=t,
            exclude=exclude
        )
        self.num_nodes += 1 # Increment the node count
        return self.num_nodes - 1

    def _parse_single(self, c0: str, seq: StringIO) -> int:
        """Parse a single element and count it as a node"""
        return self._add_node([self._parse_element(c0, seq)])
        
    def _parse_element(self, c0, seq: StringIO) -> str:
        """An element symbol as Ul"""
        while True:
            c = seq.read(1)
            if not c: 
                break
            elif c.islower():
                c0 += c
            elif c == " ":
                continue # No-op
            else:
                seq.seek(seq.tell() - 1)
                break
        return c0
 
    def _parse_group(self, seq: StringIO) -> int:
        """A group is denoted by [El,At]"""
        t = []
        exclude = []
        while True:
            c = seq.read(1)
            if not c: 
                break
            elif c.isupper():
                t.append(self._parse_element(c, seq))
            elif c == "^":
                # Advance by one
                exclude.append(self._parse_element(seq.read(1), seq))
            elif c == "]":
                break
            elif c in [" ", ","]:
                continue # No-Op
        return self._add_node(t, exclude)