import sys
import serial


##################################################
# Serial Port to be used. Look in device manager #
# for COM port name. Should look like "COM4"     #
##################################################
serialPort = 'COM4'

SOM1 = 0xf0
SOM2 = 0xaa
EOM  = 0x55

print('Opening port on \"{}\"...\n\n'.format(serialPort))
s = serial.Serial(port=serialPort, baudrate=57600, timeout=5) #define serial port with baudrate of 57.6kbps

def littleEndianSplit(n):
    LSB = int.from_bytes(n.to_bytes(2,'little', signed=True)[:1], 'little', signed=True)
    MSB = int.from_bytes(n.to_bytes(2,'little', signed=True)[1:], 'little', signed=True)
    return LSB , MSB

def getSysInfo():
    """returns the version and system information of the tsunami board"""
    s.write([SOM1, SOM2, 5, 1, EOM]) #request version
    s.read(4) #flush the first four bytes
    out = s.read(23).decode("utf-8")[:-1]#read until EOM

    s.write([SOM1, SOM2, 5, 2, EOM]) #request sys_info
    s.read(4) #flush the first four bytes
    out += '\nVoices: ' + str(int.from_bytes(s.read(),byteorder='little'))
    out += '\nTracks: ' + str(int.from_bytes(s.read(2), byteorder='little')) + '\n'
    return out



def stopAll():
    s.write([SOM1, SOM2, 5, 4, EOM])



def outputVolume(output, gain):
    channel = output - 1 #channel indexing starts at 0 for some reason


    #acceptable channel values are between 1 and 8
    if channel not in range(8):
        raise ValueError('Your output value of {} was outside the range of 1 & 8'.format(gain))
    #acceptable gain values are between -70 and 10
    if gain not in range(-71, 11):
        raise ValueError('Your gain value of {} was outside the range of -70 & 10'.format(gain))

    gainBytesLSB, gainBytesMSB = littleEndianSplit(gain)


    s.write([SOM1, SOM2, 0x08, 0x05, channel, gainBytesLSB, gainBytesMSB, EOM])



def trackVolume(track, gain):
    #acceptable gain values are between -70 and 10
    if gain not in range(-71, 11):
        raise ValueError('Your gain value of {} was outside the range of -70 & 10'.format(gain))

    trackBytesLSB, trackBytesMSB = littleEndianSplit(track)
    gainBytesLSB, gainBytesMSB = littleEndianSplit(gain)

    s.write([SOM1, SOM2, 0x09, 0x08, trackBytesLSB, trackBytesMSB, gainBytesLSB, gainBytesMSB, EOM])



def resumeAllPaused():
    s.write([0xf0, 0xaa, 0x05, 0x0b, 0x55])



def sampleRateOffset(output, offset):
    channel = output - 1 #channel indexing starts at 0 for some reason

    #acceptable channel values are between 1 and 8
    if channel not in range(8):
        raise ValueError('Your output value of {} was outside the range of 1 & 8'.format(channel))
    if offset not in range(-32769, 32768):
        raise ValueError('Your offset value of {} was outside the range of -32768 & 3276'.format(offset))

    offsetBytesLSB, offsetBytesMSB = littleEndianSplit(offset)

    s.write([0xf0, 0xaa, 0x08, 0x0c, channel, offsetBytesLSB, offsetBytesMSB, EOM])



def trackFade(track, gain, time, stop):
    #acceptable gain values are between -70 and 10
    if gain not in range(-70, 10):
        raise ValueError('Your gain value of {} was outside the range of -70 & 10'.format(gain))

    trackBytesLSB, trackBytesMSB = littleEndianSplit(track)

    gainBytesLSB, gainBytesMSB = littleEndianSplit(gain)


    timeBytesLSB, timeBytesMSB = littleEndianSplit(time)


    stopBytes = 0x01 if stop else 0x00

    s.write([SOM1, SOM2, 0x0c, 0x0a, trackBytesLSB, trackBytesMSB, gainBytesLSB, gainBytesMSB, timeBytesLSB, timeBytesMSB, stopBytes, EOM])



def controlTrack(track, controlCode, output):
    channel = output - 1 #channel indexing starts at 0 for some reason

    #acceptable channel values are between 1 and 8
    if channel not in range(8):
        raise ValueError('Your output value of {} was outside the range of 1 & 8'.format(channel))

    if controlCode not in ['play', 'pause', 'resume', 'stop', 'loop on', 'loop off', 'load']:
        raise ValueError('incorrect controlCode: {} is not a valid control code'.format(controlCode))

    codeConverter = {'play' : 1, 'pause' : 2, 'resume': 3, 'stop' : 4, 'loop on': 5, 'loop off': 6, 'load' : 7}
    code = codeConverter[controlCode]

    trackBytesLSB, trackBytesMSB = littleEndianSplit(track)

    s.write([SOM1, SOM2, 0x0a, 0x03, code, trackBytesLSB, trackBytesMSB, channel, 0x00, EOM])
def end():
    s.close()



##################################################
################ Begin Parser ####################
##################################################



if len(sys.argv)  == 1:
    sys.exit('Too few arguments')

if serialPort == '':
    print("\n\n+---------------------------------------------+")
    print("+ PLEASE SET SERIAL PORT IN audiointerface.py +")
    print("+---------------------------------------------+\n")

    sys.exit(1)


if '-h' in sys.argv or '--help' in sys.argv:
    print("Command Line Interface for the Tsunami WAV Trigger"+
          "\n\nUsage: python audioInterface.py [command] [command args]"+
          "\nExample: python audioInterface.py play 1 1"+
          "\n\nCommands:\n info\n play\n pause\n stop\n resume\n track_volume\n output_volume\n loop\n fade\n sample_offset\n load\n end\n"+
          "\n\n\nRefer to documentation for more info on each command")
    sys.exit(0)

print('Opening port on \"{}\"...\n\n'.format(serialPort))
s = serial.Serial(port=serialPort, baudrate=57600, timeout=5) #define serial port with baudrate of 57.6kbps and read timeout of 5 seconds


#info command
if sys.argv[1] == 'info':
    print(getSysInfo())


#Stop command
if sys.argv[1] == 'stop':
    if len(sys.argv) == 2:
        stop_all()
    elif len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the STOP command. If you\'re trying to stop a \nspecific track, it should be of the form: stop [track] [output]')
    else:
        controlTrack(sys.argv[2], 'stop', sys.argv[3])
        print("Stop command for track {} sent".format(sys.argv[2]))


#Resume command
if sys.argv[1] == 'resume':
    if len(sys.argv) == 2:
        resumeAllPaused()
    elif len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the RESUME command. If you\'re trying to resume a \nspecific track, it should be of the form: resume [track] [output]')
    else:
        controlTrack(sys.argv[2], 'resume', sys.argv[3])
        print("Resume command for track {} sent".format(sys.argv[2]))


#output_volume command
if sys.argv[1] == 'output_volume':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the output_volume command. It should be of the form: output_volume [output] [gain]')
    else:
        outputVolume(sys.argv[2], sys.argv[3])
        print("Volume command for output {} sent".format(sys.argv[2]))

#track_volume command
if sys.argv[1] == 'track_volume':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the track_volume command. It should be of the form: track_volume [track] [gain]')
    else:
        trackVolume(sys.argv[2], sys.argv[3])
        print("Volume command for track {} sent".format(sys.argv[2]))


#sample_offset command
if sys.argv[1] == 'sample_offset':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the sample_offset command. It should be of the form: sample_offset [output] [offset]')
    else:
        sampleRateOffset(sys.argv[2], sys.argv[3])
        print("Offset command for output {} sent".format(sys.argv[2]))


#Play command
if sys.argv[1] == 'play':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the PLAY command. It should be of the form: play [track] [output]')
    else:
        controlTrack(int(sys.argv[2]), 'play', int(sys.argv[3]))
        print("Play command for track {} sent".format(sys.argv[2]))

#Pause command
if sys.argv[1] == 'pause':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the PAUSE command. It should be of the form: pause [track] [output]')
    else:
        controlTrack(sys.argv[2], 'pause', sys.argv[3])
        print("Pause command for track {} sent".format(sys.argv[2]))

#Load command
if sys.argv[1] == 'load':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the LOAD command. It should be of the form: load [track] [output]')
    else:
        controlTrack(sys.argv[2], 'load', sys.argv[3])
        print("Load command for track {} onto output {} sent".format(sys.argv[2], sys.argv[3]))


#Fade command
if sys.argv[1] == 'fade':
    if len(sys.argv) != 6:
        sys.exit('Too many or too few arguments for the FADE command. It should be of the form: fade [track] [gain] [time] [stop]')
    else:
        trackFade(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        print("Fading track {} {}dB over {} sent".format(sys.argv[2], sys.argv[3], sys.argv[4]))
#Loop command
if sys.argv[1] == 'loop':
    if len(sys.argv) != 5:
        sys.exit('Too many or too few arguments for the LOOP command. It should be of the form: loop [track] [output] [on/off]')
    if sys.argv[5] not in ['on', 'off']:
        sys.exit('Third argument for command LOOP should either be on or off')
    else:
        controlTrack(sys.argv[2], ('loop on' if sys.argv[5] == 'on' else 'loop off'), sys.argv[3])
        print("Loop command for track {} onto output {} sent".format(sys.argv[2], sys.argv[3]))




#Close COM port when done
end()
