from app.drawing import draw_point, draw_segment, draw_polygon
from app.service import DisplayService
from geometry import Collection


class DrawService(DisplayService):
    """ Service responsible for drawing collection of 2d entities. """

    def __init__(self, collection: Collection, draw_kwargs: dict = None):
        self.collection = collection
        self.draw_kwargs = draw_kwargs or {}

    def draw(self):
        for p in self.collection.points:
            draw_point(p, **self.draw_kwargs)
        for s in self.collection.segments:
            draw_segment(s, **self.draw_kwargs)
        for p in self.collection.polygons:
            draw_polygon(p, **self.draw_kwargs)
