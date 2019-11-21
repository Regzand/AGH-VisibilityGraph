from typing import Callable

import arcade

from app.draw_service import DrawService
from geometry import Collection


class AlgorithmService(DrawService):
    """ Service that applies given algorithm to data and displays results. """

    def __init__(self, key: int, source_collection: Collection, algorithm: Callable[[Collection], Collection]):
        super().__init__(Collection(), dict(color=arcade.color.CATALINA_BLUE))
        self.key = key
        self.source_collection = source_collection
        self.algorithm = algorithm

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == self.key:
            self.collection = self.algorithm(self.source_collection)
