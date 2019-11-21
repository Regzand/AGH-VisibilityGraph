import arcade

from app.drawing import draw_point, draw_segment, draw_polygon
from app.service import DisplayService
from geometry import Collection, Point, dist, Segment, Polygon


class RemoveService(DisplayService):
    """ Service responsible for removing elements form collection. """

    def __init__(self, collection: Collection):
        self.collection = collection
        self.highlighted = None
        self.active = False

    def on_mode_change(self, mode: str):
        self.active = (mode == 'remove')

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.active:
            self.highlighted = self.find_element(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.active and self.highlighted:
            self.collection.remove(self.highlighted)
            self.highlighted = None

    def draw(self):
        if isinstance(self.highlighted, Point):
            draw_point(self.highlighted, color=arcade.color.ALIZARIN_CRIMSON)
        elif isinstance(self.highlighted, Segment):
            draw_segment(self.highlighted, color=arcade.color.ALIZARIN_CRIMSON)
        elif isinstance(self.highlighted, Polygon):
            draw_polygon(self.highlighted, edge_color=arcade.color.ALIZARIN_CRIMSON, fill=False)

    def find_element(self, x: float, y: float, radius: float = 20.0):
        """ Returns element from collection that is in radius. """
        p = Point(x, y)

        for p2 in self.collection.points:
            if dist(p, p2) < radius:
                return p2

        for seg in self.collection.segments:
            for p2 in seg:
                if dist(p, p2) < radius:
                    return seg

        for poly in self.collection.polygons:
            for p2 in poly.points:
                if dist(p, p2) < radius:
                    return poly

        return None
