# RaspPI3-acoustic-pure-tone-canceling
Raspberry3 turned into an acoustic pure-tone canceller. Using Python2.7

This is just a final project for my Transforms subject. It aims to scan the audible spectrum for pure-tones using FFT, in order to produce a "counter tone" that will effectively cancel the source by finding the appropiate phase.

#This work includes modified versions of the following libraries of other contributors:

(SWHear.py) by Scott Harden - Heavily Modified
https://github.com/swharden/Python-GUI-examples

(rpi_audio_levels.so) by Colin Guyon - Fast GPU FFT lib for RPI3
https://github.com/colin-guyon/rpi-audio-levels

# To Run
Unpack to the RPI3 on the same folder. Uses Qt, should work on all graphical environments.

* You should have a full-duplex sound card on ALSA device 0.
* My device is a 2 dollar C-Media USB audio card.
* I configured ALSA so this device always reports as CARD0 - Device0, ignoring the internal BCM chip for audio.
