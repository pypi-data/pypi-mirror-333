# SPDX-FileCopyrightText: 2022-2025 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .line import Line
    from .point import Point


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pair_projections_lines(obj1: Line, obj2: Line) -> None:
    """Include each other in the projections collection."""
    if obj2.key == "xyz":
        obj1.projections["xyz"].append(obj2)
    else:
        obj1.projections[obj2.key] = obj2
    if obj1.key == "xyz":
        obj2.projections["xyz"].append(obj1)
    else:
        obj2.projections[obj1.key] = obj1

    pair_projections_points(obj1.start, obj2.start)
    pair_projections_points(obj1.end, obj2.end)


def pair_projections_points(obj1: Point, obj2: Point) -> None:
    """Include each other in the projections collection."""
    if obj2.key == "xyz":
        obj1.projections["xyz"].append(obj2)
    else:
        obj1.projections[obj2.key] = obj2
    if obj1.key == "xyz":
        obj2.projections["xyz"].append(obj1)
    else:
        obj2.projections[obj1.key] = obj1
