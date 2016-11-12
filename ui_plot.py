# -*- coding: utf-8 -*-
"""
UNIVERSIDAD EL BOSQUE
PROYECTO INTEGRADO - TRANSFORMADAS / TRANSDUCTORES

PEDRO GUILLEM
LUISA ECHEVERRY
DIANA NUNEZ

Copyright:
Autor: PEDRO GUILLEM

Generado usando PyQT4 desde ui_plot.ui
"""

# Form implementation generated from reading ui file 'ui_plot.ui'
#
# Created: Sat Nov  5 22:10:24 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QtCore.QSize(900, 0))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.realtimeData = QtGui.QGroupBox(self.centralwidget)
        self.realtimeData.setGeometry(QtCore.QRect(10, 10, 611, 551))

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(65)
        self.realtimeData.setFont(font)
        self.realtimeData.setObjectName(_fromUtf8("realtimeData"))

        self.audioPCM = PlotWidget(self.realtimeData)
        self.audioPCM.setGeometry(QtCore.QRect(10, 30, 591, 201))
        self.audioPCM.setObjectName(_fromUtf8("audioPCM"))
        self.audioPCM.setLabel('left','Amplitud (mV)')
        self.audioPCM.setLabel('bottom','Tiempo','s')
        self.audioPCM.setTitle('Audio Microfono - PCM 16Bit - Entero con Signo (Little Endian)')

        self.audioFFT = PlotWidget(self.realtimeData)
        self.audioFFT.setGeometry(QtCore.QRect(10, 240, 591, 301))
        self.audioFFT.setObjectName(_fromUtf8("audioFFT"))
        self.audioFFT.setLabel('left','Amplitud','dB')
        self.audioFFT.setLabel('bottom','Frecuencua (4096 puntos)','Hz')
        self.audioFFT.setTitle('Fourier Discreta (Log10)')
		
		
        self.controlData = QtGui.QGroupBox(self.centralwidget)
        self.controlData.setGeometry(QtCore.QRect(630, 160, 261, 401))

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(65)

        self.controlData.setFont(font)
        self.controlData.setObjectName(_fromUtf8("controlData"))
		
        self.cancelData = PlotWidget(self.controlData)
        self.cancelData.setGeometry(QtCore.QRect(10, 230, 241, 161))
        self.cancelData.setObjectName(_fromUtf8("cancelData"))
        self.cancelData.setLabel('left','Amplitud','dB')
        self.cancelData.setLabel('bottom','Tiempo')
        self.cancelData.setTitle('Anti-Tono')

        self.btnDetectar = QtGui.QPushButton(self.controlData)
        self.btnDetectar.setGeometry(QtCore.QRect(40, 30, 171, 23))

        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(False)
        font.setWeight(50)
        self.btnDetectar.setFont(font)
        self.btnDetectar.setObjectName(_fromUtf8("btnDetectar"))
        self.btnCancelar = QtGui.QPushButton(self.controlData)
        self.btnCancelar.setGeometry(QtCore.QRect(40, 200, 171, 23))
        font = QtGui.QFont()
		
        font.setPointSize(7)
        font.setBold(False)

        self.btnCancelar.setFont(font)
        self.btnCancelar.setObjectName(_fromUtf8("btnCancelar"))
        self.dataLog = QtGui.QTextBrowser(self.controlData)
        self.dataLog.setFont(font)
        self.dataLog.setGeometry(QtCore.QRect(10, 60, 241, 131))
        self.dataLog.setObjectName(_fromUtf8("dataLog"))
        
		
        self.tprincipal = QtGui.QLabel(self.centralwidget)
        self.tprincipal.setGeometry(QtCore.QRect(630, 10, 251, 21))

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)

        self.tprincipal.setFont(font)
        self.tprincipal.setObjectName(_fromUtf8("tprincipal"))

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)

        self.tproyecto = QtGui.QLabel(self.centralwidget)
        self.tproyecto.setGeometry(QtCore.QRect(630, 30, 151, 16))
        self.tproyecto.setObjectName(_fromUtf8("tproyecto"))
        self.tproyecto.setFont(font)

        self.tproyecto2 = QtGui.QLabel(self.centralwidget)
        self.tproyecto2.setFont(font)
        self.tproyecto2.setGeometry(QtCore.QRect(630, 40, 181, 16))
        self.tproyecto2.setObjectName(_fromUtf8("tproyecto2"))

        self.pedro = QtGui.QLabel(self.centralwidget)
        self.pedro.setGeometry(QtCore.QRect(630, 70, 161, 16))
        self.pedro.setObjectName(_fromUtf8("pedro"))
        self.pedro.setFont(font)

        self.luisa = QtGui.QLabel(self.centralwidget)
        self.luisa.setGeometry(QtCore.QRect(630, 80, 161, 16))
        self.luisa.setObjectName(_fromUtf8("luisa"))
        self.luisa.setFont(font)

        self.diana = QtGui.QLabel(self.centralwidget)
        self.diana.setGeometry(QtCore.QRect(630, 90, 161, 16))
        self.diana.setObjectName(_fromUtf8("diana"))
        self.diana.setFont(font)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Proyecto Integrado - Cancelador Tonos Puros v0.1", None))
        self.realtimeData.setTitle(_translate("MainWindow", "ANÁLISIS EN TIEMPO REAL", None))
        self.controlData.setTitle(_translate("MainWindow", "CONTROL", None))
        self.btnDetectar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Iniciar Deteccion de Tonos Puros</p></body></html>", None))
        self.btnDetectar.setText(_translate("MainWindow", "INICIAR DETECCIÓN", None))
        self.btnCancelar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Activar/Desactivar Cancelador de Tonos</p></body></html>", None))
        self.btnCancelar.setText(_translate("MainWindow", "ACTIVAR CANCELADOR", None))
        self.tprincipal.setText(_translate("MainWindow", "Universidad el Bosque", None))
        self.tproyecto.setText(_translate("MainWindow", "Proyecto Integrado", None))
        self.tproyecto2.setText(_translate("MainWindow", "Transformadas / Transductores", None))
        self.pedro.setText(_translate("MainWindow", "PEDRO GUILLEM", None))
        self.luisa.setText(_translate("MainWindow", "LUISA ECHEVERRY", None))
        self.diana.setText(_translate("MainWindow", "DIANA NUÑEZ", None))

from pyqtgraph import PlotWidget
