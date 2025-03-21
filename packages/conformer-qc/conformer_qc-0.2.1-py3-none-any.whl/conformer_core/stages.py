#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#

# Add the constraint that these blocks are stateless. They cannot be combined
# with systems or view or whatnot
# Descriptor for a deferred pipeline attribute
from datetime import datetime
from inspect import getmembers
from typing import (
    Any,
    ClassVar,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)
from uuid import UUID, uuid4

import networkx as nx
import pydantic
from pydantic import BaseModel

from conformer_core.accessors import FilterCompositeAccessor, ModCompositeAccessor
from conformer_core.util import ind, summarize

# from conformer_core.accessors import Accessor

World = Dict["str", "Stage"]
DEFAULT_WORLD: World = {}


class StageException(Exception): ...


class StageInWorldException(StageException): ...


class StageOptions(BaseModel): ...


class Stage:
    # Class Variables
    Options: Type[StageOptions] = StageOptions

    # Instance variables
    id: UUID
    name: str
    created: datetime
    meta: Dict[str, Any]
    opts: StageOptions  # Instance of options
    _world: World = DEFAULT_WORLD  # Object is share among all blocks by default
    _link_atrs: ClassVar[Tuple[str, ...]] = tuple()
    _use_db: bool
    _saved: int

    def __init_subclass__(cls) -> None:
        cls._link_atrs = tuple(
            (name for name, _ in getmembers(cls, lambda x: isinstance(x, Link)))
        )
        return super().__init_subclass__()

    def __init__(
        self,
        options: Optional[StageOptions] = None,
        name: str = None,
        id: Optional[UUID] = None,
        meta: Dict[str, Any] = None,
        created: Optional[datetime] = None,
        links: Optional[Dict[str, str]] = None,
        _saved: Optional[int] = 0,
        _use_db: Optional[bool] = False,
        _world: Optional[World] = DEFAULT_WORLD,
        _delay_init=False,
    ) -> None:
        super().__init__()  # Fixes issue with multiple inheretance/PropertyExtractorMixin
        self.opts = options if options else self.Options()
        self._world = _world
        self._saved = _saved

        # Initialize the defaults
        self.id = uuid4() if id is None else id
        self.name = str(self.id) if name is None else name
        self.meta = {} if meta is None else meta
        self.created = datetime.now() if created is None else created
        self._use_db = _use_db

        # Add add this stage to the world
        if self.name in self._world:
            raise StageInWorldException(
                f"A stage named '{self.name}' already exists."
            )
        else:
            # On some level this seems like a recipe for memory leaks
            self._world[self.name] = self

        # Mark as anonymous if it wasn't given a formal name
        if name is None:
            self.meta["anonymous"] = True

        # Make soft links for all items in the world
        if links:
            for l, v in links.items():
                setattr(self, l, v)

        if not _delay_init:
            self.__init_stage__()

    def __init_stage__(self):
        pass

    def __del__(self):
        """Remove itself from the world"""
        try:
            del self._world[self.name]
        except (KeyError, AttributeError):
            pass

    @classmethod
    def from_options(
        cls,
        name: str = None,
        id: Optional[UUID] = None,
        meta: Optional[Dict[str, Any]] = None,
        links: Optional[Dict[str, str]] = None,
        _world: Optional[World] = DEFAULT_WORLD,
        **kwargs,
    ):
        """Builds a config from keyword arguments instead of an explicit config"""
        return cls(
            cls.Options(**kwargs),
            name=name,
            id=id,
            meta=meta,
            links=links,
            _world=_world,
        )

    def get_links(self):
        for name in self._link_atrs:
            yield (name, getattr(self, name))

    # Customize pickle behaviour
    def acturalize_links(self):
        """Iterates through all link fields and actualizes the fields"""
        for l in self._link_atrs:
            s = getattr(self, l)
            if isinstance(s, Stage):
                s.acturalize_links

    def __getstate__(self) -> Any:
        self.acturalize_links()  # Access all linked stages
        state = self.__dict__.copy()
        if "_world" in state:
            del state["_world"]
        return state

    def __setstate__(self, state: Dict) -> None:
        # These don't have a world
        self.__dict__.update(state)
        if not hasattr(self, "_world"):
            self._world = {}

    # Hashing
    def __hash__(self) -> int:
        return self.name.__hash__()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return False
        return __value.name == self.name and __value.id == self.id

    def summarize(self, padding=2, level=0) -> str:
        rec_str = ind(padding, level, f"Stage {self.name}: \n")

        level += 1
        rec_str += ind(padding, level, f"Type: {self.__class__.__name__}\n")
        rec_str += ind(padding, level, f"ID: {self.id}\n")
        rec_str += ind(
            padding, level, f"Created: {self.created.isoformat(timespec='minutes')}\n"
        )

        links = list(self.get_links())
        if links:
            rec_str += ind(padding, level, "Links:\n")
            for k, v in links:
                if v is None:
                    _v = "<None>"
                elif isinstance(v, Iterable):
                    _v = [i.name for i in v]
                    if not _v:
                        _v = "<empty>"
                else:
                    _v = v.name
                rec_str += summarize(k, _v, padding=padding, level=level + 1)

        options = self.opts.model_dump(mode="json")
        if options:
            rec_str += summarize("Options", options, padding=padding, level=level)

        if self.meta:
            rec_str += summarize("Meta", self.meta, padding=padding, level=level)

        return rec_str


LinkType = Optional[Union[str, Stage]]


class Link:
    def set(self, obj, value, isdirty=True):
        setattr(obj, self.private_name, (value, isdirty))

    def clean(self, obj, value):
        if isinstance(value, str):
            value = obj._world[value]
        elif isinstance(value, Stage):
            pass  # This is ok
        elif value is None:
            pass  # This is also ok
        else:
            raise ValueError(f"Links cannot be of type {type(value)}")
        return value

    """Reference to another stage"""

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj: Stage, objtype=None) -> List["Stage"]:
        try:
            val, isdirty = getattr(obj, self.private_name)
        except AttributeError:  # We want links to be optional
            val = None
            isdirty = True

        if isdirty:
            val = self.clean(obj, val)
            self.set(obj, val, isdirty=False)
        return val

    def __set__(self, obj, value):
        self.set(obj, value, isdirty=True)


StackType = Optional[List[Union[str, Stage]]]


class Stack(Link):
    """An 'array' of stages"""

    def clean(self, obj, stack):
        if stack is None:
            return []
        _stack = []
        for val in stack:
            val = super().clean(obj, val)
            if val is None:
                continue
            _stack.append(val)
        return _stack


class ModStack(Stack):
    def clean(self, obj, stack):
        val = super().clean(obj, stack)
        return ModCompositeAccessor(val)


class FilterStack(Stack):
    def clean(self, obj, stack):
        val = super().clean(obj, stack)
        return FilterCompositeAccessor(val)


####   YAML-BASED STORAGE   ####
class StoredStage(BaseModel):
    """
    Pydantic model for parsing/storing Stage data
    """

    type: str  # Which class to use to reconstitute this model
    id: Optional[UUID] = None
    name: Optional[str] = None
    note: Optional[str] = None  # stored in Stage.meta
    options: Optional[Dict[str, Any]] = pydantic.Field(
        default_factory=dict
    )  # Will be passed to Stage.Options
    links: Optional[
        Dict[str, Union[Union[str, "StoredStage"], List[Union[str, "StoredStage"]]]]
    ] = pydantic.Field(default_factory=dict)
    created: Optional[datetime] = pydantic.Field(default_factory=dict)
    meta: Dict[str, Any] = pydantic.Field(default_factory=dict)
    db_id: int = 0


def get_stage_names(stage: StoredStage | str, names: Set[str] | None) -> Set[str]:
    """Retrieves all stage names from a StoredStage"""
    if names is None:
        names = set()

    # Handle case where stage is str
    if isinstance(stage, str):
        names.add(stage)
        return  # Stop!

    if stage.name:
        names.add(stage.name)

    for link in stage.links.values():
        if isinstance(link, List):
            get_stage_names_from_list(link, names)
        else:
            get_stage_names(link, names)

    return names


def get_stage_names_from_list(
    stages: List[StoredStage | str], names: Set[str] | None = None
) -> Set[str]:
    """Retrieves all stage names from a list of StoredStage information"""
    if names is None:
        names = set()

    for stage in stages:
        get_stage_names(stage, names)
    return names


class ReconstitutionException(Exception): ...


def reconstitute(
    *stored_data: StoredStage,
    registry: Dict[str, Type[Stage]],
    world: Dict[str, Stage],
) -> Stage:
    G = stage_graph(*stored_data)  # Get dependancy info

    # Prune existing nodes from the graph
    remove_existing = []
    for n, d in G.nodes(data=True):
        # Keep if it's a stage we haven't seen befor
        if n not in world:
            continue

        remove_existing.append(n)
        remove_existing.extend(nx.descendants(G, n))

        data = d['data']
        if data is None:
            continue
        # Validate that we are getting what we expect
        stage = world[n]
        if data.type != stage.__class__.__name__:
            raise Exception(
                f"Stored data is requesting a Stage of type {data.type} but the Stage in the registry is of type {stage.__class__.__name__}"
            )
    G.remove_nodes_from(remove_existing)

    # Do a depth-first iteration a reconstitute nodes not in our world
    for n in nx.dfs_postorder_nodes(G):
        data = G.nodes[n]["data"]

        # Check if name-only references exist in our world
        if data is None:
            if n not in world:
                raise ReconstitutionException(f"Request stage `{n}` has no data")
            continue

        # Immediatly create the stage. Links will have been re-constituted by this point
        StageClass = registry[data.type]

        # Backwards compatibilty with older fragment styls
        if data.note and "note" not in data.meta:
            data.meta["note"] = data.note

        # Create normalized list of links
        links = {}
        for l_name, l in data.links.items():
            if isinstance(l, List):
                links[l_name] = [stage_name(i) for i in l]
            else:
                links[l_name] = stage_name(l)

        # Create the stage!
        # This will also add it to our world
        stage = StageClass(
            name=data.name,
            id=data.id,
            meta=data.meta,
            created=data.created,
            options=StageClass.Options(**data.options),
            links=links,
            _world=world,
            _use_db=data.db_id > 0,
            _saved=data.db_id,
        )

    # I don't like this return signature but we will keep it for backward compat.
    if len(stored_data) == 1:
        return world[stage_name(stored_data[0])]
    else:
        return (world[stage_name(s)] for s in stored_data)


def stage_name(d: StoredStage | str) -> str:
    """
    Normalized StoredStage data into a name
    """
    if isinstance(d, str):
        return d
    elif d.name:
        name = d.name
    elif d.id:
        name = str(d.id)
    else:
        # Generate this here. We need an ID
        d.id = uuid4()
        name = str(d.id)
    return name


def stage_graph(
    *data: StoredStage | str, G: None | nx.DiGraph = None
) -> nx.DiGraph:
    """
    Flattens a list of stored stage data and returns a graph
    """
    if G is None:
        G = nx.DiGraph()

    for d in data:
        # Add the node to the tree!
        name = stage_name(d)
        if name in G.nodes:  # Exists in graph
            if isinstance(d, StoredStage):
                dup_data = G.nodes[name]["data"]
                # Database actually links them together. Do is check
                if isinstance(dup_data, StoredStage):
                    if d is dup_data:
                        continue
                    else:
                        raise Exception(f"Multiple definitions for '{name}'!")
                else:  # Upgrade from None -> Stored Stage
                    G.nodes[name]["data"] = d
            else:
                continue  # NOOP for just strings

        # Add the node!
        if isinstance(d, str):
            G.add_node(name, data=None)
            continue
        else:
            G.add_node(name, data=d)

        # Now add link data and create relationship
        for l in flatten_links(d.links):
            l_name = stage_name(l)
            stage_graph(l, G=G)  # Recursivly collect info
            G.add_edge(name, l_name)
    return G


def flatten_links(
    links: Dict[str, str | StoredStage | List[str | StoredStage]],
) -> Iterable[str | StoredStage]:
    """Flattens a list of link names and/or data"""
    for l in links.values():
        if isinstance(l, List):
            for _l in l:
                yield _l
        else:  # Single value
            yield l
