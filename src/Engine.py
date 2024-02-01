from .Sprite import Sprite
import src as utils

class Engine:
    def __init__(self) -> None:
        self.sprites = []

    def add_sprite(self, position: list, size: list) -> None:
        self.sprites.append(Sprite(position, size))

    def update(self) -> None:
        for sprite in self.sprites:
            sprite.update()