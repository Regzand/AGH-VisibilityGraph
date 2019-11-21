import arcade

from geometry import Segment, Polygon, Point

POINT_SIZE = 2
SEGMENT_COLOR = arcade.color.WHITE_SMOKE
POINT_COLOR = arcade.color.WHITE_SMOKE
POLYGON_EDGE_COLOR = arcade.color.WHITE_SMOKE
POLYGON_FILL_COLOR = arcade.color.EERIE_BLACK


def draw_point(p: Point, color: tuple = POINT_COLOR, size: int = POINT_SIZE):
    arcade.draw_circle_filled(*p, size, color=color)


def draw_segment(s: Segment, color: tuple = SEGMENT_COLOR):
    """ Utility tool that draws segment only if ints length is not 0 to prevent arcade errors. """
    if s.p1 != s.p2:
        arcade.draw_line(*s.p1, *s.p2, color=color)
        draw_point(s.p1, color=color)
        draw_point(s.p2, color=color)


def draw_polygon(poly: Polygon, fill: bool = True,
                 edge_color: tuple = POLYGON_EDGE_COLOR, fill_color: tuple = POLYGON_FILL_COLOR):
    """ Draws given polygon. """
    if fill:
        arcade.draw_polygon_filled(poly.points, color=fill_color)
    arcade.draw_polygon_outline(poly.points, color=edge_color)
    for p in poly.points:
        draw_point(p, color=edge_color)
