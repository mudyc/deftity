# deftity - a tool for interaction architect
#
# Copyright (C) 2008, 2009 Matti Katila
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


# Written by 2008, 2009 Matti J. Katila


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
    def draw(self, cx, x, y, w=1, h=1):
        self.x, self.y = x, y
        self.w, self.h = w, h
        cx.identity_matrix()
        cx.new_path()
        cx.rectangle(x,y, w,h)
        cx.set_source(ACTION_BG)
        cx.close_path()
        cx.fill_preserve()
        self.write(cx, self.label)

    def set_tool(self, tool):
        self.tool = tool

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

import pages


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

class Quit(Action):
    def __init__(self):
        self.label = 'Quit'

class Page(Action):
    def __init__(self):
        self.label = 'Page'

    def set_tool(self, tool):
        self.tool = tool

    def activate(self):
        #Action.activate(self)
        self.tool.action_node = 'page'
        self.tool.redraw()

class TitlePage(Action):
    def __init__(self):
        self.label = 'Title page'
        
    def activate(self):
        Action.activate(self)
        self.tool.add_component(pages.TitlePage())
