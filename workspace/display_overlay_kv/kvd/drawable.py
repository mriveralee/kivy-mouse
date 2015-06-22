from abc import ABCMeta, abstractmethod
import uuid
import drawable

class Drawable:
    __metaclass__ = ABCMeta

    def getDrawableType(self):
        return self.drawableType

    def UUID(self):
        return uuid.uuid1().int >> 64

    @abstractmethod
    def draw(self, window):
        return NotImplemented
