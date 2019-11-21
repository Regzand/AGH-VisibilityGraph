from typing import Optional, Tuple, List

import arcade

from app.drawing import draw_segment
from app.service import DisplayService
from geometry import Segment, Point, Collection, intersection, dist

# settings
SNAP_RADIUS = 20


class SegmentsCreateService(DisplayService):
    """ Class responsible for managing segments collection. """

    def __init__(self, collection: Collection):
        self.collection = collection
        self.points: Optional[List[Point, Point]] = None
        self.active: bool = False

    def on_mode_change(self, mode: str):
        self.active = (mode == 'segments')

        if not self.active:
            self.points = None

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if not self.active:
            return

        if self.active and self.points:
            self.points[1] = self.snap_point(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if not self.active:
            return
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.points:
            self.collection.segments.add(Segment(*self.points))
            self.points = None
        else:
            point = self.snap_point(x, y)
            self.points = [point, point]

    def draw(self):
        if self.active and self.points:
            draw_segment(Segment(*self.points), color=arcade.color.ANDROID_GREEN)

    def snap_point(self, x: float, y: float) -> Point:
        p = Point(x, y)
        for p2 in self.collection.all_points:
            if dist(p, p2) < SNAP_RADIUS:
                return p2
        return p
