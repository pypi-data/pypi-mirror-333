# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations
import sys
from PySide6 import QtGui, QtWidgets

from pxsstray import trayMenu


def run():
    app = QtWidgets.QApplication()

    if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(
            None, "Systray", "I couldn't detect any system tray on this system."
        )
        sys.exit(1)

    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)

    _ = trayMenu.TrayMenu(app)

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
