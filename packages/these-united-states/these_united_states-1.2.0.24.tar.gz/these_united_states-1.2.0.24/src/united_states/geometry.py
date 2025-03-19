# BSD 3-Clause License
#
# Copyright (c) 2020, Avantus LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Various functions and classes for working with polygons."""

import math
from typing import Any, NamedTuple, Optional, Sequence, Tuple


Point = Tuple[float, float]
Polygon = Sequence[Point]


def on_segment(a: Point, b: Point, c: Point) -> bool:
    """Return True if point b is on line segment ac."""
    ax, ay = a
    bx, by = b
    cx, cy = c
    return min(ax, cx) <= bx <= max(ax, cx) and min(ay, cy) <= by <= max(ay, cy)


def orientation(a: Point, b: Point, c: Point) -> int:
    """Find the orientation of three points.

    Returns 0 if colinear, 1 if clockwise, -1 if counterclockwise.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    left = (by - ay) * (cx - bx)
    right = (bx - ax) * (cy - by)
    # Multiplying 0 and inf produces nan, which is equivalent to zero in this case
    if math.isnan(left):
        left = 0
    if math.isnan(right):
        right = 0
    value = left - right
    if value:
        return 1 if value > 0 else -1
    return 0


def intersects(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Return True if line segments ab and cd intersect."""
    abc = orientation(a, b, c)
    abd = orientation(a, b, d)
    cda = orientation(c, d, a)
    cdb = orientation(c, d, b)
    return (
            (abc != abd and cda != cdb) or
            (not abc and on_segment(a, c, b)) or
            (not abd and on_segment(a, d, b)) or
            (not cda and on_segment(c, a, d)) or
            (not cdb and on_segment(c, b, d))
    )


def contains(polygon: Polygon, point: Point) -> bool:
    """Return True if the polygon contains the given point."""
    it = iter(polygon)
    a = point
    b = (math.inf, a[1])
    try:
        c = first = next(it)
    except StopIteration:
        return False
    loop = True
    count = 0
    while loop:
        try:
            d = next(it)
        except StopIteration:
            d = first
            loop = False
        if intersects(a, b, c, d):
            if not orientation(c, a, d):
                return on_segment(c, a, d)
            count += 1
        c = d
    return count % 2 == 1


class BBox(NamedTuple):
    """Tuple representing a bounding box."""

    left: float
    bottom: float
    right: float
    top: float

    def __str__(self) -> str:
        return f'(left={self.left}, bottom={self.bottom}, right={self.right}, top={self.top})'

    def __and__(self, other: 'BBox') -> Optional['BBox']:
        """Return intersection of bounding boxes."""
        x1, y1, x2, y2 = self
        x3, y3, x4, y4 = other
        x5 = max(x1, x3)
        y5 = max(y1, y3)
        x6 = min(x2, x4)
        y6 = min(y2, y4)
        if x5 > x6 or y5 > y6:
            return None
        return BBox(x5, y5, x6, y6)

    def __or__(self, other: 'BBox') -> 'BBox':
        """Combine bounding boxes."""
        x1, y1, x2, y2 = self
        x3, y3, x4, y4 = other
        return BBox(min(x1, x3), min(y1, y3), max(x2, x4), max(y2, y4))

    def __contains__(self, point: Any) -> bool:
        """Return whether the point is within the bounding box."""
        try:
            x, y = point
            return not not (self.left <= x <= self.right and self.bottom <= y <= self.top)
        except (TypeError, ValueError):
            return False
