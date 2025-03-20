# Gtk-Stream : A stream-based GUI protocol
# Copyright (C) 2024  Marc Coiffier
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from ... import Gtk
from .. import Document, PseudoDocument

class StackSidebar(Document):
    __g_class__ = Gtk.StackSidebar
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.StackSidebar()

class StackPage(PseudoDocument):
    def __init__(self, app, title):
        super().__init__(app)
        self.title = title
    def set_page_props(self, page):
        page.set_title(self.title)
    
class Stack(Document):
    __g_class__ = Gtk.Stack
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.Stack()
    def insert_child(self, w, d):
        child = d.render_in(w)
        w.add_child(child)
        if isinstance(d, StackPage):
            page = w.get_page(child)
            d.set_page_props(page)
