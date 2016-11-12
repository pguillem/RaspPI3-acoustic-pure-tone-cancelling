"""
UNIVERSIDAD EL BOSQUE
PROYECTO INTEGRADO - TRANSFORMADAS / TRANSDUCTORES

PEDRO GUILLEM
LUISA ECHEVERRY
DIANA NUNEZ

Copyright:
Libreria SWHear descargada de:  http://github.com/swharden
Autor: Scott Harden (swharden@gmail.com)


Modificada por: PEDRO GUILLEM
"""

import pyaudio
import math
import sys
import time
import pylab
import numpy as np
import threading
import scipy
import scipy.fftpack
from generadorTonos import generadorTonos
from multiprocessing import Process, Pipe

def getFFT(data,rate):
    data=data*np.hamming(len(data))
    fft=np.fft.fft(data)
    fft=np.abs(fft)
    fft=10*np.log10(fft) #PEDRO - Aplicamos LOG para linealizar FFT .. 
    freq=np.fft.fftfreq(len(fft),1.0/rate)
    return freq[:int(len(freq)/2)],fft[:int(len(fft)/2)]


class SWHear(object):
    """
    The SWHear class is made to provide access to continuously recorded
    (and mathematically processed) microphone data.
    """

    def __init__(self,device=None,rate=None):
        """fire up the SWHear class."""
        self.p=pyaudio.PyAudio()
        self.chunk = 8912 # numero de puntos a leer en una sola lectura (4096, 8912)
        self.device=device
        self.rate=rate
        self.deviceOUT=None  
        self.seno=None
        self.fase=0
        self.frecuenciaAcancelar=0
        self.indiceFFTX = 0
        self.log=None #Objeto Log
        self.controlarCancelacion = True
        self.generator=None
        self.duracion_audio = 0
        self.fases = []
        self.periodoAntiTono = 0
    ### SYSTEM TESTS

    def valid_low_rate(self,device):
        """set the rate to the lowest supported audio rate."""
        for testrate in [44100]:
            if self.valid_test(device,testrate):
                return testrate
        print("SOMETHING'S WRONG! I can't figure out how to use DEV",device)
        return None

    def valid_test(self,device,rate=44100):
        """given a device ID and a rate, return TRUE/False if it's valid."""
        try:
            self.info=self.p.get_device_info_by_index(device)
            if not self.info["maxInputChannels"]>0:
                return False
            stream=self.p.open(format=pyaudio.paInt16,channels=1,
               input_device_index=device,frames_per_buffer=self.chunk,
               rate=int(self.info["defaultSampleRate"]),input=True)
            stream.close()
            return True
        except:
            return False

    def valid_test_out(self,device,rate=44100):
        """Encontramos canales de audio saliente""" #PEDRO
        try:
            self.infoout=self.p.get_device_info_by_index(device)
            if self.infoout["maxInputChannels"]>0:
                return False
            stream=self.p.open(format=pyaudio.paInt16,channels=1,
               output_device_index=device,frames_per_buffer=1024,
               rate=int(self.infoout["defaultSampleRate"]),output=True)
            stream.close()
            return True
        except:
            return False

    def valid_input_devices(self):
        """
        See which devices can be opened for microphone input.
        call this when no PyAudio object is loaded.
        """
        mics=[] 
        for device in range(self.p.get_device_count()):
            if self.valid_test(device):
                mics.append(device)
        if len(mics)==0:
            print("no se encontraron microfonos!")
        else:
            print("encontrados %d microfonos en indices: %s"%(len(mics),mics))
        return mics

    def valid_output_devices(self):
        """
        Encontramos Canales salientes en dispositivo
        """
        parlantes=[] 
        for device in range(self.p.get_device_count()):
            if self.valid_test_out(device):
                print str(device)
                parlantes.append(device)
        if len(parlantes)==0:
            print("no se encontraron dispositivos de audio saliente!")
        else:
            print("encontrado %d disp de salida : %s"%(len(parlantes),parlantes))
        return parlantes

### SETUP AND SHUTDOWN

    def initiate(self):
        """run this after changing settings (like rate) before recording"""
        if self.device is None:
            self.device=self.valid_input_devices()[0] #pick the first one
        if self.rate is None:
            self.rate=self.valid_low_rate(self.device)
        if not self.valid_test(self.device,self.rate):
            print("guessing a valid microphone device/rate...")
            self.device=self.valid_input_devices()[0] #pick the first one
            self.rate=self.valid_low_rate(self.device)
        self.datax=np.arange(self.chunk)/float(self.rate)
        msg='grabando de "%s" '%self.info["name"]
        msg+='(dispositivo %d) '%self.device
        msg+='en %d Hz'%self.rate
        print(msg)


    def close(self):
        """gently detach from things."""
        print(" -- sending stream termination command...")
        self.keepRecording=False #finalizar todos los hilos de captura
        self.AUDIOplay=False #finalizar todos los hilos de reproduccion (Siempre habra solo uno)
        while(self.t.isAlive()): #esperar a que finalicen todos los hilos
            time.sleep(.1)
        self.stream.stop_stream()
        self.p.terminate() #finalizar PYaudio

    ### STREAM HANDLING

    def stream_readchunk(self):
        """reads some audio and re-launches itself"""
        try:
            self.data = np.fromstring(self.stream.read(self.chunk),dtype=np.int16)
            self.fftx, self.fft = getFFT(self.data,self.rate)
        except Exception as E:
            print(" -- oops exepcion! terminando...")
            print(E,"\n"*5)
            self.keepRecording=False
        if self.keepRecording:
            self.stream_thread_new()
        else:
            self.stream.close()
            self.p.terminate()
            print(" -- stream INICIADO")

    def stream_thread_new(self):
        self.t=threading.Thread(target=self.stream_readchunk)
        self.t.start()


    ###CONTROL DE STREAM SALIENTE - CANCELADOR

    def activarCancelacion(self): #Activa cancelador de Audio - LLamado desde integrado.py
         self.log.append('Iniciando Cancelacion..')
         freqMuestreo = 44100
         self.fase = 0
         
         #Calculamos tamano exacto de ventana para frecuencua
         tamMuestra = float(1)/freqMuestreo
         periodo    = float(1)/self.frecuenciaAcancelar
         
         factor = int(0.23/periodo) # Todas las muestras de cualquier frecuencia deben ser del mismo largo
         self.duracion_audio = float(periodo*factor)
         ventana = int(math.ceil(freqMuestreo * self.duracion_audio)) - 1
         self.periodoAntiTono = int(periodo/tamMuestra) # tamano de un periodo en vector
         
         print 'Periodo: '+str(periodo)
         print 'Duracion: '+str(self.duracion_audio)
         print 'Factor de Ajuste:'+str(factor)
		 
         self.generador = generadorTonos(0,freqMuestreo,ventana) # Instanciamos generador de tonos
         
         #Generamos todas las fases para la frecuencia
         volumen = 1              # Volumen (Amplitud) de la onda
         self.fases = []
         fase = 0
         
         #Crear array de 360 senos
         self.omega = float(self.frecuenciaAcancelar) * (math.pi * 2) / freqMuestreo
         
         for x in range(0,359):
            xs = np.arange(0,ventana)
            self.fases.append((volumen * np.sin(xs * self.omega + fase)).astype(np.float32)) #Generamos todas las fases de Freq
            fase = fase+0.017 
         
         #Creamos canal entre Proceso y Clase padre (esta clase)
         papa, hijo = Pipe() 
         self.papa = papa
         self.ou=Process(target=self.stream_out_cancelar, args=(volumen,ventana,freqMuestreo,hijo,)) #Creamos hilo de cancelacion
         self.ou.start() # Iniciamos reproductor de sonido
         
         self.log.append("Fases ocupan: "+str(sys.getsizeof(self.fases))+" Kb")
         self.log.append("")
         self.log.append("--PROBABDO CON TODAS LAS FASES---")         

         
         
    def stream_out_cancelar(self,volumen, ventana,freqMuestreo,hijo):
         self.generador.fases = self.fases # Empezamos con primera fase
         self.generador.loglink = hijo
         doWork = True
         contarPass = 0
         while self.controlarCancelacion==True and doWork:
           self.generador.play(self.frecuenciaAcancelar, self.duracion_audio, volumen, self.fase, self.p)
        
           while self.generador.is_playing():
            pass
           doWork = False
            
            
    def stream_start(self):
        """adds data to self.data until termination signal"""
        self.initiate()
        print(" -- starting stream")
        self.keepRecording=True # Controla si se debe seguir grabando audio
        self.data=None 
        self.fft=None
        self.dataFiltered=None 

        #INSTANCIAMOS AUDIO ENTRANTE
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1,
                      rate=self.rate,input=True,frames_per_buffer=self.chunk)

        
        self.stream_thread_new()

if __name__=="__main__":
    ear=SWHear()
    ear.stream_start() #ejecutar para siempre
    while True:
        print(ear.data)
        time.sleep(.1)
    print("FINAL")
