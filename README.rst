===========================================
Deftity - a tool for interaction architects
===========================================

:author: Matti Katila

Deft is something smooth, artful and skillful (specially in hands).
Deft emphasizes lightness, neatness, and sureness of touch or handling
<a surgeon's deft manipulation of the scalpel> (src: merriam-webster).

Deftity is a tool for interaction architects to compose user
interfaces for computers. However, it's not a visual design tool.

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
simple to present. It should be simple to understand by those who
implement it. 


What are architects made of?
----------------------------

My take on architect is about communication. Architect is someone who
has technical skills but utilizes those by mouth or other
communication. That is, anyone can have technical talent but only
those who can communicate it out should became architects.

So, interaction architect should be able to design the interaction and
be able to communicate that design to developers. For this purpose
there is need for tools. Dia, for example, is useful general purpose
sketching visualizer. My take on deftity is to learn Cairo and try to
focus on things that are essentials for interaction design.


Some weird design ideas
-----------------------

Remove traditional save and load. File is saved when it is
changed. Hopefully there is plenty of room.

Write the content into png file and utilize some metainfo field to
describe the actual content of the design. ;))



