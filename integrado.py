#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UNIVERSIDAD EL BOSQUE
PROYECTO INTEGRADO - TRANSFORMADAS / TRANSDUCTORES


Obtiene trozos de audio del microfono de forma recurrente
y grafica sus componentes en tiempo y frecuencia (FFT).

Detecta un tono puro en cualquier frecuencia audible, 
reproduce el tono puro y emite una senal de cancelacion

PEDRO GUILLEM
LUISA ECHEVERRY
DIANA NUNEZ

Copyright:

Utiliza Libreria SWHear 
descargada de:  http://github.com/swharden
"""

from PyQt4 import QtGui,QtCore
import sys
import ui_plot
import numpy as np
import pyqtgraph
import SWHear
from ctypes import *

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

#IMPLEMENTAMOS PRODUCTOR/CONSUMIDOR
class Cancelador(QtGui.QMainWindow, ui_plot.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #Antes de ejecutar el widget
        super(Cancelador, self).__init__(parent)
        self.setupUi(self)
        self.audioFFT.plotItem.showGrid(True, True, 0.7)
        self.audioPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT=0
        self.maxPCM=0
        self.ear = SWHear.SWHear() # INSTANCIAMOS PRODUCTOR/CONSUMIDOR
        self.ear.stream_start()
        self.deteccionIniciada = False
        self.cancelacionIniciada = False
        self.btnDetectar.clicked.connect(self.detectar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.vecesleido = 0
        self.terminal = sys.stdout
        self.cancelacionEnCurso=False

    def detectar(self):
        if not self.deteccionIniciada:
           self.deteccionIniciada = 1
           self.btnDetectar.setText(_translate("MainWindow", "SUSPENDER DETECCIÓN", None))
        else:
           self.deteccionIniciada = False
           self.btnDetectar.setText(_translate("MainWindow", "INICIAR DETECCIÓN", None))

    def cancelar(self):
        if not self.cancelacionIniciada:
           self.cancelacionIniciada = 1
           self.ear.AUDIOplay=False
           self.btnCancelar.setText(_translate("MainWindow", "APAGAR CANCELADOR", None))
        else:
           self.cancelacionIniciada = False
           self.cancelacionEnCurso=False
           self.ear.AUDIOplay=False
           self.ear.controlarCancelacion = False
           self.ear.ou.terminate();
           self.ear.fase = 0
           self.btnCancelar.setText(_translate("MainWindow", "ACTIVAR CANCELADOR", None))






	#INICIAMOS ACTUALIZACION PERMANENTE
    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax=np.max(np.abs(self.ear.data))
            if pcmMax>self.maxPCM:
                self.maxPCM=pcmMax #Obtenemos Amplitud maxima de Audio de Mic leido de productor
                self.audioPCM.plotItem.setRange(yRange=[-pcmMax,pcmMax])
            if np.max(self.ear.fft)>self.maxFFT:
                self.maxFFT=np.max(np.abs(self.ear.fft)) #Obtenemos amplitud maxima de FFT
                self.audioFFT.plotItem.setRange(yRange=[0,self.maxFFT]) #ESCALA SEGUN FREQ MAXIMA
            #self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
            pen=pyqtgraph.mkPen(color='b')
            self.audioPCM.plot(self.ear.datax,self.ear.data,
                            pen=pen,clear=True) 
            pen=pyqtgraph.mkPen(color='r')
            self.audioFFT.plot(self.ear.fftx[:2048],self.ear.fft[:2048],
                            pen=pen,clear=True) # Solo graficamos 2048 - 


                            
                            
                            
                            
            #CODIGO PARA DETECTAR PICOS EN ESPECTRO
            if self.deteccionIniciada: 
              indiceFFTX = np.argmax(self.ear.fft)
              freq1 = self.ear.fftx[indiceFFTX] # Frecuencia Candidata a cancelar
			  
              if freq1 > 60:
                self.vecesleido=self.vecesleido+1
                if self.vecesleido > 3:
                   self.ear.frecuenciaAcancelar =  int(freq1) #Establecemos la frecuencia a cancelar en EAR
                   self.ear.indiceFFTX = indiceFFTX #Informamos a EAR como leer la amplitud de la freq
                   self.vecesleido = 0
                   self.detectar()
                   self.dataLog.append('Freq. Candidata en: '+str(int(freq1))+' Hz')

                   
                   
                   
                   
                   
                   
                   

             #CODIGO CANCELADOR DE AUDIO
            if self.cancelacionIniciada:
               if self.ear.frecuenciaAcancelar != 0:

                 self.dataLog.moveCursor(QtGui.QTextCursor.End) #Aseguramos que el cursor del text este al final
                 # Iniciar prueba de fases 
                 if not self.cancelacionEnCurso:
                    self.dataLog.append("--Generando 360 fases para tono de "+str(self.ear.frecuenciaAcancelar)+" Hz")
                    self.dataLog.append("...Espere...")
                    self.ear.log = self.dataLog
                    self.ear.controlarCancelacion = True
                    self.ear.activarCancelacion()
                    self.cancelacionEnCurso=True

                 #Pintamos Periodo de Tono  Puro en Grafica
                 if self.ear.papa.poll():
                    msg = self.ear.papa.recv()    # El cancelador nos esta hablando
                    self.dataLog.append(' +'+str(msg)+' grados'+'  Amplitud: '+str(self.ear.fft[self.ear.indiceFFTX])+' dB')
                    pen=pyqtgraph.mkPen(color='b')
                    try:
                        plotfase = self.ear.fases[int(msg)]
                        plotfase = plotfase[0:self.ear.periodoAntiTono]
                        self.cancelData.plot(plotfase, pen=pen,clear=True)
                    except: 
                        pass
                    
               else:
                 self.dataLog.append('No hay freq aun')
        QtCore.QTimer.singleShot(1, self.update) # Actualizar graficos tan tapido como pueda

        
        
        
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = Cancelador()
    form.show()
    form.update()
    app.exec_()
    print("LISTO")
