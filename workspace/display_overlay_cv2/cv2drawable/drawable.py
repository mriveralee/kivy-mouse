import abc
import drawable

class Drawable:
    __metaclass__ = ABCMeta
    
    def getDrawableType(self):
        return self.drawableType

    @abstractmethod
    def draw(self, window):
        return NotImplemented
