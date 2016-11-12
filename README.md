# RaspPI3-acoustic-pure-tone-canceling
Raspberry3 turned into an acoustic pure-tone canceller. Using Python2.7

This is just a final project for my Transforms subject. It aims to scan the audible spectrum for pure-tones using FFT, in order to produce a "counter tone" that will effectively cancel the source by finding the appropiate phase. The program will detect idle interfaces and start scanning the spectrum from the start.

Make your piano sound any key or simpply whistle. In order to identify a pure tone in the spectrum, click "INICIAR DETECCION" (Sorry its in spanish). Once the program has a frequency to cancel, you can then use the "ACTIVAR CANCELACION" button to start the cancellation process, which will reproduce all phases of the frequency till the amplitude of the source tone drops in the FFT.

#This work includes modified versions of the following libraries of other contributors:

(SWHear.py) by Scott Harden - Heavily Modified
https://github.com/swharden/Python-GUI-examples

(rpi_audio_levels.so) by Colin Guyon - Fast GPU FFT lib for RPI3
https://github.com/colin-guyon/rpi-audio-levels

Depends on the following modules:
pyaudio
numpy
math
sys
multiprocessing
threading
pylab
scipy
PyQt

# To Run
Unpack to the RPI3 on the same folder and run integrado.py. 
Uses Qt, should work on all graphical environments.

* You should have a full-duplex sound card with a mic on ALSA device 0.
* My device is a 2 dollar C-Media USB audio card.
* I configured ALSA so this device always reports as CARD0 - Device0, ignoring the internal BCM chip for audio.

#Notes
This is still work in progress
The GPU_FFT function has not been yet implemented, but testing is underway.

* Special thanks to Colin Guyon and Scott Harden for sharing their audio tools and previous work
