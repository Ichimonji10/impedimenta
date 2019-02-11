# coding=utf-8
"""Generate a desktop notification message."""
import gi
gi.require_version('Gtk', '3.0')  # pylint:disable=wrong-import-position
from gi.repository import Gtk

from notification_generator import dbus


def main() -> None:
    """Spawn a GUI application."""
    window = NotGenWindow()
    window.show_all()
    window.connect('destroy', Gtk.main_quit)
    Gtk.main()


class NotGenWindow(Gtk.Window):
    """A notification generator."""

    def __init__(self) -> None:
        super().__init__(title='Notification Generator')
        grid = Gtk.Grid()
        self.add(grid)

        self.summary_label = self.__gen_summary_label()
        self.summary_entry = self.__gen_summary_entry()
        self.body_label = self.__gen_body_label()
        self.body_frame = self.__gen_body_frame()
        self.send_button = self.__gen_send_button()

        for top, widget in enumerate((
                self.summary_label,
                self.summary_entry,
                self.body_label,
                self.body_frame,
                self.send_button)):
            grid.attach(widget, left=0, top=top, width=1, height=1)

    def on_send_button_clicked(self, _) -> None:
        """Send the user's input to the desktop notification service."""
        summary = self.summary_entry.get_text()

        scrolled_window = self.body_frame.get_children()[0]
        text_view = scrolled_window.get_children()[0]
        buffer_ = text_view.get_buffer()
        body = buffer_.get_text(
            buffer_.get_start_iter(),
            buffer_.get_end_iter(),
            False,
        )

        dbus.send(summary, body)

    @staticmethod
    def __gen_summary_label() -> Gtk.Label:
        return Gtk.Label(label='Summary')

    @staticmethod
    def __gen_summary_entry() -> Gtk.Entry:
        return Gtk.Entry()

    @staticmethod
    def __gen_body_label() -> Gtk.Label:
        return Gtk.Label(label='Body')

    @staticmethod
    def __gen_body_frame() -> Gtk.Frame:
        text_view = Gtk.TextView()
        text_view.props.wrap_mode = True

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.props.expand = True
        scrolled_window.add(text_view)

        frame = Gtk.Frame()
        frame.add(scrolled_window)

        return frame

    def __gen_send_button(self) -> Gtk.Button:
        send_button = Gtk.Button(label='Send')
        send_button.connect('clicked', self.on_send_button_clicked)
        return send_button
