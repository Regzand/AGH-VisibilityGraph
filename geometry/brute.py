from itertools import combinations

from geometry import Segment, intersection, Collection


def visibility_graph_brute(collection: Collection) -> Collection:
    out = Collection()
    segments = collection.all_segments

    for p1, p2 in combinations(collection.all_points, 2):
        s = Segment(p1, p2)

        if not any(intersection(s, seg) for seg in segments if (p1 not in seg) and (p2 not in seg)):
            out.segments.add(s)

    return out
