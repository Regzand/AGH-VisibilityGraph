""" Defines basic geometric structures and operations. """
import math
from dataclasses import dataclass
from typing import NamedTuple, Optional, Tuple, Iterator


class Point(NamedTuple):
    """ Defines point in 2D space. """
    x: float
    y: float

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'


@dataclass(frozen=True)
class Segment:
    """ Defines segment in 2D space. """
    p1: Point
    p2: Point

    def __eq__(self, other):
        """ Compares segments so that (p1, p2) == (p2, p1). """
        if not isinstance(other, Segment):
            return False
        return (self.p1 == other.p1 and self.p1 == other.p1) or (self.p1 == other.p2 and self.p2 == other.p1)

    def __hash__(self):
        """ Creates hash so that hash(p1, p2) == hash(p2, p1) """
        return hash((self.p1, self.p2) if self.p1 <= self.p2 else (self.p2, self.p1))

    def __iter__(self) -> Iterator[Point]:
        """ Makes segment iterable to simplify usage. """
        yield self.p1
        yield self.p2

    def __repr__(self) -> str:
        return f'Segment(({self.p1.x}, {self.p1.y}), ({self.p2.x}, {self.p2.y}))'


@dataclass(init=False, frozen=True)
class Polygon:
    """ Defines polygon in 2D space. """
    points: Tuple[Point, ...]

    def __init__(self, *points: Point):
        """ Creates constructor that accepts points as *args instead of tuple. """
        object.__setattr__(self, 'points', points)

    def __iter__(self) -> Iterator[Point]:
        """ Makes polygon iterable to simplify usage. """
        return iter(self.points)

    @property
    def segments(self) -> Iterator[Segment]:
        """ Creates iterator of segments in this polygon, starting from segment that ends on point 0. """
        for i in range(len(self.points)):
            yield Segment(self.points[i-1], self.points[i])


def dist(p1: Point, p2: Point) -> float:
    """
    Returns distance between given points.
    """
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


def orient(a: Point, b: Point, c: Point) -> float:
    """ Returns orientation relative of point c relative to a,b segment. """
    return a.x * b.y + b.x * c.y + c.x * a.y - a.x * c.y - b.x * a.y - c.x * b.y


def angle(a: Point, b: Point) -> float:
    """ Calculates relative angle [0, pi] between given vectors. """
    len_a = math.sqrt(a.x**2 + a.y**2)
    len_b = math.sqrt(b.x**2 + b.y**2)
    return math.acos((a.x*b.x + a.y*b.y) / (len_a * len_b))


def angle_between_points(a: Point, b: Point, c: Point) -> float:
    """ Calculates relative angle [0, pi] between vectors [b, a] and [b, c]. """
    return angle(Point(a.x-b.x, a.y-b.y), Point(c.x-b.x, c.y-b.y))


def angle_to_xaxis(p1: Point, p2: Point) -> float:
    """ Returns angle [0, 2pi] between segment, created from given two points, and x-axis. """
    a = math.atan2(p2.y - p1.y, p2.x - p1.x)
    return 2 * math.pi + a if a < 0 else a


def parametric_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Optional[Tuple[float, float]]:
    """
    Finds parameters of intersection of two given lines (each defined by two points).
    Based on: http://www.cs.swan.ac.uk/~cssimon/line_intersection.html by Simon Walton.
    """

    # calculate values
    numerator1 = (p3.y - p4.y) * (p1.x - p3.x) + (p4.x - p3.x) * (p1.y - p3.y)
    numerator2 = (p1.y - p2.y) * (p1.x - p3.x) + (p2.x - p1.x) * (p1.y - p3.y)
    denominator = (p4.x - p3.x) * (p1.y - p2.y) - (p1.x - p2.x) * (p4.y - p3.y)

    # if denominator is 0 then lines are parallel or are overlapping
    if denominator == 0:
        return None

    return numerator1 / denominator, numerator2 / denominator


def intersection(p1: Point, p2: Point, p3: Point, p4: Point,
                 restriction_1: str = 'line', restriction_2: str = 'line') -> Optional[Point]:
    """
    Returns intersection point (or None) of given (possibly restricted) lines.

    Possible line restrictions:
        - 'line' - no restriction, so its a line
        - 'segment' - restrictions on both ends, intersection has to be between given points
        - 'ray' - restriction on first point, intersection has to be on ray starting from first point
        - 'ray-inv' - restriction on second point, intersection has to be on ray starting from second point

    :param p1: first point of first line
    :param p2: second point of first line
    :param p3: first point of second line
    :param p4: second point of second line
    :param restriction_1: restriction for first line as describes above
    :param restriction_2: restriction for second line as describes above
    :return: intersection point or None
    """

    # get intersection parameters
    parameters = parametric_intersection(p1, p2, p3, p4)
    if parameters is None:
        return None
    t1, t2 = parameters

    # apply checks
    if restriction_1 in ['segment', 'ray'] and t1 < 0:
        return None
    if restriction_2 in ['segment', 'ray'] and t2 < 0:
        return None
    if restriction_1 in ['segment', 'ray-inv'] and t1 > 1:
        return None
    if restriction_2 in ['segment', 'ray-inv'] and t2 > 1:
        return None

    # return intersection point
    return Point(
        p1.x + t1 * (p2.x - p1.x),
        p1.y + t1 * (p2.y - p1.y)
    )
