import abc
import cv2
import drawable
import drawableTypes as DT

class Rectangle(object):

    def __init__(self, topLeftCorner, bottomRightCorner, color, thickness=1, lineType=8):
        # TODO (mrivera): take in a center of the rectangle, width and height, then compute
        # TLCorner & BRCorner
        self.drawableType = DT.Rectangle
        self.cornerTopLeft = topLetCorner
        self.cornerBottomRight = bottomRightCorner
        self.color = color
        self.thickness = thickness
        self.lineType = lineType

    def draw(self, window):
        cv2.rectangle(window,
                    self.cornerTopLeft,
                    self.cornerTopRight,
                    self.color,
                    self.thickness,
                    self.lineType)

Drawable.register(Rectangle)
