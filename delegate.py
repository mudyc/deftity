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


"""Implements cairo context and maps events to, well, methods...

Tries to hide gtk from the tool.
"""

import gtk, tool
import sys
import cairo

class Delegate(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.add_events(
            gtk.gdk.EXPOSURE_MASK
            | gtk.gdk.BUTTON_PRESS_MASK
            | gtk.gdk.BUTTON_RELEASE_MASK
            | gtk.gdk.POINTER_MOTION_MASK
            | gtk.gdk.KEY_PRESS_MASK
            | gtk.gdk.KEY_RELEASE_MASK
            )
        self.set_flags(gtk.CAN_FOCUS)

        self.the_tool = tool.TheTool()
        t = self.the_tool
        t.redraw = self.queue_draw
        
        self.connect('expose_event', self.expose)
        self.connect('button_press_event', t.mouse_pressed)
        self.connect('button_release_event', t.mouse_released)
        self.connect('motion-notify-event', t.pointer_motion)
        self.connect('key_release_event', t.key_released)
        self.connect('key_press_event', t.key_pressed)


    
    
    def expose(self, widget, event):
        self.context = widget.window.cairo_create()

        print event.area.x, event.area.y, \
              event.area.width, event.area.height

        self.context.rectangle(event.area.x, event.area.y,
                               event.area.width, event.area.height)
        self.context.clip()

        if not self.the_tool.is_quit:
            self.draw(self.context)
        else: # quit
            self.quit()
        
        return False

    def draw(self, c):
        a = self.get_allocation()
        self.the_tool.draw(c, a) #(0,0,a.width, a.height))

    def printer(self, widget, ev):
        #self.the_tool.
        print type(ev)
        #for k in dir(ev):
        #    print k, eval("ev."+k)


    def quit(self):
        print 'quit'
        a = self.get_allocation()
        canvas = cairo.ImageSurface(cairo.FORMAT_ARGB32, a.width, a.height)
        #ctx = cairo.Context(canvas)
        class Hack(cairo.Context):
            def __init__(self, canvas):
                cairo.Context.__init__(self, canvas)
            def rectangle(self, r):
                cairo.Context.rectangle(self, r.x, r.y, r.width, r.height)
        ctx = Hack(canvas)

        self.draw(ctx)
        canvas.write_to_png(sys.argv[1])
        sys.exit(0)
