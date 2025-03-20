from collections.abc import Hashable, Iterable, Mapping
from itertools import combinations
from typing import TypeVar, cast

from networkx.utils import UnionFind

from recsa import Assembly, Component, is_isomorphic

from .grouping_by_hash import group_assemblies_by_hash

__all__ = ['group_assemblies_by_isomorphism']

_T = TypeVar('_T', bound=Hashable)

def group_assemblies_by_isomorphism(
        id_to_assembly: Mapping[_T, Assembly],
        component_structures: Mapping[str, Component]
        ) -> dict[_T, set[_T]]:
    """Group duplicates by assembly isomorphism.

    Parameters
    ----------
    id_to_assembly : Mapping[_T, Assembly]
        A mapping from IDs to assemblies.
    component_structures : Mapping[str, ComponentStructure]
        A mapping from component kinds to component structures.

    Returns
    -------
    dict[_T, set[_T]]
        A mapping from unique IDs to sets of duplicate IDs.
        Unique IDs are the minimum IDs in each group.
        Duplicate IDs include the unique IDs themselves.
    """
    hash_to_ids = group_assemblies_by_hash(id_to_assembly, component_structures)

    uf = UnionFind(id_to_assembly.keys())

    for hash_, ids in hash_to_ids.items():
        if len(ids) == 1:
            continue

        for id1, id2 in combinations(ids, 2):
            if uf[id1] == uf[id2]:
                continue
            if is_isomorphic(
                    id_to_assembly[id1], id_to_assembly[id2],
                    component_structures):
                uf.union(id1, id2)

    grouped_ids = cast(Iterable[set[_T]], uf.to_sets())
    unique_id_to_ids = {min(ids): ids for ids in grouped_ids}
    return unique_id_to_ids
