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
        self.act = actions.TextareaAct( \
            '', 0, 20, 80, 50,12, 'caption', self.get_data, pango.ALIGN_CENTER)
    def size(self, w, h):
        self.wh = [w, h]

    def xywh(self):
        return ( self.xy[0], self.xy[1], self.wh[0], self.wh[1])
    def pos(self, x,y):
        self.xy = [x, y]
    def size(self, w,h):
        ratio = float(self.WH[0])/float(self.WH[1])
        # intent is to make bigger?
        int_bigger = w*h > self.wh[0]*self.wh[1]
        bigger = w*(w/ratio) < (h*ratio*h) 
        if bigger and int_bigger or not bigger and not int_bigger:
            self.wh = [h*ratio, h]
        elif bigger and not int_bigger or not bigger and int_bigger:
            self.wh = [w, w/ratio]

        x,y,w,h = self.xywh()
        self.act = actions.TextareaAct( \
            '', 0, h, w, 20,12, 'caption', self.get_data, pango.ALIGN_CENTER)

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
        #util.write_center(c, self.get_data()['caption'], x,w, y+h+20, 16)
        
        self.act.draw(c, x+self.act.x, y+self.act.y, x<mx<x+w and my-20-y < h and my < y+h)

        if self.is_close(mx,my):
            c.new_path()
            c.rectangle(x,y,w,h)
            c.close_path()
            c.set_source(cairo.SolidPattern(.8,.9,1, .2))
            c.fill_preserve()

    def mouse_released(self, tc, mx, my):
        x,y,w,h = self.xywh()
        x = mx - x
        y = my - 20 - y
        self.act.mouse_released(tc, x, y)
    def key(self, k, cur):
        actions.KeyHandler.key(self.act, k, cur)

    def save_data(self):
        ret = tool.Component.save_data(self)
        ret['data'] = self.data
        return ret
    def get_data(self): return self.data
    def is_within(self, X,Y,XW,YH):
        x,y,w,h = self.xywh()
        print x+w, y+h+20, XW, YH, (y+h+20<YH)
        return X < x and Y < y and x+w < XW and y+h+20 < YH



class WVGAScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.wh = self.WH = (800, 480)
        self.size(800,480)
    def draw(self, c, tc, mx, my):
        Screen.draw_frame(self, c, mx, my)
