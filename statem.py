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

import traceback
import cairo
import pango

import tool
import actions
import math

class SM(tool.Component):
    def __init__(self):
        self.xy = [0,0]
    def pos(self, x,y): self.xy = [x,y]
    def xywh(self): return (self.xy[0], self.xy[1], self.wh[0], self.wh[1])

class Start(SM):
    def __init__(self):
        self.wh = [25,25]
    def draw(self, c, tc, mx, my):
        x,y,w,h = self.xywh()
        c.new_path()
        c.arc(x+w/2,y+h/2, w/2, 0, 2 * math.pi)
        c.close_path()
        if self in tc.selected_comps:
            c.set_source_rgb(1,0,0)
        else:
            c.set_source_rgb(0,0,0)
        c.fill_preserve()

class End(SM):
    def __init__(self):
        self.wh = [90,18]
    def draw(self, c, tc, mx, my):
        x,y,w,h = self.xywh()
        c.new_path()
        c.rectangle(x,y,w,h)
        c.close_path()
        if self in tc.selected_comps:
            c.set_source_rgb(1,0,0)
        else:
            c.set_source_rgb(0,0,0)
        c.fill_preserve()

class State(SM):
    def __init__(self):
        self.wh = [80,70]
        self.data = { 'text': 'Text' }
        self.act = actions.TextareaAct( \
            '', 0, 20, 80, 50,12, 'text', self.get_data, pango.ALIGN_CENTER)
    def size(self, w, h):
        self.wh = [w, h]
        self.act = actions.TextareaAct( \
            '', 0, 20, w, h-20,12, 'text', self.get_data, pango.ALIGN_CENTER)
    def get_data(self): return self.data
    def save_data(self):
        ret = tool.Component.save_data(self)
        ret['data'] = self.data
        return ret
    def mouse_released(self, tc, mx, my):
        x,y,w,h = self.xywh()
        x = mx - x
        y = my - y
        self.act.mouse_released(tc, x, y)
    def key(self, k, cur):
        actions.KeyHandler.key(self.act, k, cur, {'Return': '\n'})

    def draw(self, c, tc, mx, my):
        x,y,w,h = self.xywh()
        r = 30
        c.new_path()
        # see http://cairographics.org/cookbook/roundedrectangles/
        c.move_to(x+r,y)                    
        c.line_to(x+w-r,y)                  
        c.curve_to(x+w,y,x+w,y,x+w,y+r)     
        c.line_to(x+w,y+h-r)                
        c.curve_to(x+w,y+h,x+w,y+h,x+w-r,y+h)
        c.line_to(x+r,y+h)                   
        c.curve_to(x,y+h,x,y+h,x,y+h-r)      
        c.line_to(x,y+r)                     
        c.curve_to(x,y,x,y,x+r,y)            
        
        #c.rectangle(x, y, w, h)
        c.close_path()
        if self in tc.selected_comps:
            c.set_source_rgb(1,0,0)
        else:
            c.set_source_rgb(0,0,0)
        c.stroke()#fill_preserve()

        self.act.draw(c, x+self.act.x, y+self.act.y, self.is_close(mx, my))
