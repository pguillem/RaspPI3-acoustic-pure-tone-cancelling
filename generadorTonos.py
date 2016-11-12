import numpy
import math
import pyaudio
import time

class generadorTonos(object):
 
    
 
    def __init__(self, deviceIndex,samplerate=44100, frames_per_buffer=8820):
        self.deviceIndex = deviceIndex
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False
        self.data=None
        self.i = 0;
        self.fases = None
        self.faseIndex = 0
        self.loglink = None
        print 'Tam buffer: '+str(frames_per_buffer)
 
    def callback(self, in_data, frame_count, time_info, status):
        #if self.buffer_offset < self.x_max:
            #if self.data==None:
            #   self.data = self.sinewave().astype(numpy.float32)
            #   print 'Seno empieza en: '+str(self.data[0])
            #print 'BufferOffset en: '+str(self.buffer_offset)+'de '+str(self.x_max)
    
        if self.faseIndex != 359:
            if self.i < 1:
              self.i = self.i + 1
              self.data = self.fases[self.faseIndex]
            else:
              self.i = 0
              self.faseIndex = self.faseIndex+1
              self.loglink.send(str(self.faseIndex))

            return (self.data.tostring(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)
            

    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False
 
    def play(self, frequency, duration, amplitude, fase, p):
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate
        print 'Omega: '+str(self.omega)
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.fase = fase
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * duration) - 1
        print 'XMAX: '+str(self.x_max)
		#INSTANCIAMOS AUDIO SALIENTE
        self.stream = p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output_device_index=self.deviceIndex,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)