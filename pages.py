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


"""The page component drawn on screen.

Paper size of A4 is 210 x 297 mm. Cairo wants pixel size and the
resolution is 1 pixel = 1/72 inch, where inch is 2.54 cm.
1 inch = 25.4 mm
1 pixel = 1/72 inch = 25.4/72 mm
1 mm = 1/(25.4/72) pixel
210 x 297 mm = 595.2755 x 841.889 pixels
"""

SIZE_TITLE = 64
SIZE_HEADER = 32
SIZE_TEXT = 12

def write(cr, s, x, y, size):
    cr.set_font_size(size)
    cr.set_source_rgb(0,0,0)
    cr.move_to(x,y)
    cr.show_text(s)
    return

    fascent, fdescent, fheight, fxadvance, fyadvance = cr.font_extents()
    for cx, letter in enumerate(s):
        xbearing, ybearing, width, height, xadvance, yadvance = (
                cr.text_extents(letter))
        cr.move_to(x,# + cx + 0.5 - xbearing - width / 2,
                y) # + 0.5 - fdescent + fheight / 2)
        cr.show_text(s)

def write_center(cr, s, x, w, y, size):
    cr.set_font_size(size)
    x_bear, y_bear, width, height, x_adv, y_adv = cr.text_extents(s)
    write(cr, s, x + (w-width)/2, y, size)

A4_SIZE = ( 1./(25.4/72)*297., 1./(25.4/72)*210. )

class Page(tool.Component):
    def __init__(self):
        self.wh = A4_SIZE
        self.xy = [ 0,0 ]
        self.actions = []
        self.data = {}
    def xywh(self):
        return ( self.xy[0], self.xy[1], self.wh[0], self.wh[1])
    def pos(self, x,y):
        self.xy = [x, y]

    def is_close(self,x0,y0):
        x,y,w,h = self.xywh()
        return x-70 < x0 < x+w+70 and \
               y-70 < y0 < y+h+70

    def draw(self, c, active):
        x,y,w,h = self.xywh()
        for act in self.actions:
            xx,yy = act.x, act.y
            act.draw(c, x+xx, y+yy, active)

    def draw_frame(self, c, label, mx, my):
        x,y,w,h = self.xywh()
        c.new_path()
        c.rectangle(x,y,w,h)
        c.close_path()
        c.set_source_rgb(0,0,0)
        c.stroke()
        write(c, label, x,y-10, 40)

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
        print self.data
        return ret
    def get_data(self): return self.data
       

class TextfieldAct(actions.Action):
    CENTER = 'center'
    def __init__(self, label, x,y,w,h, name, model, align=CENTER):
        self.label = label
        self.x, self.y, self.w, self.h = x,y,w,h
        self.name = name
        self.modelF = model
        self.align = align
    def draw(self, c, x, y, active):
        w, size = self.w, self.h
        content = self.modelF()[self.name]
        if active:
            c.new_path()
            c.rectangle(x,y,w,size)
            c.close_path()
            c.set_source(cairo.SolidPattern(1,0,.7, .2))
            c.fill_preserve()
            
            content = self.label + content

        if self.align == TextfieldAct.CENTER:
            write_center(c, content, x, w, y+size, size)
        else:
            write(c, content, x, y+size, size)

    def mouse_released(self, x,y, cursor):
        cursor.set_obj(self)

    def key(self, k):
        if len(k) == 1:
            self.modelF()[self.name] += k
        elif k == 'BackSpace':
            self.modelF()[self.name] = self.modelF()[self.name][:-1]
        elif k == 'space':
            self.modelF()[self.name] += ' '
        print self.modelF()
            
class TextareaAct(actions.Action):
    def __init__(self, label, x,y,w,h, size, name, model):
        self.label = label
        self.x, self.y, self.w, self.h = x,y,w,h
        self.size = size
        self.name = name
        self.modelF = model
    def draw(self, c, x, y, active):
        w, size = self.w, self.h
        print w
        content = self.modelF()[self.name]
        if active:
            c.new_path()
            c.rectangle(x,y,w,size)
            c.close_path()
            c.set_source(cairo.SolidPattern(1,0,.7, .2))
            c.fill_preserve()

            content = self.label + content

        c.move_to(x, y)
        pctx = pangocairo.CairoContext(c)
        pctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        layout = pctx.create_layout()
        fontname = "Sans "+str(self.size)
        font = pango.FontDescription(fontname)
        layout.set_font_description(font)

        layout.set_width(int(w*pango.SCALE))
        layout.set_wrap(pango.WRAP_WORD_CHAR)
        layout.set_text(content)
        c.set_source_rgb(0, 0, 0)
        pctx.update_layout(layout)
        pctx.show_layout(layout)

    def mouse_released(self, x,y, cursor):
        cursor.set_obj(self)
        print self.label

    def key(self, k):
        if len(k) == 1:
            self.modelF()[self.name] += k
        elif k == 'BackSpace':
            self.modelF()[self.name] = self.modelF()[self.name][:-1]
        elif k == 'space':
            self.modelF()[self.name] += ' '
        print self.modelF()


class TitlePage(Page):
    def __init__(self):
        Page.__init__(self)
        self.data = { 'title': '', 'subtitle': ''}
        x,y,w,h = self.xywh()
        wlim = w
        self.actions.append(TextfieldAct( \
            'Title:', x, h/2-32., wlim, 64, 'title', self.get_data))
        self.actions.append(TextfieldAct( \
            'SubTitle:', x, h/2+40., wlim, 38, 'subtitle', self.get_data))
    def draw(self, c, mx, my):
        Page.draw_frame(self, c, 'Title page', mx, my)

        Page.draw(self, c, self.is_close(mx,my))

class ChangeLogPage(Page):
    def __init__(self):
        Page.__init__(self)
        self.data = { 'titlerow': ['Version', 'Description'],
                      'row1': ['0.1', 'Foo']}
        x,y,w,h = self.xywh()
        wlim = w/2
    def draw(self, c, mx, my):
        Page.draw_frame(self, c, 'Changelog page', mx, my)
        x,y,w,h = self.xywh()
        write_center(c, 'Changelog', x, w, y+2*SIZE_HEADER, SIZE_HEADER)
        
        Page.draw(self, c, self.is_close(mx,my))

class DescriptionPage(Page):
    def __init__(self):
        Page.__init__(self)
        self.data = { 'title': 'Project golas',
                      'text': 'some text'}
        x,y,w,h = self.xywh()
        wlim = w
        self.actions.append(TextfieldAct( \
            'Title:', 0, SIZE_HEADER, wlim, SIZE_HEADER, 
            'title', self.get_data))
        self.actions.append(TextareaAct( \
            'Text:', w/20, 2*SIZE_HEADER, 
            w*18/20, h-2*SIZE_HEADER, SIZE_TEXT, 'text', self.get_data))

    def draw(self, c, mx, my):
        Page.draw_frame(self, c, 'Description page', mx, my)
        x,y,w,h = self.xywh()
        Page.draw(self, c, self.is_close(mx,my))

