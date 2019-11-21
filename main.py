import arcade

from app import Display, SegmentsCreateService, PolygonsCreateService, AlgorithmService
from app.draw_service import DrawService
from app.points_service import PointsCreateService
from app.remove_service import RemoveService
from geometry import Collection, visibility_graph_brute, visibility_graph

if __name__ == "__main__":

    collection = Collection()

    display = Display(
        'Test',
        [
            AlgorithmService(collection, visibility_graph),
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
