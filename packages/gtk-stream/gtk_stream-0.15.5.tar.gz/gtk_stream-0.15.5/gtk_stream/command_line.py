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

import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='gtk-stream',
        description='A stream-based GUI tool',
        add_help=False
    )
    parser.add_argument('--list-icons', action='store_true')
    parser.add_argument('--hook')
    parser.add_argument('-h', '--help', action='store_true')
    args = parser.parse_args()

    if args.help:
        parser.print_help()

    elif args.list_icons:
        from . import Gtk, Gdk
        theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        for name in theme.get_icon_names():
            print(name)

    elif args.hook:
        match args.hook:
            case "bash":
                print('''
coproc GTK_STREAM { exec gtk-stream; }
trap 'kill -INT "$GTK_STREAM_PID"; wait "$GTK_STREAM_PID"' EXIT
exec {GTK_STREAM_EVENTS}<&"${GTK_STREAM[0]}"
exec {GTK_STREAM_MESSAGES}>&"${GTK_STREAM[1]}"
function GTK.send() {
    if (($# > 0)); then
        printf "$@" >&"$GTK_STREAM_MESSAGES"
    else
        cat >&"$GTK_STREAM_MESSAGES"
    fi
}
function GTK.receive() {
    read -u "$GTK_STREAM_EVENTS" "$@"
}
''')
    else:
        import io
        import sys
        import os
        import threading
        import xml.sax as sax
        
        from .parser import GtkStreamXMLHandler
        from .application import GtkStreamApp
        from .common import Logger, LogLevel

        class GtkStreamErrorHandler(sax.handler.ErrorHandler):
            def error(self, exc):
                raise exc
            def fatalError(self, exc):
                raise exc

        logLevel = LogLevel.__dict__.get(os.environ.get('GTK_STREAM_LOGLEVEL', 'WARN'), LogLevel.WARN)
        
        logger = Logger(logLevel)
        
        app = GtkStreamApp(logger)

        def parser_main():
            handler = GtkStreamXMLHandler(app)
            errHandler = GtkStreamErrorHandler()
            parser = sax.make_parser()
            parser.setContentHandler(handler)
            parser.setErrorHandler(errHandler)
            try:
                parser.parse(io.FileIO(0, 'r', closefd=False))
            except Exception as e:
                logger.error("Done with exception : %s", e)
            handler.quit_application()

        parser_thread = threading.Thread(target = parser_main, daemon = True)
        parser_thread.start()

        app.wait_for_init()
        app.run()
