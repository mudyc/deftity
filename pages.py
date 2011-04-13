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

import actions


"""The page component drawn on screen.

Paper size of A4 is 210 x 297 mm. Cairo wants pixel size and the
resolution is 1 pixel = 1/72 inch, where inch is 2.54 cm.
1 inch = 25.4 mm
1 pixel = 1/72 inch = 25.4/72 mm
1 mm = 1/(25.4/72) pixel
210 x 297 mm = 595.2755 x 841.889 pixels
"""

class Page:
    def __init__(self):
        self.wh = ( 1./(25.4/72)*297., 1./(25.4/72)*210. )
        self.xy = [ 0,0 ]
        self.actions = []
    def xywh(self):
        return ( self.xy[0], self.xy[1], self.wh[0], self.wh[1])
    def pos(self, x,y):
        self.xy = [x, y]

    def write(self, cr, s, x, y, size):
        cr.set_font_size(size)
        cr.set_source_rgb(0,0,0)
        fascent, fdescent, fheight, fxadvance, fyadvance = cr.font_extents()
        for cx, letter in enumerate(s):
            xbearing, ybearing, width, height, xadvance, yadvance = (
                    cr.text_extents(letter))
            cr.move_to(x,# + cx + 0.5 - xbearing - width / 2,
                    y) # + 0.5 - fdescent + fheight / 2)
            cr.show_text(s)
    def is_close(self,x0,y0):
        x,y,w,h = self.xywh()
        return x-70 < x0 < x+w+70 and \
               y-70 < y0 < y+h+70

    def draw(self, c):
        x,y,w,h = self.xywh()
        for act in self.actions:
            act.draw(c, x+act.x, y+ act.y, act.w, act.h)

class LabelTextfieldAction(actions.Action):
    def __init__(self, label, xywh):
        self.label = label
        self.xywh = xywh
    def draw(self, c):
        c.new_path()
        x,y,w,h = self.xywh
        c.rectangle(x,y,w,h)
        c.close_path()
        c.set_source(cairo.SolidPattern(1,0,.7, .2))
        c.fill_preserve()
        self.write(c, self.label+ self.title, x/3, w/2, 64)
        

class TitlePage(Page):
    class TitleAct(LabelTextfieldAction):
        pass
    
    def __init__(self):
        Page.__init__(self)
        self.title = ''
        self.subtitle = ''
        self.author = ''
        self.date = ''
    def draw(self, c, mx, my):
        x,y,w,h = self.xywh()
        c.new_path()
        c.rectangle(x,y,w,h)
        c.close_path()
        c.set_source_rgb(0,0,0)
        c.stroke()
        self.write(c, 'Title page', x,y, 40)

        Page.draw(self, c)


        if self.is_close(mx,my):
            c.new_path()
            c.rectangle(x,y,w,h)
            c.close_path()
            c.set_source(cairo.SolidPattern(1,0,.7, .2))
            c.fill_preserve()
            self.write(c, 'Title: '+ self.title, x/3, w/2, 64)

