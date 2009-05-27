# (c): Matti J. Katila
#
# The Deft tool
#

import gtk
import math
import cairo
import actions


#colors
BG = cairo.SolidPattern(1,1,1)
GRID_FG = cairo.SolidPattern(.8,.8,.8)
TOOLBOX_BG = cairo.SolidPattern(.4,.4,.5, .5)


class TheTool(object):

    def __init__(self):
        self.canvas_position = {
            'x': 0.,
            'y': 0.,
            }

        self.old_zoom = 1.0
        self.zoom = 0.3
        self.grid_spacing = 50

        self.mouse_pointer = {
            'x': 0.,
            'y': 0.,
            }
        self.drag_start_position = None
        self.drag_button = -1
        self.toolbox = False

        self.active_tool = None
        self.actions = []

    def draw(self, c, rect):
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

        c.arc(x,y, radius, 0, 2 * math.pi)
        c.set_source_rgb(1,.3,1)
        c.fill_preserve()
        c.set_source_rgb(0,0,0)
        c.stroke()

        def draw_toolbox(c, point):
            w, h = 42*3, 38*3
            c.identity_matrix()
            #print dir(c)
            x, y = self.mouse_pointer['x'], self.mouse_pointer['y']
            x, y = x-w/2, y-h/2
            c.translate(x, y)
            #c.translate(-50, -50)
            c.rectangle(0,0, w, h)
            c.set_source(TOOLBOX_BG)
            c.fill_preserve()
            c.stroke()

            idx = 0
            x_ = x
            for act in 'Screen Text Line Arrow Non Rectangle Circle'.split():
                a = eval('actions.'+act+'()')
                def cb():
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

        # reorder the actions. topmost is first.
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
                self.toolbox = False
        print 'released'

    def pointer_motion(self, w, ev):
        #print 'pointer motion'
        if not self.toolbox:
            self.mouse_pointer['x'] = ev.x
            self.mouse_pointer['y'] = ev.y
        if self.drag_start_position == None:
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
            print self.zoom
            self.redraw()

    def key_released(self, widget, ev):
        #for i in dir(ev): print i, eval('ev.'+i)
        print ev.keyval
        keyname = gtk.gdk.keyval_name(ev.keyval)
        print "Key %s (%d) was pressed" % (keyname, ev.keyval)
        if ev.keyval & gtk.gdk.MOD1_MASK or \
               gtk.gdk.keyval_name(ev.keyval).startswith('Control'):
            self.toolbox = False
            self.redraw()
            print 'alt release'
           
    def key_pressed(self, widget, ev):
        #for i in dir(ev): print i, eval('ev.'+i)
        print ev.keyval
        keyname = gtk.gdk.keyval_name(ev.keyval)
        print "Key %s (%d) was pressed" % (keyname, ev.keyval)
        if ev.keyval & gtk.gdk.MOD1_MASK or \
               gtk.gdk.keyval_name(ev.keyval).startswith('Control'):
            self.toolbox = True
            self.redraw()
            print 'alt pressed'

