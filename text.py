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

import pango
import pangocairo
import cairo

import tool
import actions


class TextComp(tool.Component, actions.KeyHandler):
    def __init__(self):
        self.wh = [100, 40]
        self.data = { 'text': 'Text..' }
        self.modelF = self.get_data
        self.name = 'text'
    def save_data(self):
        ret = tool.Component.save_data(self)
        ret['data'] = self.data
        return ret
    def get_data(self): return self.data
    def pos(self, x,y): self.xy = [ x,y]
    def xywh(self): return (self.xy[0], self.xy[1], self.wh[0], self.wh[1])
    def draw(self, c, tc, mx, my):
        x,y,w,h = self.xywh()
        if self.is_close(mx, my):
            c.new_path()
            c.rectangle(x,y,w,h)
            c.close_path()
            c.set_source(cairo.SolidPattern(1,0,.7, .2))
            c.fill_preserve()

        c.move_to(x, y)
        pctx = pangocairo.CairoContext(c)
        pctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        layout = pctx.create_layout()
        fontname = "Sans "+str(self.size)
        font = pango.FontDescription(fontname)
        layout.set_font_description(font)

        layout.set_width(int(w*pango.SCALE))
        layout.set_wrap(pango.WRAP_WORD_CHAR)
        layout.set_justify(True)
        layout.set_text(self.modelF()[self.name])
        if self in tc.selected_comps:
            c.set_source_rgb(1, 0, 0)
        else:
            c.set_source_rgb(0, 0, 0)
        pctx.update_layout(layout)
        pctx.show_layout(layout)

    def mouse_released(self, tc, x,y):
        tc.cursor.set_obj(self)

    def key(self, k):
        actions.KeyHandler.key(self, k)
        if k == 'Return': self.modelF()[self.name] += '\n'
        if self.modelF()[self.name] == '':
            self.tool.comps.remove(self)
