from dataclasses import dataclass

from geometry import Point


@dataclass(order=True)
class Event:
    """ Defines event point. """
    point: Point
    type: str
