# RaspPI3-acoustic-pure-tone-canceling
Raspberry3 turned into an acoustic pure-tone canceller. Using Python2.7

This is just a final project for my Transforms subject. It aims to scan the audible spectrum for pure-tones using FFT, to later produce a "counter tone" that will effectively cancel the source tone in the same frequency by finding the appropiate phase, using the principle of acoustic interference. 

The program will detect any idle audio card interfaces and start scanning the spectrum from the start. Make your piano sound any key or simply whistle, the code will pick up the frequency. 

In order to focus the program on the dominant pure-tone in the spectrum, click the "INICIAR DETECCION" button (Sorry, its in spanish). Once the program has a target frequency to cancel, you can then use the "ACTIVAR CANCELACION" button to start the cancellation process for the tone, which will generate a counter-tone on a speaker output sweeping all phases one by one till the amplitude of the source tone drops in the FFT. Effectively cancelling the tone on a fixed position in space.

This work uses modified versions of the following libraries :

(SWHear.py) by Scott Harden - Heavily Modified 
https://github.com/swharden/Python-GUI-examples

(rpi_audio_levels.so) by Colin Guyon - C++ GPU_FFT wrapper for RASP-PI3 
https://github.com/colin-guyon/rpi-audio-levels

# To Run
Clone files to the RPI3 on the same folder and run integrado.py. 
Uses Qt, should work on all graphical environments. (Thanks Scott for posting how to build Qt interfaces for PyQt)

* You should have a full-duplex sound card with a mic on ALSA device 0.
* My device is a 2 dollar C-Media USB audio card.
* I configured ALSA so this device always reports as CARD0 - Device0, ignoring the internal BCM chip for audio.

#Notes
This is still work in progress
The GPU_FFT function has not been yet implemented, but testing is underway.

* Special thanks to Colin Guyon and Scott Harden for sharing their audio tools and previous work
