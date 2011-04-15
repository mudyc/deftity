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



"""A bootstrap and main loop of Deft tool

implements reloading capabilities by using
EventBox as delegator.
"""


import sys
import pygtk
pygtk.require('2.0')
import gtk, reloader

WINDOW = 'placeholder'
RELOADER = 'placeholder'

def check_reload(widget, event):
    #print event, event.type, event.string, event.keyval, event.hardware_keycode, event.state
    if event.state & gtk.gdk.CONTROL_MASK \
           and event.keyval == ord('r'):

        for c in WINDOW.get_children():
            WINDOW.remove(c)

        RELOADER.reinit()

        import delegate
        WINDOW.add(delegate.Delegate())
        WINDOW.show_all()

        print 'reloaded...'
        return False
    else:
        # hack - key release is omitted if not delegated.
        # delegate the event further..
        WINDOW.get_children()[0].event(event)


if __name__ == '__main__':

    if len(sys.argv[1:]) != 1:
        print "Deftity needs one parameter which is the file name.\n\n", \
              "For example: 'python deftity.py my_design.dat'\n"

        sys.exit(1)
    

    WINDOW = gtk.Window()
    WINDOW.resize(640, 480)
    WINDOW.connect('destroy', gtk.main_quit)
    WINDOW.connect('key_release_event', check_reload)

    # A hack - reloader makes key_pressed useless...
    def hack(widget, event):
        WINDOW.get_children()[0].event(event)
    WINDOW.connect('key_press_event', hack)

    RELOADER = reloader.RollbackImporter()

    import delegate
    WINDOW.add(delegate.Delegate())

    WINDOW.show_all()
    
    gtk.main()
