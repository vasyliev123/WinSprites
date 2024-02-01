import tkinter as tk
from enum import Enum
from src import utils

class DraggableWindow(tk.Toplevel):
    """
    A draggable window class extending tkinter's Toplevel widget.
    """
    def __init__(self):
        super().__init__()
        self.title("WinSprites")
        self.overrideredirect(True)
        self.position = [0, 0]
        self._offset_x = 0
        self._offset_y = 0
        self.is_dragged = False
        self._configure_bindings()

    def _configure_bindings(self):
        """
        Configures event bindings for the window.
        """
        self.bind("<Button-1>", self._click_window)
        self.bind("<B1-Motion>", self._drag_window)
        self.bind("<ButtonRelease-1>", self._release_window)


    def set_window_params(self, position: list, size: list) -> None:
        """
        Sets the window's position and size.
        """
        self.geometry(f"{size[0]}x{size[1]}+{position[0]}+{position[1]}")

    def _click_window(self, event):
        """
        Initiates window drag on mouse click.
        """
        self._offset_x = event.x
        self._offset_y = event.y
        self.is_dragged = True

    def _drag_window(self, event):
        """
        Drags the window based on mouse movement.
        """
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f"+{x}+{y}")

    def _release_window(self, event):
        """
        Stops window drag on mouse button release.
        """
        self.is_dragged = False

class SpriteStates(Enum):
    """
    Enum for sprite states.
    """
    ON_SURFACE = "on_surface"
    SITTING = "sitting"
    FALLING = "falling"

class Sprite:
    """
    A class representing a sprite with a window.
    """
    def __init__(self, position, size) -> None:
        self.window = DraggableWindow()
        self.position = position
        self.size = size
        self.window.set_window_params(position, size)
        self.states = [SpriteStates.ON_SURFACE]
        self.surfaces = []
        self.surfaces_ato_b = []
        self.window.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        """
        Handles window configuration changes.
        """
        if self.window.is_dragged:
            self.position = [event.x, event.y]

    def is_on_surface(self) -> bool:
        """
        Checks if the sprite is on a surface.
        """

        for surface in self.surfaces:
            if self.position[1] + self.size[1] >= surface[1][1] and self.position[1] < surface[1][1]:
                if SpriteStates.ON_SURFACE not in self.states:
                    self.states.append(SpriteStates.ON_SURFACE)
                return (True, surface[1][1] - self.size[1])
        return (False, 0)

    def update(self) -> None:
        """
        Updates the sprite's state based on its environment.
        """
        windows = utils.get_filtered_windows()
        self.surfaces = [((69696969, 'TaskBar'), utils.get_taskbar_dimensions())]
        for window in windows:
            self.surfaces.append(window)

        print(" ########################### ")
        for info, rect in self.surfaces:
            print(f"HWND: {info}, Rect: {rect}")
        print(" ########################### ")
        
        
        print(f"Sprite position: {self.position[1]} {self.position[1] + self.size[1]}")
        if not self.window.is_dragged:
            print(self.is_on_surface())
            if self.is_on_surface()[0]:
                self.position[1] = self.is_on_surface()[1]
            else:
                self.position[1] += 1
                self.window.set_window_params(self.position, self.size)
