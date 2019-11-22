import arcade

from algorithms import visibility_graph
from app import Display, SegmentsCreateService, PolygonsCreateService, AlgorithmService, DrawService, \
    PointsCreateService, RemoveService
from geometry import Collection

if __name__ == "__main__":

    collection = Collection()

    display = Display(
        'Test',
        [
            AlgorithmService(arcade.key.U, collection, visibility_graph),
            DrawService(collection),
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
