# deftity - a tool for interaction architect
#
# Copyright (C) 2011 Matti Katila
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


# Written by Matti J. Katila, 2011



def write(cr, s, x, y, size):
    cr.set_font_size(size)
    cr.set_source_rgb(0,0,0)
    cr.move_to(x,y)
    cr.show_text(s)
    return

    fascent, fdescent, fheight, fxadvance, fyadvance = cr.font_extents()
    for cx, letter in enumerate(s):
        xbearing, ybearing, width, height, xadvance, yadvance = (
                cr.text_extents(letter))
        cr.move_to(x,# + cx + 0.5 - xbearing - width / 2,
                y) # + 0.5 - fdescent + fheight / 2)
        cr.show_text(s)

def write_center(cr, s, x, w, y, size):
    cr.set_font_size(size)
    x_bear, y_bear, width, height, x_adv, y_adv = cr.text_extents(s)
    write(cr, s, x + (w-width)/2, y, size)



