# coding=utf-8
"""Generate a desktop notification message."""
import sys

from PyQt5 import QtWidgets

from notification_generator import dbus


def main() -> None:
    """Spawn a GUI application."""
    app = QtWidgets.QApplication(sys.argv)
    widget = SenderWidget()
    widget.show()
    app.exec_()


class SenderWidget(QtWidgets.QWidget):  # pylint:disable=too-few-public-methods
    """A widget for sending notification messages."""

    def __init__(self) -> None:
        """Initialize this object."""
        super().__init__()
        self.summary = QtWidgets.QLineEdit()
        self.body = QtWidgets.QPlainTextEdit()

        self.setWindowTitle('Notification Generator')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel('Summary:'))
        layout.addWidget(self.summary)
        layout.addWidget(QtWidgets.QLabel('Body:'))
        layout.addWidget(self.body)
        layout.addWidget(self.__gen_submit_button())
        self.setLayout(layout)

    def __gen_submit_button(self):
        """Generate a "submit" button for this widget."""
        button = QtWidgets.QPushButton('Ship it!')
        button.clicked.connect(self.send_notification)
        return button

    def send_notification(self) -> None:
        """Send a notification message."""
        dbus.send(self.summary.text(), self.body.toPlainText())
