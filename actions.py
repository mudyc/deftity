
"""
What is an action?
==================

A widget is something that may
- draw itself,
- be bound to action, and
- be part of widget tree.

An action is something that may
- draw itself, and
- be bound to action.


"""

import cairo


ACTION_BG = cairo.SolidPattern(1,1,1,.6)


class Action(object):
    def __init__(self):
        self.label = ''
    def draw(self, cx, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        cx.identity_matrix()
        cx.new_path()
        cx.rectangle(x,y, w,h)
        cx.set_source(ACTION_BG)
        cx.close_path()
        cx.fill_preserve()
        self.write(cx, self.label)

    def is_hit(self,x,y):
        return self.x < x < self.x+self.w and \
               self.y < y < self.y+self.h
    def activate(self):
        self.callback()

    def write(self, cr, s):
        cr.set_font_size(12)
        cr.set_source_rgb(0,0,0)
        fascent, fdescent, fheight, fxadvance, fyadvance = cr.font_extents()
        for cx, letter in enumerate(s):
            xbearing, ybearing, width, height, xadvance, yadvance = (
                    cr.text_extents(letter))
            cr.move_to(self.x,# + cx + 0.5 - xbearing - width / 2,
                    self.y +self.h/2) # + 0.5 - fdescent + fheight / 2)
            cr.show_text(s)

class Screen(Action):
    def __init__(self):
        self.label = 'Screen'

class Text(Action):
    def __init__(self):
        self.label = 'Text'

class Line(Action):
    def __init__(self):
        self.label = 'Line'

class Arrow(Action):
    def __init__(self):
        self.label = 'Arrow'

class Non(Action):
    def __init__(self):
        self.label = 'None'

class Rectangle(Action):
    def __init__(self):
        self.label = 'Rect'

class Circle(Action):
    def __init__(self):
        self.label = 'Circle'
