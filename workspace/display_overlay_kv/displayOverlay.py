#!/usr/bin/kivy

# import sys
# import numpy as np
# import cv2 as cv2
# import uuid

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException
from kivy.vector import Vector
from random import random
from math import sqrt

import kvd
from kvd.pointer import Pointer


from enum import Enum
from displayOverlayState import DisplayOverlayState

""" Display Overlay using Kivy
""  An image serves as the microscope view port
"""

# Keys
kColor = 'color'
kLines = 'lines'
kLabel = 'label'
kLabelBackground = 'labelBackground'
kLabelBackgroundColor = 'labelBackgroundColor'

kLabelRecWidth = 200
kLabelRecHeight = 100

''' GLOBAL '''
def calculate_points(x1, y1, x2, y2, steps=5):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return None
    o = []
    m = dist / steps
    for i in range(1, int(m)):
        mi = i / m
        lastx = x1 + dx * mi
        lasty = y1 + dy * mi
        o.extend([lastx, lasty])
    return o

class CircularViewPort(object):

    def __init__(self, centerPt, radius ):
        self.centerPt = centerPt
        self.radius = radius


    ''' Returns the point if it is within the bounds of this view point
    '' Otherwise this returns the nearest point on the bounds
    '''
    def restrict_point_to_bounds(self, pt):
        if self.is_point_in_bounds(pt):
            return pt
        v = pt - self.centerPt
        if (v.x == 0 and v.y == 0):
            raise Exception('Cannot restrict center of viewport to viewport')
        vMag = v.length
        a = self.centerPt + (v.normalize() * self.radius)
        return a

    def is_point_in_bounds(self, pt):
        # pt: (h,k) --> (x-h)^2 + (y-k)^2 = r^2
        sqCenterX = (self.centerPt.x - pt.x) ** 2
        sqCenterY = (self.centerPt.y - pt.y) ** 2
        sqRad = self.radius ** 2
        return sqCenterX + sqCenterY <= sqRad


class DisplayOverlay(FloatLayout):

    DISPLAY_OVERLAY_WINDOW_WIDTH = 1400
    DISPLAY_OVERLAY_WINDOW_HEIGHT = 1400

    VIEWPORT_RADIUS = 300
    POINTER_COLOR = (1, 0, 0, 1)
    POINTER_GROUP = 'pointers'

    def __init__(self):
        super(DisplayOverlay, self).__init__()
        self.size.width = self.DISPLAY_OVERLAY_WINDOW_WIDTH
        self.size.height = self.DISPLAY_OVERLAY_WINDOW_HEIGHT
        self.viewPort = CircularViewPort(self.get_viewport_center_point(),
                                         self.VIEWPORT_RADIUS)
        self.state = DisplayOverlayState.IDLE
        self.print_state('init')
        self.pointer = Pointer(Vector(self.size.width / 2, self.size.height / 2),
                               self.POINTER_COLOR)

        self.window = self.get_parent_window()
        if self.window is None:
            # manually set the current window
            from kivy.core.window import Window
            self.window = Window
            self.window.bind(mouse_pos=self.on_mouse_position_changed)
            self.window.bind(on_motion=self.on_motion)
                # on_key_up=partial(self.on_keyboard, 'keyup'),
                # on_key_down=partial(self.on_keyboard, 'keydown'),
                # on_keyboard=partial(self.on_keyboard, 'keyboard'))

    # User's mouse position updated
    def on_mouse_position_changed(self, window, mousePos):
        # Remove old pointer drawing & update pointer position
        self.canvas.remove_group(self.POINTER_GROUP)

        # Restrict pointer to viewport bounds
        self.pointer.center = self.viewPort.restrict_point_to_bounds(Vector(mousePos[0],
                                                                            mousePos[1]))
        with self.canvas:
            # Draw an updated mouse pointer
            self.pointer.draw(self.window, self.POINTER_GROUP)

    def on_motion(self, window, etype, motionEvent):
        pass

    # Debug State
    def print_state(self, methodName=None):
        print "%s in %s" % (self.state, methodName)

    def get_viewport_center_point(self):
        win = self.get_parent_window()
        if win is None:
            return Vector(0,0)
        centerPt = Vector(win.width, win.height) / 2
        return centerPt

    def on_touch_down(self, touch):
        self.state = DisplayOverlayState.DRAGGING
        self.print_state('onTouchDown')


        # Update the viewport center
        self.viewPort.centerPt = self.get_viewport_center_point()

        # Get window
        win = self.get_parent_window()
        # Get the User Dictionary for the touch
        ud = touch.ud

        # Ensure our point is within the view port (if not do nothing)
        touchPt = Vector(touch.x, touch.y)
        if not self.viewPort.is_point_in_bounds(touchPt):
            print 'touched outside view port'
            return False

        ud['group'] = g = str(touch.uid)
        with self.canvas:
            # Draw the touch location lines
            ud[kColor] = Color(random(), 1, 1, mode='hsv', group=g)
            ud[kLines] = (
                Rectangle(pos=(touch.x, 0), size=(1, win.height), group=g),
                Rectangle(pos=(0, touch.y), size=(win.width, 1), group=g),
                Point(points=(touch.x, touch.y), source='particle.png',
                      pointsize=5, group=g))

            # Background label
            ud[kLabelBackgroundColor] = Color(random(), random(), random(), 0.5, mode='rgba', group=g)

            ud[kLabelBackground] = Rectangle(pos=(touch.x, touch.y),
                                            size=(kLabelRecWidth, kLabelRecHeight),
                                            cornerRadius=10,
                                            group=g)
        # Draw the text label of our mouse
        ud[kLabel] = Label(size_hint=(None, None))
        self.update_touch_label(ud[kLabel], touch)
        self.add_widget(ud[kLabel])

        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return

        # Restrict touch point
        touchPt = self.viewPort.restrict_point_to_bounds(Vector(touch.x,
                                                                touch.y))
        touch.x = touchPt.x
        touch.y = touchPt.y
        touch.pos = touchPt

        # Grab user data stored on the touch
        ud = touch.ud

        # Update the line positions
        ud[kLines][0].pos = touch.x, 0
        ud[kLines][1].pos = 0, touch.y

        # Draw the paint dots
        points = ud[kLines][2].points
        oldx, oldy = points[-2], points[-1]
        points = calculate_points(oldx, oldy, touch.x, touch.y)
        if points:
            try:
                lp = ud[kLines][2].add_point
                for idx in range(0, len(points), 2):
                    lp(points[idx], points[idx+1])
            except GraphicException:
                pass

        # Update the the time for our userdata
        import time
        t = int(time.time())
        if t not in ud:
            ud[t] = 1
        else:
            ud[t] += 1

        # Update the label position
        self.update_touch_label(ud[kLabel], touch)

        # Update the label background rectangle
        self.update_touch_label_background(ud[kLabelBackground], touch)


    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['group'])
        self.remove_widget(ud[kLabel])

        # Reset State
        self.state = DisplayOverlayState.IDLE
        self.print_state('onTouchUp')


    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id, touch.x, touch.y, touch.__class__.__name__)
        label.texture_update()
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20

    def update_touch_label_background(self, labelBackground, touch):
        labelBackground.pos = touch.pos

class DisplayOverlayApp(App):
    title = 'DisplayOverlay'
    icon = 'icon.png'

    def build(self):
        return DisplayOverlay()

    def on_pause(self):
        return True

if __name__ == '__main__':
    DisplayOverlayApp().run()
