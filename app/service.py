from abc import ABC


class DisplayService(ABC):
    """ Abstract display service class. """

    def on_mode_change(self, mode: str):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        pass

    def draw(self):
        pass

    def update(self, delta: float):
        pass
