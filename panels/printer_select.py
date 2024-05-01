import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from ks_includes.screen_panel import ScreenPanel
from ks_includes.widgets.autogrid import AutoGrid
from ks_includes.KlippyGtk import find_widget


class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        printers = self._config.get_printers()

        printer_buttons = []
        for i, printer in enumerate(printers):
            name = list(printer)[0]
            scale = 3
            self.labels[name] = self._gtk.Button("printer", name, f"color{1 + i % 4}", scale=scale)
            scale *= self._gtk.img_scale
            pixbuf = self._gtk.PixbufFromIcon(f"../../printers/{name}", scale, scale)
            if pixbuf is not None:
                image = find_widget(self.labels[name], Gtk.Image)
                image.set_from_pixbuf(pixbuf)
            self.labels[name].connect("clicked", self.connect_printer, name)
            printer_buttons.append(self.labels[name])
        grid = AutoGrid(printer_buttons, vertical=self._screen.vertical_mode)

        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(grid)
        self.content.add(scroll)

    def connect_printer(self, widget, name):
        self._screen.connect_printer(name)

    def activate(self):
        self._screen.base_panel.action_bar.hide()
        #GLib.timeout_add(100, self._screen.base_panel.action_bar.hide) # Changes
        GLib.timeout_add(0, self._screen.base_panel.action_bar.hide) # Changes
        if self._screen._ws:
            self._screen.close_websocket()
