# deftity - a tool for interaction architect
#
# Copyright (C) 2008, 2009, 2011 Matti Katila
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


# Written by Matti J. Katila, 2008, 2009, 2011 


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
import util
import pangocairo
import pango

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
    def mouse_released(self, x, y): pass

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
import screens

# Toolbox actions
# ===============

class Screen(Action):
    def __init__(self):
        self.label = 'Screen'
    def activate(self):
        self.tool.action_node = 'screen'
        self.tool.redraw()

class WVGAScreen(Action):
    def __init__(self):
        self.label = 'WVGA'
    def activate(self):
        Action.activate(self)
        self.tool.add_component(screens.WVGAScreen())

class Text(Action):
    def __init__(self):
        self.label = 'Text'
    def activate(self):
        import text
        Action.activate(self)
        self.tool.add_component(text.TextComp())

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
        self.label = 'Quit&Save'
    def activate(self):
        Action.activate(self)
        self.tool.store_data()

class Export(Action):
    def __init__(self):
        self.label = 'Export'
    def activate(self):
        import sys
        # PDF export
        w,h = pages.A4_SIZE
        surf = cairo.PDFSurface(sys.argv[1]+'.pdf', w,h)
        pdf = cairo.Context(surf)
        for comp in self.tool.comps:
            pdf.identity_matrix()
            x,y,w,h = comp.xywh()
            pdf.translate(-x,-y)
            comp.draw(pdf, -1000, -1000)
            pdf.show_page()
        surf.finish()

        # Data export
        obs = []
        for comp in self.tool.comps:
            print comp
            obs.append(comp.save_data())
        import json
        print obs
        print json.dumps(obs, indent=4)
        dat = open(sys.argv[1], 'w')
        dat.write(json.dumps(obs, indent=4, ensure_ascii=True))
        dat.close()

        Action.activate(self)

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

class ChangeLogPage(Action):
    def __init__(self):
        self.label = 'Changelog page'
    def activate(self):
        Action.activate(self)
        self.tool.add_component(pages.ChangeLogPage())

class DescriptionPage(Action):
    def __init__(self):
        self.label = 'Description page'
    def activate(self):
        Action.activate(self)
        self.tool.add_component(pages.DescriptionPage())

class EmptyPage(Action):
    def __init__(self):
        self.label = 'Empty page'
    def activate(self):
        Action.activate(self)
        self.tool.add_component(pages.EmptyPage())


# Functional actions
# ==================


class KeyHandler(object):
    def key(self, k):
        if len(k) == 1:
            self.modelF()[self.name] += k
        elif k == 'BackSpace':
            self.modelF()[self.name] = self.modelF()[self.name][:-1]
        elif k == 'space':
            self.modelF()[self.name] += ' '
        elif k == 'period':
            self.modelF()[self.name] += '.'
        elif k == 'comma':
            self.modelF()[self.name] += ','
        elif k == 'question':
            self.modelF()[self.name] += '?'

class TextfieldAct(Action, KeyHandler):
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
            util.write_center(c, content, x, w, y+size, size)
        else:
            util.write(c, content, x, y+size, size)

    def mouse_released(self, x,y, cursor):
        cursor.set_obj(self)
            
class TextareaAct(Action, KeyHandler):
    def __init__(self, label, x,y,w,h, size, name, model):
        self.label = label
        self.x, self.y, self.w, self.h = x,y,w,h
        self.size = size
        self.name = name
        self.modelF = model
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
        KeyHandler.key(self, k)
        if k == 'Return': self.modelF()[self.name] += '\n'
