# RaspPI3-acoustic-pure-tone-canceling
Raspberry3 turned into an acoustic pure-tone canceller. Using Python2.7

Just a final project for my Transforms lecture. It aims to scan the audible spectrum for pure-tones using FFT, and produce a "counter tone" that will effectively cancel the same frequency, by finding the appropiate phase angle using the principle of acoustic interference.

The program detects any idle audio card interface and starts using its mike to scan the spectrum. Make your piano play any key - or simply whistle, the code will pick up the frequency. 

In order to focus the program on the dominant pure-tone in the spectrum, click the "INICIAR DETECCION" button (Sorry, its in spanish). Once the program has a target frequency to cancel, you can use the "ACTIVAR CANCELACION" button to start the interference, generating a counter-tone on a speaker output sweeping all phases one by one till the amplitude of the source tone drops in the FFT.

This code uses modified versions of the following libraries:

(SWHear.py) by Scott Harden - Heavily Modified 
https://github.com/swharden/Python-GUI-examples

(rpi_audio_levels.so) by Colin Guyon - C++ GPU_FFT wrapper for RASP-PI3 
https://github.com/colin-guyon/rpi-audio-levels

# To Run
Clone the repo to your RPI3 and run integrado.py. 
Uses PyQt, should work on all graphical environments.

* You should have a full-duplex sound card with a mic on ALSA device 0.
* My device is a 2 dollar C-Media USB audio card. Worked like a charm.
* I configured ALSA so this device always reports as CARD0 - Device0, ignoring the internal BCM chip for audio.
* You need a pure sine wave tone generator to thest it properly.

#Notes
Work in progress...
The GPU_FFT function has not been yet implemented, but testing is underway. Currently the code runs on numpy.fft()

* Special thanks to Colin Guyon and Scott Harden for sharing their audio tools and previous work
