# TsunamiSnake: the Tsunami WAV Trigger Serial Interface written in Python

Library for controlling robertsonics' Tsunami WAV Trigger via FTDI serial
written by Nicholas Hayeck (nick.hayeck@gmail.com)

### I. What is it?
The tsunami-wav-trigger-python library is serial interface for robertsonics' Super Tsunami WAV Trigger written entirely in Python 3.7 that makes use of the micro-controller's FTDI serial port to communicate commands to the board and control its functions. This library conforms to the standards set out [here](https://robertsonics.com/tsunami-user-guide/#serial-control)

### II. How is it structured?

The library (if you can really even call it that) consists of two files: the business end of the library that actually pushes commands to the board (tsunamiSerial.py) and the wrapper script that gives a neat little command line interface for programmers using other languages (audioInterface.py). For more on tsunamiSerial.py, see Section 3. For more on the wrapper class, see section 4.

### III. The Business Bit

tsunamiSerial.py is a class that contains several methods for accessing the Tsunami's capabilities, including the ability to get version and system information, stop all tracks, change individual output volume, change track volume, resume all paused tracks, change the offset of the sample rate, fade tracks in or out, play tracks, stop tracks, resume tracks, pause tracks, loop tracks, and load tracks. Each function performs one or multiple of these tasks. Most of the functions are self-explanatory and simple to use based upon the function name and parameter name, but `controlTrack` requires special explanation.

The track and output parameters are fairly self-explanatory, but the `controlCode` parameter is less so. It requires one of five strings: `'play', 'pause', 'resume', 'stop', 'loop on', 'loop off', 'load'` to function. From there, it's easy enough to understand.

### IV. Wrapping It Up

For those that would rather program in something more speedy than python or prefer another language, this wrapper class has been created to make the interface availible in any language with command-line access. To use the wrapper class, run the python file in the terminal or command prompt with your arguments like so: `python audioInterface.py [command [command args]]`. This command can be automated within another program quite easily, using whatever terminal accessing commands that language provides (e.g. a `system()` call in C++).<br><br> A list of commands and their arguments are found below:

 `info` - prints board version and system info<br>
 `play [track] [output]` - plays given track on given output <br>
 `pause  [track] [output]` - pauses given track on given output<br>
 `stop [track] [output]` - stops all tracks if no arguments are given, otherwise stops given track on given output <br>
 `resume [track] [output]` - resumes all tracks if no arguments are given, otherwise resumes given track on given output<br>
 `track_volume [track] [gain]` - sets gain of given track to given gain<br>
 `output_volume [output] [gain]` - sets gain of output <br>
 `loop [track] [output] [on/off]` - either loops or ends a loop of the given track on the given output<br>
 `fade [track] [gain] [time] [stop]` - fades a track to the given gain over the given time, and then stops or doesn't<br>
 `sample_offset [output] [offset]` - offsets the sample rate of an output<br>
 `load [track] [output]` - loads a given track onto a given output<br>
 
 All gain values must be between -70 and +10, outputs between 1-8, and offsets between -32768 & 32767, inclusive.
