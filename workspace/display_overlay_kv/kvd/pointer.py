import abc

from kivy.graphics import Color, Line, Ellipse, GraphicException

from drawable import Drawable
from drawableTypes import DrawableType


class Pointer(Drawable):

    DEFAULT_POINTER_COLOR = (0.5, 1, 0.5, 1)
    POINTER_RADIUS = 15
    POINTER_WIDTH = 30
    POINTER_HEIGHT = 30
    POINTER_BORDER_WIDTH = 1
    POINTER_COLOR_MODE = 'rgba'

    def __init__(self, center, color=DEFAULT_POINTER_COLOR):
        self.drawableType = DrawableType.Pointer
        self.center = center
        self.color = color
        # the unique Annotation IDentifier
        self.anid = self.UUID()

    # Must be called from within a `with canvas: `
    def draw(self, window, group):
        Color(self.color[0],
              self.color[1],
              self.color[2],
              self.color[3],
              mode=self.POINTER_COLOR_MODE)
        Line(ellipse=(self.center.x - self.POINTER_RADIUS,
                      self.center.y - self.POINTER_RADIUS,
                      self.POINTER_WIDTH,
                      self.POINTER_HEIGHT),
             width=self.POINTER_BORDER_WIDTH,
             group=group)

Drawable.register(Pointer)
