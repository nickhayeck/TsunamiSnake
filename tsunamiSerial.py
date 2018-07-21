import serial


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
