# these-united-states

A Python library for performing reverse geocoding of the United States of America.

## Overview

These-united-states provides a simple, class-based interface to shapefiles from the United States
Census Bureau defining boundaries of U.S. states and territories. States may be queried via 
full state name, abbreviation, or by coordinates (latitude/longitude pairs). State objects contain
some metadata, including the bounding box, area, and polygons defining the state's boundaries.

## Example

```python
>>> import united_states

>>> us = united_states.UnitedStates()

>>> us.from_coords(29.881888, -82.726846)
[State(abbr='FL', name='Florida', bbox=BBox(left=-87.634896, bottom=24.396307999999998, right=-79.974306, top=31.000968))]

>>> us.by_abbr['WA']
State(abbr='WA', name='Washington', bbox=BBox(left=-124.848974, bottom=45.543541, right=-116.916071, top=49.002435999999996))

>>> us.by_name['Alaska']
State(abbr='AK', name='Alaska', bbox=BBox(left=-179.231086, bottom=51.175092, right=179.859681, top=71.439786))
```

## Command-line interface

These-united-states is also usable from the command-line, with the appropriate extras installed.

```
$ pip install "these-united-states[cli,plot]"

$ python -m united_states 29.881888,-82.726846
(29.881888, -82.726846)  Florida

$ python -m united_states --help
Usage: united_states [OPTIONS] [POINT]...

  Lookup U.S. states by coordinate (reverse geocoding).

Options:
  -b, --bbox / --no-bbox          Print state bounding boxes in listing
                                  (implies -l/--list).

  -d, --dc / --no-dc              Include the District of Columbia.
  -x, --exclude TEXT              Exclude states by abbreviation or name.
  -h, --help                      Show this message and exit.
  -i, --include TEXT              Include states by abbreviation or name.
  -l, --list / --no-list          List included states.
  -o, --oconus / --no-oconus      Include states outside the continental U.S.
  -p, --plot / --no-plot          Plot the results (requires matplotlib).
  -s, --seed FLOAT                Seed random number generator for color plot
                                  selection.

  -t, --territories / --no-territories
                                  Include U.S. territories.

  Options may be given multiple times. Options taking arguments are
  additive. Multiple abbreviations or names may be provided in a single
  option using a comma-separated list.
```

## License

[BSD 3-Clause license](LICENSE)
