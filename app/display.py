""" Arcade based presentation of algorithms. """
from typing import List, Dict, Tuple

import arcade

from app.service import DisplayService


class Display(arcade.Window):
    """ Creates interactive display. """

    def __init__(self, title: str, services: List[DisplayService], modes: Dict[int, Tuple[str, str]]):
        """ Creates display. """
        super().__init__(title=title, resizable=True)
        arcade.set_background_color(arcade.color.BLACK)

        self.modes = modes
        self.mode: str = "none"
        self.services: List[DisplayService] = services

        self.change_mode(list(self.modes.values())[0][1])

    @staticmethod
    def run():
        """ Starts display. """
        arcade.run()

    def on_key_release(self, symbol: int, modifiers: int):
        # change modes keys
        if symbol in self.modes:
            self.change_mode(self.modes[symbol][1])

        for s in self.services:
            s.on_key_release(symbol, modifiers)

    def change_mode(self, mode: str):
        self.mode = mode
        for s in self.services:
            s.on_mode_change(mode)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for s in self.services:
            s.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for s in self.services:
            s.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        for s in self.services:
            s.on_mouse_release(x, y, button, modifiers)

    def on_draw(self):
        arcade.start_render()

        # draw services
        for s in self.services:
            s.draw()

        # draw mode info
        arcade.draw_xywh_rectangle_filled(0, 0, arcade.get_viewport()[1], 22, arcade.color.BLACK_BEAN)
        arcade.draw_text(self.mode.upper(), 5, 5, arcade.color.BLACK, bold=True)
        arcade.draw_text(
            ' '.join(f'({m[0]}) {m[1]}' for m in self.modes.values()),
            arcade.get_viewport()[1]-5, 5, arcade.color.BLACK, anchor_x='right'
        )

    def on_update(self, delta_time: float):
        for s in self.services:
            s.update(delta_time)
