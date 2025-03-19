# SPDX-FileCopyrightText: 2022-2025 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""A toolbox to script and generate axonometric drawing operations.

To enable a maximum amount of thinkering, the following API documentation
covers all public objects of the codebase. For scripting,
the :py:class:`Axonometry`, :py:class:`Point` and :py:class:`Line`
classes and their corresponding methods are sufficient.
"""

from __future__ import annotations

from .axonometry import Axonometry
from .config import config_manager
from .drawing import Drawing
from .line import Line
from .plane import Plane
from .point import Point
from .surface import Surface
from .trihedron import Trihedron

__all__ = [
    "Axonometry",
    "Drawing",
    "Line",
    "Plane",
    "Point",
    "Surface",
    "Trihedron",
    "config_manager",
]
