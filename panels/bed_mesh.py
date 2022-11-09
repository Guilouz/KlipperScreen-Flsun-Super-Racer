import gi
import logging
import contextlib

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.screen_panel import ScreenPanel
from ks_includes.widgets.bedmap import BedMap


def create_panel(*args):
    return BedMeshPanel(*args)


class BedMeshPanel(ScreenPanel):

    def __init__(self, screen, title, back=True):
        super().__init__(screen, title, back)
        self.clear = None
        self.profiles = {}
        self.show_create = False
        self.active_mesh = None

    def initialize(self, panel_name):

        addprofile = self._gtk.ButtonImage("increase", " " + _("Add profile"), "color1", .66, Gtk.PositionType.LEFT, 1)
        addprofile.connect("clicked", self.show_create_profile)
        addprofile.set_hexpand(True)
        self.clear = self._gtk.ButtonImage("cancel", " " + _("Clear"), "color2", .66, Gtk.PositionType.LEFT, 1)
        self.clear.connect("clicked", self.send_clear_mesh)
        self.clear.set_hexpand(True)
        script = {"script": "BED_LEVELING"} # Changes
        calibrate = self._gtk.ButtonImage("refresh", " " + _("Bed Level"), "color3", .66, Gtk.PositionType.LEFT, 1) # Changes
        calibrate.connect("clicked", self._screen._confirm_send_action,
                                          _("Please plug in leveling switch before auto-leveling."),
                                          "printer.gcode.script", script) # Changes
        calibrate.set_hexpand(True)

        topbar = Gtk.Box(spacing=5)
        topbar.set_hexpand(True)
        topbar.set_vexpand(False)
        topbar.add(addprofile)
        topbar.add(self.clear)
        topbar.add(calibrate)

        # Create a grid for all profiles
        self.labels['profiles'] = Gtk.Grid()
        self.labels['profiles'].get_style_context().add_class("frame-item")
        self.labels['profiles'].set_valign(Gtk.Align.CENTER)

        scroll = self._gtk.ScrolledWindow()
        scroll.add(self.labels['profiles'])
        scroll.set_vexpand(True)

        self.load_meshes()

        grid = self._gtk.HomogeneousGrid()
        grid.set_row_homogeneous(False)
        grid.attach(topbar, 0, 0, 2, 1)
        self.labels['map'] = BedMap(self._gtk.get_font_size(), self.active_mesh)
        grid.attach(self.labels['map'], 0, 2, 1, 1)
        grid.attach(scroll, 1, 2, 1, 1)
        self.labels['main_grid'] = grid
        self.content.add(self.labels['main_grid'])

    def activate(self):
        self.load_meshes()
        with contextlib.suppress(KeyError):
            self.activate_mesh(self._screen.printer.get_stat("bed_mesh", "profile_name"))

    def activate_mesh(self, profile):
        if self.active_mesh is not None:
            self.profiles[self.active_mesh]['name'].set_sensitive(True)
            self.profiles[self.active_mesh]['name'].get_style_context().remove_class("button_active")
        if profile == "":
            logging.info("Clearing active profile")
            self.active_mesh = None
            self.update_graph()
            self.clear.set_sensitive(False)
            return
        if profile not in self.profiles:
            self.add_profile(profile)

        logging.info(f"Active {self.active_mesh} changing to {profile}")
        self.profiles[profile]['name'].set_sensitive(False)
        self.profiles[profile]['name'].get_style_context().add_class("button_active")
        self.active_mesh = profile
        self.update_graph(profile=profile)
        self.clear.set_sensitive(True)

    def retrieve_bm(self, profile):
        if profile is None:
            return None
        if profile == self.active_mesh:
            bm = self._printer.get_stat("bed_mesh")
            if bm is None:
                logging.info(f"Unable to load active mesh: {profile}")
                return None
            matrix = 'probed_matrix'
        else:
            bm = self._printer.get_config_section(f"bed_mesh {profile}")
            if bm is False:
                logging.info(f"Unable to load profile: {profile}")
                self.remove_profile(profile)
                return None
            matrix = 'points'
        return bm[matrix]

    def update_graph(self, widget=None, profile=None):
        self.labels['map'].update_bm(self.retrieve_bm(profile))
        self.labels['map'].queue_draw()

    def add_profile(self, profile):
        logging.debug(f"Adding Profile: {profile}")
        name = self._gtk.Button(f"<big><b>{profile}</b></big>")
        name.get_children()[0].set_use_markup(True)
        name.get_children()[0].set_line_wrap(True)
        name.get_children()[0].set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        name.set_vexpand(False)
        name.set_halign(Gtk.Align.START)
        name.connect("clicked", self.send_load_mesh, profile)
        name.connect("clicked", self.update_graph, profile)

        buttons = {
            "save": self._gtk.ButtonImage("complete", None, "color4", .75),
            "delete": self._gtk.ButtonImage("cancel", None, "color2", .75),
        }
        buttons["save"].connect("clicked", self.send_save_mesh, profile)
        buttons["delete"].connect("clicked", self.send_remove_mesh, profile)

        for b in buttons.values():
            b.set_hexpand(False)
            b.set_vexpand(False)
            b.set_halign(Gtk.Align.END)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        if profile != "default":
            button_box.add(buttons["save"])
        button_box.add(buttons["delete"])
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box.pack_start(name, True, True, 0)
        box.pack_start(button_box, False, False, 0)

        frame = Gtk.Frame()
        frame.get_style_context().add_class("frame-item")
        frame.add(box)

        self.profiles[profile] = {
            "name": name,
            "button_box": button_box,
            "row": frame,
            "save": buttons["save"],
            "delete": buttons["delete"],
        }

        pl = list(self.profiles)
        if "default" in pl:
            pl.remove('default')
        profiles = sorted(pl)
        pos = profiles.index(profile) + 1 if profile != "default" else 0

        self.labels['profiles'].insert_row(pos)
        self.labels['profiles'].attach(self.profiles[profile]['row'], 0, pos, 1, 1)
        self.labels['profiles'].show_all()

    def back(self):
        if self.show_create is True:
            self.remove_create()
            return True
        return False

    def load_meshes(self):
        bm_profiles = self._printer.get_stat("bed_mesh", "profiles")
        logging.info(f"Bed profiles: {bm_profiles}")
        for prof in bm_profiles:
            if prof not in self.profiles:
                self.add_profile(prof)
        for prof in self.profiles:
            if prof not in bm_profiles:
                self.remove_profile(prof)

    def process_update(self, action, data):
        if action == "notify_status_update":
            with contextlib.suppress(KeyError):
                logging.info(data['bed_mesh'])
                self.activate_mesh(data['bed_mesh']['profile_name'])

    def remove_create(self):
        if self.show_create is False:
            return

        self._screen.remove_keyboard()
        for child in self.content.get_children():
            self.content.remove(child)

        self.show_create = False
        self.content.add(self.labels['main_grid'])
        self.content.show()

    def remove_profile(self, profile):
        if profile not in self.profiles:
            return

        pl = list(self.profiles)
        if "default" in pl:
            pl.remove('default')
        profiles = sorted(pl)
        pos = profiles.index(profile) + 1 if profile != "default" else 0
        self.labels['profiles'].remove_row(pos)
        del self.profiles[profile]
        if not self.profiles:
            self.active_mesh = None
            self.update_graph()
            self.clear.set_sensitive(False)

    def show_create_profile(self, widget):

        for child in self.content.get_children():
            self.content.remove(child)

        if "create_profile" not in self.labels:
            pl = self._gtk.Label(_("Profile Name:"))
            pl.set_hexpand(False)
            self.labels['profile_name'] = Gtk.Entry()
            self.labels['profile_name'].set_text('')
            self.labels['profile_name'].set_hexpand(True)
            self.labels['profile_name'].connect("activate", self.create_profile)
            self.labels['profile_name'].connect("focus-in-event", self._show_keyboard)
            self.labels['profile_name'].grab_focus_without_selecting()

            save = self._gtk.ButtonImage("complete", _("Save"), "color3")
            save.set_hexpand(False)
            save.connect("clicked", self.create_profile)

            box = Gtk.Box()
            box.pack_start(self.labels['profile_name'], True, True, 5)
            box.pack_start(save, False, False, 5)

            self.labels['create_profile'] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            self.labels['create_profile'].set_valign(Gtk.Align.CENTER)
            self.labels['create_profile'].set_hexpand(True)
            self.labels['create_profile'].set_vexpand(True)
            self.labels['create_profile'].pack_start(pl, True, True, 5)
            self.labels['create_profile'].pack_start(box, True, True, 5)

        self.content.add(self.labels['create_profile'])
        self._show_keyboard()
        self.show_create = True

    def _show_keyboard(self, widget=None, event=None):
        self._screen.show_keyboard(entry=self.labels['profile_name'])

    @staticmethod
    def _close_dialog(widget, response):
        widget.destroy()

    def create_profile(self, widget):
        name = self.labels['profile_name'].get_text()
        if self.active_mesh is None:
            self.calibrate_mesh(None)

        self._screen._ws.klippy.gcode_script(f"BED_MESH_PROFILE SAVE={name}")
        self.remove_create()

    def calibrate_mesh(self, widget):
        self._screen.show_popup_message(_("Calibrating"), level=1)
        if self._screen.printer.get_stat("toolhead", "homed_axes") != "xyz":
            self._screen._ws.klippy.gcode_script(KlippyGcodes.HOME)

        self._screen._ws.klippy.gcode_script("BED_MESH_CALIBRATE")

        # Load zcalibrate to do a manual mesh
        if not (self._printer.config_section_exists("probe") or self._printer.config_section_exists("bltouch")):
            self.menu_item_clicked(widget, "refresh", {"name": _("Mesh calibrate"), "panel": "zcalibrate"})

    def send_clear_mesh(self, widget):
        self._screen._ws.klippy.gcode_script("BED_MESH_CLEAR")

    def send_load_mesh(self, widget, profile):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.bed_mesh_load(profile))

    def send_save_mesh(self, widget, profile):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.bed_mesh_save(profile))

    def send_remove_mesh(self, widget, profile):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.bed_mesh_remove(profile))
        self.remove_profile(profile)
