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
    def load_data(self, comps): pass
    def is_close(self,x0,y0):
        x,y,w,h = self.xywh()
        return x < x0 < x+w and \
               y < y0 < y+h


class Arrow(Component):
    def __init__(self, links=None):
        self.data = {}
        self.links = links
    
    def save_data(self):
        ret = Component.save_data(self)
        a,b = self.links
        ax,ay,aw,ah = a.xywh()
        bx,by,bw,bh = b.xywh()
        ret['data'] = {
            'a': a.__class__.__module__ +'.'+ a.__class__.__name__,
            'b': b.__class__.__module__ +'.'+ b.__class__.__name__,
            'ax':ax, 'ay':ay, 'bx':bx, 'by':by,
            }
        return ret
    def load_data(self, comps):
        def find_comp(comps, clas, xx,yy):
            for c in comps:
                x,y,w,h = c.xywh()
                #print c, x, y, xx, yy
                if c.__class__.__module__ +'.'+ c.__class__.__name__ == clas \
                   and x == xx and y == yy:
                    return c
            raise 'No comp found '+ clas+ str(xx)+ str(yy)
        a = find_comp(comps, self.data['a'], self.data['ax'], self.data['ay'])
        b = find_comp(comps, self.data['b'], self.data['bx'], self.data['by'])
        self.links = (a,b)
        
    def pos(self, x,y): pass
    #def is_close(self, mx, my): pass
    def xywh(self):
        a, b = self.links
        ax,ay,aw,ah = a.xywh()
        bx,by,bw,bh = b.xywh()
        x = min(ax, bx)
        y = min(ay, by)
        #w = max(ax+aw, bx+bw)
        #h = max(ay+ah, by+bh)
        w = max(ax, bx)
        h = max(ay, by)
        w = w - x
        h = h - y
        return (x,y,w,h)
        
    def draw(self, c, tc, mx, my):
        a,b = self.links
        ax,ay,aw,ah = a.xywh()
        bx,by,bw,bh = b.xywh()
        lenght = 35
        degrees = 0.5

        if self in tc.selected_comps:
            c.set_source_rgb(1, 0, 0)
        else:
            c.set_source_rgb(0, 0, 0)
        #c.move_to(ax, ay)
        xx,yy = ax-bx, ay-by
        l = math.sqrt(xx**2 + yy**2)/2
        angle = math.atan2(by - ay, bx - ax) + math.pi;

        c.new_path()
        xx = bx + l * math.cos(angle + degrees);
        yy = by + l * math.sin(angle + degrees);
        c.curve_to(ax,ay, xx, yy, bx, by)
        c.set_line_width(0.92)

        x1 = bx + lenght * math.cos(angle )
        y1 = by + lenght * math.sin(angle )
        c.move_to(x1, y1)
        c.line_to(bx, by)
        x2 = bx + lenght * math.cos(angle + 2*degrees);
        y2 = by + lenght * math.sin(angle + 2*degrees);
        c.move_to(x2, y2)
        c.line_to(bx, by)

        c.stroke()
    def mouse_released(self, tc, x,y): pass


import actions
import util

#colors
BG = cairo.SolidPattern(1,1,1)
GRID_FG = cairo.SolidPattern(.8,.8,.8)
TOOLBOX_BG = cairo.SolidPattern(.4,.4,.5, .5)


class Start(Component):
    def draw(self, c, tc, mx,my):
        x,y,w,h = self.xywh()
        c.arc(x+w/2,y+h/2, w/2, 0, 2 * math.pi)
        if self.is_close(mx, my):
            c.set_source_rgb(1,.3,1)
            c.fill_preserve()
        c.set_source_rgb(0,0,0)
        c.stroke()

        c.set_font_size(h/4)
        c.set_source_rgb(0,0,0)
        c.move_to(x,y+h*3/5)
        c.show_text("Start")
    def mouse_released(self, tc, mx, my):
        if tc.arrow == ToolContext.ARROW_START:
            tc.set_arrow(self)

class ToolContext(object):
    ARROW_START = 1
    ARROW_END = 2
    ARROW_NONE = 3

    HLEFT = 1
    HCENTER = 2
    HRIGHT = 3
    VTOP = 4
    VCENTER = 5
    VBOTTOM = 6

    class Cursor(object):
        def __init__(self): self.obj = None
        def set_obj(self, obj, pos = -1):
            self.obj = obj
            self.pos = pos
            print pos
        def lost(self):
            self.obj = None
        def handle(self, foo):
            if self.obj != None: self.obj.key(foo)

    def __init__(self, tool):
        self.tool = tool
        self.cursor = ToolContext.Cursor()
        
        # Arrow tool selected?
        self.arrow = ToolContext.ARROW_NONE
        self.arrow_comps = []

        # Alt pressed?
        self.is_move_scale = False

        # Shift selection?
        self.is_selection = False
        self.is_selection_active = False
        self.selected_xywh = [0,0,0,0]
        self.selected_comps = []
        self.selection_mode = [None, None]
    def handle_selection(self):
        s = self.selected_xywh
        if s[2] < 0:
            s[2] = abs(s[2])
            s[0] -= s[2]
        if s[3] < 0:
            s[3] = abs(s[3])
            s[1] -= s[3]
        X,Y,XW,YH = s
        XW += s[0]
        YH += s[1]
        X,Y = self.tool.screen2canvas_pt(X,Y)
        XW, YH = self.tool.screen2canvas_pt(XW, YH)
        self.selected_comps = []
        for c in self.tool.comps:
            x,y,w,h = c.xywh()
            if X < x and Y < y and x+w < XW and y+h < YH:
                self.selected_comps.append(c)
        print self.selected_comps

    def start_arrow(self):
        self.arrow = ToolContext.ARROW_START
    def set_arrow(self, comp):
        if self.arrow == ToolContext.ARROW_START:
            self.arrow = ToolContext.ARROW_END
            self.arrow_comps.append(comp)
        elif self.arrow == ToolContext.ARROW_END:
            self.arrow = ToolContext.ARROW_NONE
            self.arrow_comps.append(comp)
            self.tool.add_component(Arrow(self.arrow_comps))
            self.arrow_comps = []
    def selection_pressed(self, xy):
        x,y,xx,yy = self._selection_xyxxyy()
        gap = 150*0.3/self.tool.zoom
        self.selection_mode = [None, None]
        self.is_selection_active = False
        if xx - x < gap*3 or yy - y < gap*3:
            x, y, xx, yy = x-gap, y-gap, xx+gap, yy+gap
        if x < xy[0] < xx and y < xy[1] < yy:
            if x < xy[0] < x+gap:
                self.selection_mode[0] = ToolContext.HLEFT
            elif x+gap < xy[0] < xx-gap:
                self.selection_mode[0] = ToolContext.HCENTER
            elif xx-gap < xy[0] < xx:
                self.selection_mode[0] = ToolContext.HRIGHT
            if y < xy[1] < y+gap:
                self.selection_mode[1] = ToolContext.VTOP
            elif y+gap < xy[1] < yy-gap:
                self.selection_mode[1] = ToolContext.VCENTER
            elif yy-gap < xy[1] < yy:
                self.selection_mode[1] = ToolContext.VBOTTOM
            self.is_selection_active = True
            self.selection_xy = xy

    def selection_move(self, xy):
        x,y = self.selection_xy
        X = xy[0] - x
        Y = xy[1] - y
        SX = X
        SY = Y
        if self.selection_mode in [
            [ToolContext.HLEFT, ToolContext.VBOTTOM],
            [ToolContext.HLEFT, ToolContext.VCENTER],
            [ToolContext.HCENTER, ToolContext.VCENTER],
            [ToolContext.HLEFT, ToolContext.VTOP],
            [ToolContext.HCENTER, ToolContext.VTOP],
            [ToolContext.HRIGHT, ToolContext.VTOP]]:
            if self.selection_mode == [ToolContext.HCENTER,
                                       ToolContext.VCENTER]:
                pass
            elif self.selection_mode[0] in [ToolContext.HCENTER,
                                            ToolContext.HRIGHT]:
                X = 0
            elif self.selection_mode[1] in [ToolContext.VCENTER,
                                            ToolContext.VBOTTOM]:
                Y = 0
        else:
            X = Y = 0
        if self.selection_mode != [ToolContext.HCENTER,
                                   ToolContext.VCENTER]:
            if self.selection_mode[0] == ToolContext.HCENTER:
                SX = 0
            elif self.selection_mode[1] == ToolContext.VCENTER:
                SY = 0
            if self.selection_mode[0] == ToolContext.HLEFT:
                print 'xsmall'
                SX *= -1
            if self.selection_mode[1] == ToolContext.VTOP:
                print 'ysmall'
                SY *= -1
        else:
            SX = SY = 0
                
        for c in self.selected_comps:
            x,y,w,h = c.xywh()
            c.pos(x+X, y+Y)
            if len(self.selected_comps) == 1:
                c.size(w+SX, h+SY)
            
        self.selection_xy = xy
        self.tool.redraw()
    def selection_released(self, xy):
        self.selection_mode = [None, None]
        self.is_selection_active = False
    def select_deleted(self):
        for c in self.selected_comps:
            for linked in filter(lambda x: isinstance(x, Arrow) and \
                                 (x.links[0] == c or x.links[1] == c),
                                 self.tool.comps):
                self.tool.comps.remove(linked)
                print 'del', linked
            self.tool.comps.remove(c)
            print 'del', c
        self.selected_comps = []
                
    def _selection_xyxxyy(self):
        x,y = math.pow(2, 30), math.pow(2, 30)
        xx,yy = -math.pow(2,30), -math.pow(2, 30)
        for comp in self.selected_comps:
            X,Y,W,H = comp.xywh()
            x = min(x, X)
            y = min(y, Y)
            xx = max(xx, X+W)
            yy = max(yy, Y+H)
        return (x, y, xx, yy)
    def draw_move_scale(self, c, mx, my):
        if len(self.selected_comps) == 0: return
        x,y,xx,yy = self._selection_xyxxyy()
        c.new_path()
        c.rectangle(x,y,xx-x,yy-y)
        c.set_source_rgb(1,0,0)
        c.close_path()

        gap = 150*0.3/self.tool.zoom
        if xx - x < gap*3 or yy - y < gap*3:
            c.new_path()
            c.rectangle(x-gap,y-gap,xx-x+2*gap,yy-y+2*gap)
            c.set_source_rgb(1,0,0)
            c.close_path()

            c.move_to(x-gap, y)
            c.line_to(xx+gap, y)
            c.move_to(x, y-gap)
            c.line_to(x, yy+gap)
            c.move_to(x-gap, yy)
            c.line_to(xx+gap, yy)
            c.move_to(xx, y-gap)
            c.line_to(xx, yy+gap)

        else:
            c.move_to(x, y+gap)
            c.line_to(xx, y+gap)
            c.move_to(x, yy-gap)
            c.line_to(xx, yy-gap)
            c.move_to(x+gap, y)
            c.line_to(x+gap, yy)
            c.move_to(xx-gap, y)
            c.line_to(xx-gap, yy)
        c.stroke()
            
    def draw(self, c):

        c.identity_matrix()
        if self.arrow == ToolContext.ARROW_START:
            util.write(c, 'Select arrow start component.', 40,40, 32)
        elif self.arrow == ToolContext.ARROW_END:
            util.write(c, 'Select arrow end component.', 40,40, 32)

        if self.is_selection:
            c.new_path()
            x,y,w,h = self.selected_xywh
            c.rectangle(x,y,w,h)
            c.set_source_rgb(1,0,0)
            c.close_path()
            c.stroke()


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

        self.tool_context = ToolContext(self)

        self.active_tool = None
        self.actions = []

        self.comps = []

        self.is_quit = False

        self.action_node = 'root'
        self.action_tree = {
            'root': 'Screen Text Draw Arrow  Quit Page Export'.split(),
            'page': 'TitlePage ChangeLogPage DescriptionPage EmptyPage'.split(),
            'screen': 'WVGAScreen'.split(),
            'draw': 'Image Line Rectangle Circle'.split()
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

            import tool, pages, text, image
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
                i.load_data(self.comps)

                #if hasattr(i, 'data'): print i.data
                
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

    def screen2canvas_pt(self,x,y):
        return (
            (x - self._rect.width/2) / self.zoom \
            - self.canvas_position['x'],
            (y - self._rect.height/2) / self.zoom \
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

        mx, my = self.screen2canvas_pt(self.mouse_pointer['x'], 
                                       self.mouse_pointer['y'])
        for comp in self.comps:
            comp.draw(c, self.tool_context, mx, my)

        self.tool_context.draw_move_scale(c, mx, my)

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

        self.tool_context.draw(c)

        # reorder the actions. topmost is first if event is coming.
        self.actions.reverse()

    def mouse_pressed(self, w, ev):
        self.drag_start_position = { 'x': ev.x, 'y': ev.y}
        self.drag_button = ev.button
        self.old_zoom = self.zoom
        print 'pressed', self.drag_button
        if len(self.tool_context.selected_comps) > 0:
            self.tool_context.selection_pressed(
                self.screen2canvas_pt(ev.x, ev.y))
        

    def mouse_released(self, w, ev):
        if self.drag_start_position != None:
            self.drag_start_position = None

        if self.tool_context.is_selection_active:
            self.tool_context.selection_released(
                self.screen2canvas_pt(ev.x, ev.y))
            self.redraw()
            return


        for action in self.actions:
            if action.is_hit(ev.x, ev.y):
                action.activate()
                #self.toolbox = False

        mx, my = self.screen2canvas_pt(ev.x, ev.y)
        found = False
        for comp in self.comps:
            if comp.is_close(mx, my):
                comp.mouse_released(self.tool_context, mx, my)
                found = True
        if not found:
            self.tool_context.cursor.lost()
        else:
            self.redraw()

        print 'released'

    def pointer_motion(self, w, ev):
        #print 'pointer motion', ev.x, ev.y
        #print 'canvas position', \
        #      (ev.x - self._rect.width/2 )/ self.zoom - self.canvas_position['x'], \
        #      (ev.y - self._rect.height/2 )/ self.zoom - self.canvas_position['y']
        if self.tool_context.is_selection_active:
            self.tool_context.selection_move(
                self.screen2canvas_pt(ev.x, ev.y))
            self.redraw()
            return
        
        if not self.toolbox:
            self.mouse_pointer['x'] = ev.x
            self.mouse_pointer['y'] = ev.y
            s = self.tool_context.selected_xywh
            s[2] = ev.x - s[0]
            s[3] = ev.y - s[1]
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
        if gtk.gdk.keyval_name(ev.keyval).startswith('Alt_'):
            self.tool_context.is_move_scale = False
            self.redraw()
        if gtk.gdk.keyval_name(ev.keyval).startswith('Shift_'):
            self.tool_context.is_selection = False
            self.tool_context.handle_selection()
            self.redraw()
           
    def key_pressed(self, widget, ev):
        #for i in dir(ev): print i, eval('ev.'+i)
        print ev.keyval
        keyname = gtk.gdk.keyval_name(ev.keyval)
        print "Key %s (%d) was pressed" % (keyname, ev.keyval), self
        if gtk.gdk.keyval_name(ev.keyval).startswith('Control'):
            self.toolbox = True
            self.redraw()
            print 'alt pressed'
        if gtk.gdk.keyval_name(ev.keyval).startswith('Alt_'):
            self.tool_context.is_move_scale = True
        if gtk.gdk.keyval_name(ev.keyval).startswith('Shift_'):
            s = self.tool_context.selected_xywh
            s[0] = s[2] = self.mouse_pointer['x']
            s[1] = s[3] = self.mouse_pointer['y']
            self.tool_context.is_selection = True

        if keyname == 'q':
            self.is_quit = True
            self.redraw()

        if self.tool_context.selected_comps != [] and keyname == 'Delete':
            print 'asdfadsf'
            self.tool_context.select_deleted()

        self.tool_context.cursor.handle(keyname)
        self.redraw()
