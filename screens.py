# deftity - a tool for interaction architect
#
# Copyright (C) 2011 Matti Katila
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


# Written by Matti J. Katila, 2011

import cairo
import pango
import pangocairo

import actions
import tool
import util

"""

"""


class Screen(tool.Component):
    def __init__(self):
        self.xy = [ 0,0 ]
        self.actions = []
        self.data = { 'caption': 'Screen' }
    def xywh(self):
        return ( self.xy[0], self.xy[1], self.wh[0], self.wh[1])
    def pos(self, x,y):
        self.xy = [x, y]

    def is_close(self,x0,y0):
        x,y,w,h = self.xywh()
        return x < x0 < x+w and \
               y < y0 < y+h

    def draw_frame(self, c, mx, my):
        x,y,w,h = self.xywh()
        c.new_path()
        c.rectangle(x,y,w,h)
        c.close_path()
        c.set_source_rgb(0,0,0)
        c.stroke()
        util.write_center(c, self.get_data()['caption'], x,w, y+h+20, 16)

        if self.is_close(mx,my):
            c.new_path()
            c.rectangle(x,y,w,h)
            c.close_path()
            c.set_source(cairo.SolidPattern(.8,.9,1, .2))
            c.fill_preserve()

    def mouse_released(self, mx, my, cur):
        x,y,w,h = self.xywh()
        x = mx - x
        y = my - y
        for act in self.actions:
            if act.is_hit(x, y):
                act.mouse_released(x,y, cur)

    def save_data(self):
        ret = tool.Component.save_data(self)
        ret['data'] = self.data
        return ret
    def get_data(self): return self.data
       



class WVGAScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.wh = (800, 480)
    def draw(self, c, tc, mx, my):
        Screen.draw_frame(self, c, mx, my)
