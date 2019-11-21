from itertools import islice
from typing import Optional, List

import arcade

from app.drawing import draw_segment
from app.service import DisplayService
from geometry import Point, Polygon, Collection, dist, Segment

# settings
SNAP_RADIUS = 20


class PolygonsCreateService(DisplayService):
    """ Class responsible for managing polygons collection. """

    def __init__(self, collection: Collection):
        self.collection = collection
        self.points: Optional[List[Point]] = None
        self.active: bool = False

    def on_mode_change(self, mode: str):
        self.active = (mode == 'polygons')

        if not self.active:
            self.points = None

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if not self.active:
            return

        if self.points:
            self.points[-1] = self.snap_point(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if not self.active:
            return
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        point = self.snap_point(x, y)

        # continue creation
        if self.points:
            # not a starting point -> continue creation
            if point != self.points[0]:
                self.points[-1] = point
                self.points.append(point)
            # starting point -> end creation
            else:
                del self.points[-1]
                self.collection.polygons.add(Polygon(*self.points))
                self.points = None

        # start creation
        else:
            self.points = [point, point]

    def draw(self):
        # draw active polygon
        if self.active and self.points:
            for i in range(1, len(self.points)):
                draw_segment(
                    Segment(self.points[i - 1], self.points[i]),
                    color=arcade.color.ANDROID_GREEN
                )

    def snap_point(self, x: float, y: float) -> Point:
        p = Point(x, y)

        # snap to active polygon
        if self.points:
            for p2 in self.points[:-1]:
                if dist(p, p2) < SNAP_RADIUS:
                    return p2

        # snap to polygons
        for p2 in self.collection.all_points:
            if dist(p, p2) < SNAP_RADIUS:
                return p2
        return p
