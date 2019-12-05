from collections import defaultdict
from functools import cmp_to_key
from itertools import chain
from typing import Iterator, Iterable, Callable, List, Dict, Union

from sortedcontainers import SortedList

from geometry import Collection, Point, Segment, intersection, dist, angle_to_xaxis, orient, angle_between_points


def visibility_graph(collection: Collection) -> Collection:
    """ Generates visibility graph from in O(n^2 log n). """

    # create dict that maps point to segments that it belongs to
    segments = defaultdict(list)
    for seg in collection.all_segments:
        segments[seg.p1].append(seg)
        segments[seg.p2].append(seg)

    # output graph
    graph = Collection(points=collection.all_points)

    # for each point
    for point in graph.points:
        # for each point visible from point
        for visible_point in visible_vertices(point, graph.points, segments):
            # create edge in graph
            graph.segments.add(Segment(point, visible_point))

    return graph


def visible_vertices(point: Point, points: Iterable[Point], segments: Dict[Point, List[Segment]]) -> Iterator[Point]:
    """ Yields points from given points that can be seen from given start point. """

    # remove point from points
    points = filter(lambda x: x != point, points)

    # sort points first by angle and then by distance from point
    points = sorted(points, key=lambda x: (angle_to_xaxis(point, x), dist(point, x)))

    # create sorted list from segments that cross starting ray
    # list is sorted using ray that has to be updated
    ray = Segment(point, Point(point.x + 1, point.y))
    status = SortedList(
        iterable=(
            seg
            for seg in set(chain(*segments.values()))
            if intersection(*ray, *seg, restriction_1='ray', restriction_2='segment') and point not in seg
        ),
        key=status_key(lambda: ray)
    )

    # for each point (they are sorted by angle)
    for p in points:

        # update ray
        ray = Segment(point, p)

        # if p is visible yield it
        if status.bisect_left(p) == 0:
            yield p

        # remove segments from this point
        for seg in segments[p]:
            if orient(point, p, seg.p1 if seg.p2 == p else seg.p2) < 0:
                status.remove(seg)

        # add segments to this point
        for seg in segments[p]:
            if orient(point, p, seg.p1 if seg.p2 == p else seg.p2) > 0:
                status.add(seg)


def status_key(ray_getter: Callable[[], Segment]):
    """ Creates comparision for status structure key that pulls current ray from given function. """

    def compare(a: Union[Point, Segment], b: Union[Point, Segment]):
        # get current ray
        ray = ray_getter()

        if isinstance(a, Point) and isinstance(b, Point):
            return dist(ray.p1, a) - dist(ray.p2, b)

        if isinstance(a, Point) and isinstance(b, Segment):
            pb = intersection(*ray, *b, restriction_1='ray', restriction_2='segment')
            dist_a = dist(ray.p1, a)
            dist_b = dist(ray.p1, pb)
            if dist_a == dist_b:
                return -1
            return dist_a - dist_b

        if isinstance(a, Segment) and isinstance(b, Point):
            pa = intersection(*ray, *a, restriction_1='ray', restriction_2='segment')
            dist_a = dist(ray.p1, pa)
            dist_b = dist(ray.p1, b)
            if dist_a == dist_b:
                return 1
            return dist_a - dist_b

        if isinstance(a, Segment) and isinstance(b, Segment):
            pa = intersection(*ray, *a, restriction_1='ray', restriction_2='segment')
            pb = intersection(*ray, *b, restriction_1='ray', restriction_2='segment')
            dist_a = dist(ray.p1, pa)
            dist_b = dist(ray.p1, pb)
            if dist_a == dist_b:
                pa2 = a.p1 if a.p2 == pa else a.p2
                pb2 = b.p1 if b.p2 == pb else b.p2
                return angle_between_points(ray.p1, ray.p2, pa2) - angle_between_points(ray.p1, ray.p2, pb2)
            return dist_a - dist_b

        raise ValueError(f'Comparator got unexpected types: {type(a)}, {type(b)}')

    # noinspection PyTypeChecker
    return cmp_to_key(compare)
