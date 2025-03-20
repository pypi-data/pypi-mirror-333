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

from ...properties import parse_property, get_prop_type
from ...common import print_event

class Document:
    __g_class__ = None
    def __init__(self, app, id = None, **attrs):
        self.id = id
        self.app = app
        self.props = {
            attr: parse_property(get_prop_type(self.__g_class__, attr), val)
            for (attr, val) in attrs.items()
        }
        self.children = []

    def connect_event(self, w, event, name, **print_event_kwargs):
        w.connect(event, print_event(self.app.logger, name, self.id, **print_event_kwargs))
    def add_child(self, child):
        self.children.append(child)
        
    def render_raw(self):
        """Method to render the document to a widet"""
        raise Exception("Method 'render' not implemented")
    def set_properties(self, w):
        self.app.name_widget(self.id, w)
        for (p,v) in self.props.items():
            val = v(self.app)
            self.app.logger.debug("Setting property '%s' to '%s' in widget %s", p, val, self.__class__)
            w.set_property(p, val)
        if self.id:
            w.set_property("name", self.id)
        w.insert_child = lambda d: self.insert_child(w, d)
    def render(self):
        w = self.render_raw()
        self.set_properties(w)
        for child in self.children:
            self.insert_child(w, child)
        return w
    def render_in(self, w):
        ret = self.render()
        ret.remove_self = lambda: w.remove(ret)
        return ret
    
    def insert_child(self, w, child):
        raise Exception("Unimplemented method 'insert_child'")

class PseudoDocument(Document):
    def __init__(self, app):
        super().__init__(app)
        self.child = None
    def add_child(self, child):
        self.child = child
    def render(self):
        return self.child.render()
