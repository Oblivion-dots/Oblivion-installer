#!/usr/bin/env python3

import gi, os, subprocess
from datetime import datetime
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

CHOICES_SH_PATH = os.path.expanduser("~/Oblivian-Installer/gui/choices.sh")  # update this path


class Installer(Gtk.Window):
    def __init__(self):
        super().__init__(title="Oblivion Installer")
        self.set_default_size(720, 540)
        self.set_border_width(12)

        # Typewriter title
        self.title_label = Gtk.Label()
        self.title_index = 0
        self.title_full_text = "Welcome to Oblivion dot-files"
        self.cursor_visible = True

        # Checkbox options
        self.options = {"hyprland": True, "quickshell": True, "matugen": True, "guifetch": True}
        self.aur_helper = "yay"

        # Main vertical box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(main_box)

        # Typewriter title
        self.title_label.set_markup("")
        main_box.pack_start(self.title_label, False, False, 0)
        GLib.timeout_add(100, self.typewriter_tick)

        # Notebook tabs
        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        main_box.pack_start(self.notebook, True, True, 0)

        # Installer Tab
        self.install_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.install_box.set_border_width(12)
        self.install_box.set_name("panel")
        self.notebook.append_page(self.install_box, Gtk.Label(label="Installer"))

        options_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.install_box.pack_start(options_hbox, False, False, 12)

        # Left VBox: dependency checkboxes
        left_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        options_hbox.pack_start(left_vbox, True, True, 0)
        self.checkbuttons = {}
        for option in ["hyprland", "quickshell", "matugen", "guifetch"]:
            cb = Gtk.CheckButton(label=option.replace("_", " ").title())
            cb.set_active(True)
            cb.connect("toggled", self.on_checkbox_toggled, option)
            left_vbox.pack_start(cb, False, False, 0)
            self.checkbuttons[option] = cb

        # Right VBox: AUR dropdown
        right_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        options_hbox.pack_start(right_vbox, True, True, 0)
        aur_label = Gtk.Label(label="Select AUR Helper:")
        aur_label.set_xalign(0)
        right_vbox.pack_start(aur_label, False, False, 0)
        self.aur_combo = Gtk.ComboBoxText()
        for aur in ["yay", "paru"]:
            self.aur_combo.append_text(aur)
        self.aur_combo.set_active(0)
        self.aur_combo.connect("changed", self.on_aur_changed)
        right_vbox.pack_start(self.aur_combo, False, False, 0)

        # Progress label and bar
        self.progress_label = Gtk.Label()
        self.install_box.pack_start(self.progress_label, False, False, 6)
        self.progress_bar = Gtk.ProgressBar()
        self.install_box.pack_start(self.progress_bar, False, False, 6)

        # Install button
        self.install_button = Gtk.Button(label="Install Dotfiles")
        self.install_button.connect("clicked", self.on_install_clicked)
        self.install_box.pack_start(self.install_button, False, False, 6)

        # Logs tab
        log_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        log_box.set_border_width(12)
        log_box.set_name("panel")
        self.notebook.append_page(log_box, Gtk.Label(label="Logs"))

        top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        log_box.pack_start(top_box, False, False, 0)
        spacer = Gtk.Label()
        top_box.pack_start(spacer, True, True, 0)
        copy_icon = Gtk.Image.new_from_icon_name("edit-copy", Gtk.IconSize.MENU)
        copy_button = Gtk.Button()
        copy_button.set_image(copy_icon)
        copy_button.set_tooltip_text("Copy Logs")
        copy_button.set_relief(Gtk.ReliefStyle.NONE)
        copy_button.connect("clicked", self.copy_logs)
        top_box.pack_start(copy_button, False, False, 0)

        self.log_textview = Gtk.TextView()
        self.log_textview.set_editable(False)
        self.log_textview.set_monospace(True)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.add(self.log_textview)
        log_box.pack_start(scrolled, True, True, 0)

        # Apply CSS
        self.apply_css_light_modern()

    # Typewriter
    def typewriter_tick(self):
        if self.title_index < len(self.title_full_text):
            current_text = self.title_full_text[:self.title_index + 1]
            cursor = "_" if self.cursor_visible else " "
            self.title_label.set_markup(f'<big><b><span foreground="#000000">{current_text}{cursor}</span></b></big>')
            self.title_index += 1
        else:
            self.title_label.set_markup(f'<big><b><span foreground="#000000">{self.title_full_text}_</span></b></big>')
        self.cursor_visible = not self.cursor_visible
        return True

    # Logs
    def write_log(self, text):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        buf = self.log_textview.get_buffer()
        buf.insert(buf.get_end_iter(), f"[{timestamp}] {text}\n")
        mark = buf.create_mark(None, buf.get_end_iter(), True)
        self.log_textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

    def copy_logs(self, button):
        buf = self.log_textview.get_buffer()
        start, end = buf.get_bounds()
        text = buf.get_text(start, end, True)
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(text, -1)
        self.write_log("Logs copied to clipboard!")

    # Checkbox toggle
    def on_checkbox_toggled(self, widget, option):
        self.options[option] = widget.get_active()
        self.write_log(f"{option.replace('_',' ').title()} set to {self.options[option]}")

    def on_aur_changed(self, widget):
        self.aur_helper = widget.get_active_text()
        self.write_log(f"AUR Helper set to {self.aur_helper}")

    # Install logic
    def on_install_clicked(self, button):
        self.install_button.set_sensitive(False)
        for cb in self.checkbuttons.values():
            cb.set_sensitive(False)
        self.progress_label.set_text("Running installation...")
        self.progress_bar.pulse()
        GLib.timeout_add(100, self.pulse_progress)
        GLib.idle_add(self.run_choices_sh)

    def pulse_progress(self):
        self.progress_bar.pulse()
        return True

    def run_choices_sh(self):
        args = [CHOICES_SH_PATH]
        for dep, enabled in self.options.items():
            if enabled:
                args.append(dep)
        args.append(f"--aur={self.aur_helper}")
        self.write_log(f"Executing: {' '.join(args)}")

        try:
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                GLib.idle_add(self.write_log, line.strip())
            process.wait()
            if process.returncode == 0:
                self.progress_bar.set_fraction(1.0)
                self.progress_label.set_text("DONE")
                self.write_log("Installation complete!")
            else:
                self.progress_label.set_text("FAILED")
                self.write_log(f"choices.sh exited with code {process.returncode}")
        except Exception as e:
            self.progress_label.set_text("FAILED")
            self.write_log(f"Error running choices.sh: {e}")

        self.install_button.set_sensitive(True)
        for cb in self.checkbuttons.values():
            cb.set_sensitive(True)

    def apply_css_light_modern(self):
        css = b"""
        window { background-color: #ffffff; }
        #panel { background-color: #f9f9f9; border-radius: 10px; padding: 12px; }
        textview { background-color: #ffffff; color: #000000; border-radius: 6px; padding: 6px; }
        button { background-color: #e8e8e8; color: #000000; border-radius: 6px; padding: 6px 12px; }
        button:hover { background-color: #d8d8d8; }
        checkbutton { padding: 4px; color: #000000; }
        progressbar { background-color: #e0e0e0; color: #007ACC; border-radius: 6px; min-height: 18px; }
        notebook tab { background-color: #ffffff; color: #000000; padding: 6px 12px; border-radius: 6px; }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


if __name__ == "__main__":
    win = Installer()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()