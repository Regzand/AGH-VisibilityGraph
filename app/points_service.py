import arcade

from app.service import DisplayService
from geometry import Collection, Point


class PointsCreateService(DisplayService):
    """ Class responsible for creating points. """

    def __init__(self, collection: Collection):
        self.collection = collection
        self.active: bool = False

    def on_mode_change(self, mode: str):
        self.active = (mode == 'points')

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if not self.active:
            return
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        self.collection.points.add(Point(x, y))
