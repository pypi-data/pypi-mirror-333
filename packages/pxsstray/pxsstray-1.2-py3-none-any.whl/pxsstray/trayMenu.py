from importlib.resources import files
from PySide6 import QtCore, QtGui, QtWidgets
from Xlib import display, X
from Xlib.ext import dpms
import time


class TrayMenu(QtWidgets.QSystemTrayIcon):
    def __init__(self, app):
        super().__init__()
        iconPath = str(files("pxsstray.images").joinpath("cross.png"))
        self.icon = QtGui.QIcon(iconPath)
        self.setIcon(self.icon)
        self.setVisible(True)

        self.display = display.Display()

        self.menu = QtWidgets.QMenu()

        saverInfo = self.display.get_screen_saver()
        timeout = int(saverInfo._data["timeout"])
        self.screenSaverTimeout = timeout if timeout > 0 else 600
        self.toggleS = QtGui.QAction(
            f"Enable ScreenSaver (timeout: {self.screenSaverTimeout})"
        )
        self.toggleS.setCheckable(True)
        self.toggleS.setChecked(timeout > 0)
        self.toggleS.toggled.connect(self.enableS)
        self.menu.addAction(self.toggleS)

        dpmsInfo = self.display.dpms_info()
        self.toggleDPMS = QtGui.QAction("Enable DPMS")
        self.toggleDPMS.setCheckable(True)
        self.toggleDPMS.setChecked(dpmsInfo.state)
        self.toggleDPMS.toggled.connect(self.enableDPMS)
        self.menu.addAction(self.toggleDPMS)

        self.menu.addSeparator()

        self.activateScreenSaver = QtGui.QAction("Force ScreenSaver")
        self.activateScreenSaver.triggered.connect(self.forceScreenSaver)
        self.menu.addAction(self.activateScreenSaver)

        self.activateDPMS = QtGui.QAction("Force DPMS")
        self.activateDPMS.triggered.connect(self.forceDPMS)
        self.menu.addAction(self.activateDPMS)

        self.menu.addSeparator()
        self.quit = QtGui.QAction("Quit")
        self.quit.triggered.connect(app.quit)
        self.menu.addAction(self.quit)

        self.setContextMenu(self.menu)

    @QtCore.Slot()
    def enableDPMS(self, enabled):
        current_info = self.display.dpms_info()
        if current_info.state:
            self.display.dpms_disable()
        else:
            self.display.dpms_enable()

        self.display.sync()

    @QtCore.Slot()
    def enableS(self, enabled):
        saverInfo = self.display.get_screen_saver()
        timeout = int(saverInfo._data["timeout"])
        if timeout > 0:
            timeout = 0
        else:
            timeout = self.screenSaverTimeout

        interval = int(saverInfo._data["interval"])
        prefer_blank = bool(saverInfo._data["prefer_blanking"])
        allow_exposures = bool(saverInfo._data["allow_exposures"])

        self.display.set_screen_saver(timeout, interval, prefer_blank, allow_exposures)
        self.display.sync()

    @QtCore.Slot()
    def forceDPMS(self):
        self.toggleDPMS.setChecked(True)
        self.display.dpms_enable()
        self.display.sync()
        self.display.dpms_force_level(dpms.DPMSModeOff)
        self.display.sync()

    @QtCore.Slot()
    def forceScreenSaver(self):
        self.display.force_screen_saver(X.ScreenSaverActive)
        self.display.sync()
