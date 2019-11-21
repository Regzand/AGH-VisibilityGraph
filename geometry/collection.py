from dataclasses import dataclass, field
from itertools import chain
from typing import List, Union, Set

from geometry import Point, Segment, Polygon


@dataclass
class Collection:
    """ Collection of 2d entities. """
    points: Set[Point] = field(default_factory=set)
    segments: Set[Segment] = field(default_factory=set)
    polygons: Set[Polygon] = field(default_factory=set)

    @property
    def all_points(self):
        """ Returns set of all points in collection. """
        return set(chain(
            self.points,
            *self.segments,
            *[poly.points for poly in self.polygons]
        ))

    @property
    def all_segments(self):
        """ Returns set of all segments in collection. """
        return set(chain(
            self.segments,
            *[poly.segments for poly in self.polygons]
        ))

    def add(self, element: Union[Point, Segment, Polygon]):
        """ Adds given element to corresponding list. """
        self._get_list(element).add(element)

    def remove(self, element: Union[Point, Segment, Polygon]):
        """ Removes given element from corresponding list. """
        self._get_list(element).remove(element)

    def _get_list(self, element: Union[Point, Segment, Polygon]):
        if isinstance(element, Point):
            return self.points
        if isinstance(element, Segment):
            return self.segments
        if isinstance(element, Polygon):
            return self.polygons
        raise ValueError('Type not supported')
