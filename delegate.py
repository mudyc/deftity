# (c): Matti J. Katila
#
# Implements cairo context and maps events to,
# well, methods...

import gtk, tool


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
        
        self.draw(self.context)
        
        return False

    def draw(self, c):
        a = self.get_allocation()
        self.the_tool.draw(c, a) #(0,0,a.width, a.height))

    def printer(self, widget, ev):
        #self.the_tool.
        print type(ev)
        #for k in dir(ev):
        #    print k, eval("ev."+k)

