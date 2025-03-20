"""Define the attributes associated with vertices in a dependency graph."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Generic, Literal

if sys.version_info >= (3, 11):
    from typing import TypedDict
else:  # pragma: no cover
    from typing_extensions import TypedDict

from .constant import V, VertexPredecessors, VertexValue

if TYPE_CHECKING:
    from collections.abc import Callable


class VertexAttributes(TypedDict, Generic[V]):
    """Attributes associated with a vertex in the dependency graph."""

    func: Callable[..., Any] | None
    """An optional function that computes the vertex value.

    If ``None``, the vertex must have a predefined value at the computation stage.
    """
    value: VertexValue
    """The value of the vertex.

    - If the vertex has been computed or assigned a value, it is stored here.
    - If the value is missing, the sentinel :py:data:`turbograph.NA` is used.
    """
    predecessors: VertexPredecessors[V]
    """A sequence of predecessor vertices.

    Predecessors are the input vertices whose values are used to compute
    the current vertex's value. The order of predecessors matters for
    positional argument-based function calls.
    """


VertexAttributeName = Literal["func", "value", "predecessors"]
"""Enumeration of valid attribute names for a vertex."""
