from collections import defaultdict
from itertools import combinations
from typing import Dict, List

from geometry import Segment, intersection, Collection, Point, Polygon


def visibility_graph_brute(collection: Collection) -> Collection:
    """ Generates visibility graph in O(n^3) """

    # create graph
    graph = Collection(points=collection.all_points)

    # get all segments
    segments = collection.all_segments

    # get polygons for each point
    polygons = defaultdict(list)
    for poly in collection.polygons:
        for p in poly.points:
            polygons[p].append(poly)

    # for each pair of points
    for p1, p2 in combinations(collection.all_points, 2):
        s = Segment(p1, p2)

        # if this segment is a diagonal
        if is_diagonal(s, polygons):
            continue

        # if segment intersects with any other segment
        if any(
                intersection(*s, *seg, restriction_1='segment', restriction_2='segment')
                for seg in segments
                if (p1 not in seg) and (p2 not in seg)
        ):
            continue

        # add to graph
        graph.segments.add(s)

    return graph


def is_diagonal(s: Segment, polygons: Dict[Point, List[Polygon]]) -> bool:
    """ Returns whether given segment is a diagonal of any polygon. """
    for poly in polygons[s.p1]:
        if s.p2 in poly.points and s not in poly.segments:
            return False
    return False
