import arcade

from algorithms import sweep_line_simple
from app import Display, SegmentsCreateService, PolygonsCreateService, AlgorithmService, PointsCreateService, \
    RemoveService, DrawService
from geometry import Collection

if __name__ == "__main__":

    collection = Collection()

    display = Display(
        'Test',
        [
            DrawService(collection),
            AlgorithmService(arcade.key.S, collection, sweep_line_simple),
            PolygonsCreateService(collection),
            SegmentsCreateService(collection),
            PointsCreateService(collection),
            RemoveService(collection)
        ],
        {
            arcade.key.KEY_1: ('1', 'points'),
            arcade.key.KEY_2: ('2', 'segments'),
            arcade.key.KEY_3: ('3', 'polygons'),
            arcade.key.KEY_0: ('0', 'remove'),
        }
    )

    display.run()
