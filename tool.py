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


"""The Def tool
"""


import gtk
import math
import cairo
import json

class Component(object):
    def __init__(self): pass
    def xywh(self): return (-500,-500,100,100)
    def pos(self, x,y): pass
    def size(self, w, h): pass
    def save_data(self):
        x,y,w,h = self.xywh()
        cz = self.__class__
        cz = cz.__module__ +'.'+cz.__name__
        return {'class': cz, 'x':x,'y':y,'w':w,'h':h }
    def load_data(self): pass
    def is_close(self,x0,y0):
        x,y,w,h = self.xywh()
        return x < x0 < x+w and \
               y < y0 < y+h


import actions


#colors
BG = cairo.SolidPattern(1,1,1)
GRID_FG = cairo.SolidPattern(.8,.8,.8)
TOOLBOX_BG = cairo.SolidPattern(.4,.4,.5, .5)


class Start(Component):
    def draw(self, c, mx,my):
        x,y,w,h = self.xywh()
        c.arc(x,y, w/2, 0, 2 * math.pi)
        c.set_source_rgb(1,.3,1)
        c.fill_preserve()
        c.set_source_rgb(0,0,0)
        c.stroke()

        c.set_font_size(h/4)
        c.set_source_rgb(0,0,0)
        c.move_to(x-w/2,y+h/8)
        c.show_text("Start")

class Cursor(object):
    def __init__(self): self.obj = None
    def set_obj(self, obj):
        self.obj = obj
    def lost(self):
        self.obj = None
    def handle(self, foo):
        if self.obj != None: self.obj.key(foo)

class TheTool(object):

    def __init__(self):
        print self
        self.canvas_position = {
            'x': 0.,
            'y': 0.,
            }

        self.old_zoom = 1.0
        self.zoom = 0.3
        self.grid_spacing = 1./(25.4/72)*50.  # 1 pixel = 1/72 inch, 5 cm = 

        self.mouse_pointer = {
            'x': 0.,
            'y': 0.,
            }
        self.drag_start_position = None
        self.drag_button = -1
        self.toolbox = False
        self.choicebox = None

        self.active_tool = None
        self.actions = []

        self.comps = []
        self.cursor = Cursor()

        self.is_quit = False

        self.action_node = 'root'
        self.action_tree = {
            'root': 'Screen Text Line Arrow Rectangle Circle Quit Page Export'.split(),
            'page': 'TitlePage ChangeLogPage'.split(),
            }
        self.load_data()
        if len(self.comps) == 0:
            self.comps.append(Start())

    def load_data(self):
        import sys, os
        if os.path.isfile(sys.argv[1]):
            f = open(sys.argv[1], 'r')
#            try:
            pyobs = json.load(f)

            import tool, pages
            for ob in pyobs:
                print ob['class']
                i = eval(ob['class']+'()')
                i.pos(ob['x'], ob['y'])
                i.size(ob['w'], ob['h'])
                for k in 'class x y w h'.split():
                    del ob[k]
                for key in ob.keys():
                    setattr(i, key, ob[key])
                self.comps.append(i)

                if hasattr(i, 'data'): print i.data
                
                
#            except:
            print 'error in load'

    def save_data(self):
        import sys
        f = open(sys.argv[1], 'rw')
        

    def get_actions(self):
        return self.action_tree[self.action_node]

    def add_component(self, comp):
        self.comps.append(comp)
        comp.pos( \
            (self.mouse_pointer['x'] - self._rect.width/2) / self.zoom \
            - self.canvas_position['x'],
            (self.mouse_pointer['y'] - self._rect.height/2) / self.zoom \
            - self.canvas_position['y'])

    def draw(self, c, rect):
        self._rect = rect
        self.actions = []
        
        c.set_source(BG)
        c.rectangle(rect)
        c.fill_preserve()
        #rect = self.get_allocation()

        c.translate(rect.width/2, rect.height/2)
        c.scale(self.zoom, self.zoom)
        c.translate(self.canvas_position['x'],
                    self.canvas_position['y'])


        def draw_grid(c, rect):
            (x0, y0) = c.device_to_user(0,0)
            (x1, y1) = c.device_to_user(rect.width, rect.height)
            for x in range (int(x0 - x0%self.grid_spacing),
                            int(x1 + x1%self.grid_spacing),
                            self.grid_spacing):
                c.move_to(x, y0)
                c.line_to(x, y1)
            for y in range (int(y0 - y0%self.grid_spacing),
                            int(y1 + y1%self.grid_spacing),
                            self.grid_spacing):
                c.move_to(x0, y)
                c.line_to(x1, y)

            c.set_source(GRID_FG)
            c.stroke()
        draw_grid(c, rect)


        x = rect.x + rect.width /2
        y = rect.x + rect.height /2
        radius = min(rect.width /2, rect.height /2) - 5

        #print 'canvas position', \
        mx, my = (self.mouse_pointer['x'] - self._rect.width/2 )/ self.zoom \
                 - self.canvas_position['x'], \
                 (self.mouse_pointer['y'] - self._rect.height/2 )/ self.zoom \
                 - self.canvas_position['y']
        for comp in self.comps:
            comp.draw(c, mx, my)

        def draw_toolbox(c, point):
            w, h = 42*3, 38*3
            c.identity_matrix()
            #print dir(c)
            x, y = self.mouse_pointer['x'], self.mouse_pointer['y']
            x, y = x-w/2, y-h/2
            c.translate(x, y)
            #c.translate(-50, -50)
            c.new_path()
            c.rectangle(0,0, w, h)
            c.set_source(TOOLBOX_BG)
            c.fill_preserve()
            c.close_path()
            c.stroke()

            idx = 0
            x_ = x

            for act in self.get_actions():
                a = eval('actions.'+act+'()')
                if hasattr(a, 'set_tool'): a.set_tool(self)
                def cb():
                    self.action_node = 'root'
                    self.toolbox = False
                    self.redraw()
                a.callback = cb
                self.actions.append(a)
                a.draw(c, x, y, (w-1)/3, (h-1)/3)
                
                x += w/3
                if idx%3 == 2:
                    y+= h/3
                    x = x_
                idx += 1
            
        if self.toolbox:
            draw_toolbox(c, self.mouse_pointer)


        # reorder the actions. topmost is first if event is coming.
        self.actions.reverse()

    def mouse_pressed(self, w, ev):
        self.drag_start_position = { 'x': ev.x, 'y': ev.y}
        self.drag_button = ev.button
        self.old_zoom = self.zoom
        print 'pressed', self.drag_button

    def mouse_released(self, w, ev):
        if self.drag_start_position != None:
            self.drag_start_position = None

        for action in self.actions:
            if action.is_hit(ev.x, ev.y):
                action.activate()
                #self.toolbox = False

        mx, my = (ev.x - self._rect.width/2 )/ self.zoom \
                 - self.canvas_position['x'], \
                 (ev.y - self._rect.height/2 )/ self.zoom \
                 - self.canvas_position['y']
        found = False
        for comp in self.comps:
            if comp.is_close(mx, my):
                comp.mouse_released(mx, my, self.cursor)
                found = True
        if not found:
            self.cursor.lost()

        print 'released'

    def pointer_motion(self, w, ev):
        #print 'pointer motion', ev.x, ev.y
        #print 'canvas position', \
        #      (ev.x - self._rect.width/2 )/ self.zoom - self.canvas_position['x'], \
        #      (ev.y - self._rect.height/2 )/ self.zoom - self.canvas_position['y']
        
        if not self.toolbox:
            self.mouse_pointer['x'] = ev.x
            self.mouse_pointer['y'] = ev.y
        if self.drag_start_position == None:
            self.redraw()
            return

        if self.drag_button == 1:
            self.canvas_position['x'] += \
               (ev.x - self.drag_start_position['x'])/self.zoom
            self.canvas_position['y'] += \
               (ev.y - self.drag_start_position['y'])/self.zoom
            self.drag_start_position = { 'x': ev.x, 'y': ev.y}
            self.redraw()
        elif self.drag_button == 3:
            self.zoom = self.old_zoom + (ev.y - self.drag_start_position['y']) / w.get_allocation().height
            self.zoom = max(0.05, self.zoom)
            print self.zoom
            self.redraw()

    def key_released(self, widget, ev):
        #for i in dir(ev): print i, eval('ev.'+i)
        print ev.keyval
        keyname = gtk.gdk.keyval_name(ev.keyval)
        print "Key %s (%d) was released" % (keyname, ev.keyval)
        if ev.keyval & gtk.gdk.MOD1_MASK or \
               gtk.gdk.keyval_name(ev.keyval).startswith('Control'):
            self.toolbox = False
            self.action_node = 'root'
            self.redraw()
            print 'alt release'
           
    def key_pressed(self, widget, ev):
        #for i in dir(ev): print i, eval('ev.'+i)
        print ev.keyval
        keyname = gtk.gdk.keyval_name(ev.keyval)
        print "Key %s (%d) was pressed" % (keyname, ev.keyval), self
        if gtk.gdk.keyval_name(ev.keyval).startswith('Control'):
            self.toolbox = True
            self.redraw()
            print 'alt pressed'

        if keyname == 'q':
            self.is_quit = True
            self.redraw()

        self.cursor.handle(keyname)
        self.redraw()
