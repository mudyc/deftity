# (c): 2008, Matti J. Katila
#
# A bootstrap and main loop of Deft tool
#
# implements reloading capabilities by using
# EventBox as delegator.
#


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
