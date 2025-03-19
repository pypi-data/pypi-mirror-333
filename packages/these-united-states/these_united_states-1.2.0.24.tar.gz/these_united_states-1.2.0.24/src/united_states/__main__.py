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

# mypy: disallow_untyped_decorators=false

import functools
import random
import re
from typing import Iterable, Optional, Tuple, Union

import click

from . import Region, State, UnitedStates
from .geometry import BBox, Point


def show_plot(states: Iterable[State], points: Iterable[Point], *, seed: float = 123) -> None:
    import matplotlib.colors
    from matplotlib import pyplot as plt

    random.seed(seed)
    colors = sorted(matplotlib.colors.CSS4_COLORS.values())
    random.shuffle(colors)
    fig = plt.figure(figsize=(15,10))

    states = sorted(set(states), key=lambda st: st.name)
    for i, state in enumerate(states):
        color = colors[i % len(colors)]
        for start, stop in zip(state.parts, [*state.parts[1:], None]):
            plt.fill(*zip(*state.points[start:stop]), fc=color, ec='gray')
        plt.text(*state.point, state.abbr, ha='center', va='center',
                 bbox={'boxstyle': 'round4', 'fc': 'white', 'ec': 'gray', 'alpha': 0.4})
    for point in set(points):
        y, x = point
        plt.plot((x,), (y,), color='black', marker='+', markersize=8)
        plt.annotate(str(point), (x, y), ha='center', va='bottom')

    # Adjust the plot to initially use a 7:3 aspect ratio
    bbox = functools.reduce(BBox.__or__, (st.bbox for st in states))
    hsize = (bbox.right - bbox.left)
    vsize = bbox.top - bbox.bottom
    if hsize / vsize < 7/3:
        adj = ((vsize * 7/3) - hsize) / 2
        bbox = BBox(bbox.left - adj, bbox.bottom, bbox.right + adj, bbox.top)
    else:
        adj = ((hsize * 3/7) - vsize) / 2
        bbox = BBox(bbox.left, bbox.bottom - adj, bbox.right, bbox.top + adj)
    ax, = fig.axes
    ax.set_xlim(bbox.left - 0.5, bbox.right + 0.5)
    ax.set_ylim(bbox.bottom - 0.5, bbox.top + 0.5)
    plt.show()


def can_plot(ctx: click.Context, param: click.Parameter, value: Optional[bool]) -> Optional[bool]:
    if not value or ctx.resilient_parsing:
        return None
    try:
        import matplotlib
    except ImportError:
        assert param.name
        raise click.BadOptionUsage(param.name, 'plotting requires matplotlib', ctx=ctx)
    return value


class LatLon(click.ParamType):
    name = 'LatLon'

    def convert(self, value: Optional[Union[str, Point]],
                param: Optional[click.Parameter], ctx: Optional[click.Context]) -> Optional[Point]:
        if value is None or isinstance(value, tuple):
            return value
        try:
            lat, lon = (float(i) for i in re.split(r'\s|,', value))
        except (TypeError, ValueError):
            self.fail(f'expected coordinates in "lat,lon" or "lat lon" format; got {value!r}', param, ctx)
        if not -90.0 <= lat <= 90.0:
            self.fail(f'expected -90.0 <= lat <= 90.0; got {lat!r}', param, ctx)
        if not -180.0 <= lon <= 180.0:
            self.fail(f'expected -180.0 <= lon <= 180.0; got {lon!r}', param, ctx)
        return lat, lon


@click.command(
    epilog='Options may be given multiple times. Options taking arguments are additive. '
           'Multiple abbreviations or names may be provided in a single option using '
           'a comma-separated list.')
@click.option('-b', '--bbox/--no-bbox', default=False,
              help='Print state bounding boxes in listing (implies -l/--list).')
@click.option('-d', '--dc/--no-dc', default=False,
              help='Include the District of Columbia.')
@click.option('-x', '--exclude', multiple=True,
              help='Exclude states by abbreviation or name.')
@click.help_option('-h', '--help')
@click.option('-i', '--include', multiple=True,
              help='Include states by abbreviation or name.')
@click.option('-l', '--list/--no-list', 'listing', default=False,
              help='List included states.')
@click.option('-o', '--oconus/--no-oconus', default=False,
              help='Include states outside the continental U.S.')
@click.option('-p', '--plot/--no-plot', default=False, callback=can_plot,
              help='Plot the results (requires matplotlib).')
@click.option('-s', '--seed', type=float, default=123,
              help='Seed random number generator for color plot selection.')
@click.option('-t', '--other/--no-other', default=False,
              help='Include Puerto Rico and the Island Areas.')
@click.argument('point', nargs=-1, type=LatLon())
def main(point: Tuple[Point, ...],
         include: Tuple[str, ...], exclude: Tuple[str, ...],
         dc: bool, oconus: bool, other: bool,
         bbox: bool, listing: bool, plot: bool, seed: float) -> None:
    """Lookup U.S. states by coordinate (reverse geocoding)."""
    if bbox:
        listing = True
    included = set(i.strip() for x in include for i in x.split(','))
    excluded = set(i.strip() for x in exclude for i in x.split(','))

    def filter(state: State) -> bool:
        if not dc and state.abbr == 'DC':
            return False
        if not oconus and state.abbr in ['AK', 'HI']:
            return False
        if not other and state.region == Region.other:
            return False
        if included and state.abbr not in included and state.name not in included:
            return False
        if excluded and (state.abbr in excluded or state.name in excluded):
            return False
        return True

    states = UnitedStates(filter)

    if listing:
        fmt = '{0.abbr}  {0.name:{fill}}  '
        if bbox:
            fmt += '  {0.bbox}'
            fill = f'<{max(len(st.name) for st in states)}'
        else:
            fill = '<'
        for state in states:
            click.echo(fmt.format(state, fill=fill))

    if point:
        max_point = max(len(str(pt)) for pt, _ in point)
        for coord in point:
            click.echo(f'{coord!s:<{max_point}}  {", ".join(sorted(st.name for st in states.from_coords(*coord)))}')

    if plot:
        show_plot(states, point, seed=seed)


if __name__ == '__main__':
    main(prog_name=__package__)
