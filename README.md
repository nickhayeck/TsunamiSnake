# TsunamiSnake: the Tsunami WAV Trigger Serial Interface written in Python

Library for controlling robertsonics' Tsunami WAV Trigger via FTDI serial
written by Nicholas Hayeck (nick.hayeck@gmail.com)

### I. What is it?
The tsunami-wav-trigger-python library is serial interface for robertsonics' Super Tsunami WAV Trigger written entirely in Python 3.7 that makes use of the micro-controller's FTDI serial port to communicate commands to the board and control its functions. This library conforms to the standards set out [here](https://robertsonics.com/tsunami-user-guide/#serial-control)

### II. How is it structured?

The library (if you can really even call it that) consists of two files: the business end of the library that actually pushes commands to the board (tsunamiSerial.py) and the wrapper script that gives a neat little command line interface for programmers using other languages (audioInterface.py). Think of tsunamiSerial.py as the car, and audioInterface.py as the steering wheel.
### III. The Business Bit

tsunamiSerial.py is a module that contains several methods for accessing the Tsunami's capabilities, including the ability to get version and system information, stop all tracks, change individual output volume, change volume by track, resume all paused tracks, change the offset of the sample rate, fade tracks in or out, play tracks, stop tracks, resume tracks, pause tracks, loop tracks, and load tracks. Each function performs one or multiple of these tasks. Most of the functions are self-explanatory and simple to use based upon the function name and parameter name, but `controlTrack` requires special explanation.

The track and output parameters are fairly self-explanatory, but the `controlCode` parameter is less so. It requires one of five strings: `'play', 'pause', 'resume', 'stop', 'loop on', 'loop off', 'load'` to function. From there, it's easy enough to understand.

### IV. Wrapping It Up

For those that would rather program in something more speedy than python or just prefer another language, this wrapper class has been created to make the interface available in any language with command-line access. To use the wrapper class, run the python file in the terminal or command prompt with your arguments like so: `python audioInterface.py [command [command args]]`. This command can be automated within another program quite easily, using whatever terminal accessing commands that language provides (e.g. a `system()` call in C++).<br><br> A list of commands and their arguments are found below:


|       Command       |            Arguments            |     Abbreviation         |     Description                            |
|---------------------|:-------------------------------:|:------------------------:|---------------------------------------------------------------------------------------------------------|
|`help`               |  *None*                         | `-h`                     | displays usage and a list of commands      |
|`info`               |  *None*                         | `-i`                     | prints board version and system info       |       
| `play`              | `[track] [output]`              | `-p`                     | plays given track on given output|
| `pause`             | `[track] [output]`              | `-pp`                    | pauses given track on given output|
| `stop`              | `[track] [output]`              | `-s`                     | stops all tracks if no arguments are given, otherwise stops given track on given output|
| `resume`            | `[track] [output]`              | `-r`                     | resumes all tracks if no arguments are given, otherwise resumes given track on given output|
| `track_volume`      | `[track] [gain]`                | `-tv`                    | sets gain of given track to given gain|
| `output_volume`     | `[output] [gain]`               | `-ov`                    | sets gain of output|
| `loop`              |`[track] [output] [on/off]`      | `-l`                     | either loops or ends a loop of the given track on the given output|
| `fade`              |`[track] [gain] [time] [stop]`   | `-f`                     | fades a track to the given gain over the given time, and then stops or doesn't (stop should be true or false)|
| `sample_offset`     | `[output] [offset]`             | `-so`                    | offsets the sample rate of an output|
| `queue`             | `[track] [output]`              | `-q`                     | plays track on output and pauses before any audio is played. It can then be resumed, starting the audio.|

 All gain values must be between -70 and +10, outputs between 1-8, and offsets between -32768 & 32767, inclusive.
