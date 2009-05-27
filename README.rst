===========================================
Deftity - a tool for interaction architects
===========================================

:author: Matti Katila

Deft is something smooth, artful and skillful (specially in hands).
Deft emphasizes lightness, neatness, and sureness of touch or handling
<a surgeon's deft manipulation of the scalpel> (src: merriam-webster).

Deftity is a tool for interaction architects to compose user
interfaces for computers. However, this is not a visual design tool.

Interaction is something that happens between user and the device.
For instance user's eyes are input port for device's screen which is
output, and user's hands may be source for input events. However,
there may be other events as well, such as time or incoming call. More
event sources the more complicated design.

Except event handling interaction architect is also about design of
change. It's the responsibility of interaction architect to design 
the change to outputs when event has come, e.g. play a ringtone.

::

        t0           t1
   -----+------------+--------->
        |<- change ->|
        |            '- Output changes
        |         
        '- Input event


In this trivial example it's rather simple to say that ringtone shall
be played and stopped when line closes. However, it's not. How about
ringtone + silent mode? Or ringtone + watching video? Or ringtone when
music player is playing? Someone has to think of these cases. Someone
has to make decisions. Someone has to think the best scenario for the
user. Someone has to think what would be consistent for the
system. It's not rocket sciense nor brain surgery but it should be
simple present.

