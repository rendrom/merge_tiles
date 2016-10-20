#!/usr/bin/env python
from __future__ import division
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
import os
import time
from threading import Thread
from PyQt4.QtCore import QString
from merge_tiles import VERSION, get_available_layers

LAYERS = get_available_layers()

class Progress(QtCore.QThread):

    notifyProgress = QtCore.pyqtSignal(int)
    closeDialog = QtCore.pyqtSignal(str)
    count = -1

    def __init__(self, layer, zoom, bbox):
        super(Progress, self).__init__()
        self.tile = LAYERS[str(layer)](zoom=zoom, bbox=bbox, threads=15)

    def stop(self):
        self.tile.stop = True
        self.notifyProgress.emit(100)

    def run(self):
        def timer_thread(tile):
            total = tile.total
            while self.count == -1 and not tile.stop:
                self.notifyProgress.emit((tile.count/total)*100)
                time.sleep(0.5)
        t = Thread(target=timer_thread, args=(self.tile,))
        t.start()
        self.count = self.tile.download()
        outpath = self.tile.merge_tiles()
        self.notifyProgress.emit(100)
        self.closeDialog.emit(outpath)


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.show()
        self.raise_()

    def setupUi(self):
        vbox = QtGui.QVBoxLayout()
        self.setFixedSize(800, 500)
        self.setWindowTitle("Tile Map Parser v%s" % VERSION)
        self.setWindowIcon(QtGui.QIcon('TileParser.ico'))
        self.setLayout(vbox)

        view = self.view = QtWebKit.QWebView()
        view.page().mainFrame().addToJavaScriptWindowObject("MainWindow", self)
        view.load(QtCore.QUrl(os.path.join('web', 'map.html')))
        view.loadFinished.connect(self.onLoadFinished)
        vbox.addWidget(view)

        form_layout = QtGui.QFormLayout()
        zoomlevels = self.zoomlevels = QtGui.QComboBox(self)
        zoomlevels.setMaximumWidth(60)
        zoomlevels.addItems(map(str, range(1, 22)))
        form_layout.addRow('Zoom level:', zoomlevels)

        layer = self.layer = QtGui.QComboBox(self)
        layer.setMaximumWidth(200)
        layer.addItems(LAYERS.keys())
        layer.currentIndexChanged.connect(self.on_layer_selected)
        form_layout.addRow('Service:', layer)
        vbox.addLayout(form_layout)

        button = QtGui.QPushButton('Run parser')
        run_parser = self.run_download
        button.clicked.connect(run_parser)
        vbox.addWidget(button)

    def onLoadFinished(self):
        frame = self.view.page().mainFrame()

        def load_script(scr):
            with open(scr, 'r') as f:
                frame.evaluateJavaScript(f.read())
        map(load_script, [
            os.path.join(*['web', 'leaflet', 'leaflet.js']),
            os.path.join(*['web', 'leaflet_areaselect', 'leaflet-areaselect.js']),
            os.path.join(*['web', 'layer', 'Google.js']),
            os.path.join(*['web', 'map.js'])])

    def on_layer_selected(self):
        frame = self.view.page().mainFrame()
        layer = self.layer.currentText()
        frame.evaluateJavaScript('changeLayer("%s")' % layer)

    @QtCore.pyqtSlot(str)
    def getBbox(self, bbox_str):
        
        def show_complete_message(outpath):
            QtGui.QMessageBox.about(self, QString("Complete"), QString("You file - %s" % outpath))

        bbox = map(float, bbox_str.split(','))
        progress = QtGui.QProgressDialog(
            "Parsing Log", "Stop", 0, 100, self)
        progress.setWindowTitle('Progress')
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress._progress = Progress(layer=self.layer.currentText(),
                                      zoom=int(self.zoomlevels.currentText()),
                                      bbox=bbox)
        progress._progress.notifyProgress.connect(progress.setValue)
        progress._progress.closeDialog.connect(show_complete_message)
        progress._progress.start()
        progress.canceled.connect(progress._progress.stop)

    def run_download(self):
        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript('MainWindow.getBbox(getBboxArray())')

    def pan_map(self, lng, lat):
        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript('map.panTo(L.latLng({}, {}));'.format(lat, lng))


if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = MainWindow()
    app.exec_()
