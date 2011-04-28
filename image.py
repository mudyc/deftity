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
import tool
import actions

class ImgComp(tool.Component):
    def __init__(self):
        self.wh = [100,100]
        self.xy = [0,0]
        self.data = { 'file': '' }
        self.act = actions.TextfieldAct( \
            'File:', 0, 20, 400, 16, 'file', self.get_data)
        self.img = None
    def pos(self, x,y): self.xy = [x,y]
    def size(self, w,h):
        self.wh = [w,h]
        if self.img == None: return
        ratio = float(self.img.get_width())/float(self.img.get_height())
        ratio2 = float(w)/float(h)
        print self.wh, w, h, ratio, ratio2
        # intent is to make bigger?
        int_bigger = w*h > self.wh[0]*self.wh[1]
        bigger = w*(w/ratio) < (h*ratio*h) 
        if bigger and int_bigger or not bigger and not int_bigger:
            self.wh = [h*ratio, h]
        elif bigger and not int_bigger or not bigger and int_bigger:
            self.wh = [w, w/ratio]
        
    def xywh(self): return (self.xy[0], self.xy[1], self.wh[0], self.wh[1])
    def get_data(self): return self.data
    def save_data(self):
        ret = tool.Component.save_data(self)
        ret['data'] = self.data
        return ret
    def load_data(self, cs):
        self.load()
    def mouse_released(self, tc, mx, my):
        tc.cursor.set_obj(self)
    def key(self, k, cur):
        self.act.key(k, cur)
        self.img = None
        self.wh = [100,100]
        self.load()
    def load(self):
        try:
            print 'file', self.data['file']
            self.img = cairo.ImageSurface.create_from_png(self.data['file'])
            width = self.img.get_width()
            height = self.img.get_height()
            if float(width)/float(height) - float(self.wh[0])/float(self.wh[1]) > 0.05:
                pass #self.wh = [ width, height ]
            self.imgpat = cairo.SurfacePattern(self.img)
        except: traceback.print_exc()
        
    def draw(self, c, tc, mx, my):
        x,y,w,h = self.xywh()
        c.new_path()
        c.rectangle(x,y,w,h)
        c.close_path()
        if self in tc.selected_comps:
            c.set_source_rgb(1,0,0)
        else:
            c.set_source_rgb(0,0,0)
        c.stroke()

        if not (self.img == None or self.data['file'] == ''):
            screensize = self.wh
            width = self.img.get_width()
            height = self.img.get_height()
            scaler = cairo.Matrix()
            #scaler.scale(1/tc.tool.zoom, 1/tc.tool.zoom)
            scaler.translate(-x, -y)
            matrix = cairo.Matrix(xx=width/float(w), yy=height/float(h))
            scaler = scaler.multiply(matrix)
            self.imgpat.set_matrix(scaler)
            self.imgpat.set_filter(cairo.FILTER_BEST)

            #canvas = cairo.ImageSurface(cairo.FORMAT_ARGB32,320,240)
            #ctx = cairo.Context(canvas)
            c.set_source(self.imgpat)
            c.paint()
        else:
            print x, y, self.act.x, self.act.y, mx, my, self.is_close(mx, my)

        if self.is_close(mx, my):
            self.act.draw(c, x+self.act.x, y+self.act.y, True)
