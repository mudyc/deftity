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



"""A bootstrap and main loop of Deft tool

implements reloading capabilities by using
EventBox as delegator.
"""


import sys
import pygtk
pygtk.require('2.0')
import gtk, reloader

WINDOW = 'placeholder'
CONNS = []
RELOADER = 'placeholder'

def check_reload(widget, event):
    if event != widget:
        print event, event.type, event.string, event.keyval, event.hardware_keycode, event.state
    if event == WINDOW or \
           (event.state & gtk.gdk.CONTROL_MASK \
            and event.keyval == ord('r')):


        for c in WINDOW.get_children():
            for conn in CONNS:
                WINDOW.disconnect(conn)
            c.destroy()
            WINDOW.remove(c)

        RELOADER.reinit()

        import delegate
        if not False:
            WINDOW.add(delegate.Delegate())

        # Bug in pygtk. When new object is inserted into window all
        # keys stop working.
        if event != WINDOW:
            t = WINDOW.get_children()[0].the_tool
            #CONNS.append(WINDOW.connect('key_release_event', t.key_released))
            #CONNS.append(WINDOW.connect('key_press_event', t.key_pressed))
        WINDOW.show_all()

        def fix(type_):
            ev=gtk.gdk.Event(gtk.gdk.KEY_PRESS)
            ev.window = WINDOW.window
            import time
            ev.time = long(time.time())
            ev.state = 65363
            ev.keyval = 114
            gtk.main_do_event(ev)
        fix(gtk.gdk.KEY_PRESS)
        fix(gtk.gdk.KEY_RELEASE)

        print 'reloaded...',WINDOW.get_children()[0]#, WINDOW.get_children()[0].the_tool
    return False

if __name__ == '__main__':

    if len(sys.argv[1:]) != 1:
        print "Deftity needs one parameter which is the file name.\n\n", \
              "For example: 'python deftity.py my_design'\n"

        sys.exit(1)
    

    WINDOW = gtk.Window()
    WINDOW.resize(640, 480)
    WINDOW.connect('destroy', gtk.main_quit)
    WINDOW.connect('key_release_event', check_reload)

    WINDOW.add_events(
            gtk.gdk.EXPOSURE_MASK
            | gtk.gdk.BUTTON_PRESS_MASK
            | gtk.gdk.BUTTON_RELEASE_MASK
            | gtk.gdk.POINTER_MOTION_MASK
            | gtk.gdk.KEY_PRESS_MASK
            | gtk.gdk.KEY_RELEASE_MASK
            )
    WINDOW.set_flags(gtk.CAN_FOCUS)
    
    # A hack - reloader makes key_pressed useless...
    #def hack(widget, event):
    #    print 'hack..'
    #    WINDOW.get_children()[0].event(event)
    #WINDOW.connect('key_press_event', hack)

    RELOADER = reloader.RollbackImporter()

    check_reload(WINDOW, WINDOW)
    #import delegate
    #WINDOW.add(delegate.Delegate())
    #WINDOW.show_all()
    
    gtk.main()
