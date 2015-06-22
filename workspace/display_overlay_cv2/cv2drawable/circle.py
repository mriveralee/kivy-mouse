import abc
import cv2
import drawable
import drawableTypes as DT

class Circle(object):

    def __init__(self, center, radius, color, thickness=1, lineType=8):
        self.drawableType = DT.Circle
        self.center = center
        self.radius = radius
        self.color = color
        self.thickness = thickness
        self.lineType = lineType

    def draw(self, window):
        cv2.circle(window, self.center, self.radius, self.color, self.thickness)

Drawable.register(Circle)
