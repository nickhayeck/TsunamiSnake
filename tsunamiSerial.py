import serial

def littleEndianSplit(n):
    LSB = int.from_bytes(n.to_bytes(2,'little', signed=True)[:1], 'little', signed=True)
    MSB = int.from_bytes(n.to_bytes(2,'little', signed=True)[1:], 'little', signed=True)
    return LSB , MSB


class TsunamiSerial:




    def __init__(self, portal):
        self.sClass = serial.Serial(port=portal, baudrate=57600, timeout=5) #define serial port with baudrate of 57.6kbps
        self.SOM1 = 0xf0
        self.SOM2 = 0xaa
        self.EOM  = 0x55




    def getSysInfo(self):
        """returns the version and system information of the tsunami board"""
        self.sClass.write([self.SOM1, self.SOM2, 5, 1, self.EOM]) #request version
        self.sClass.read(4) #flush the first four bytes
        out = self.sClass.read(23).decode("utf-8")[:-1]#read until self.EOM

        self.sClass.write([self.SOM1, self.SOM2, 5, 2, self.EOM]) #request sys_info
        self.sClass.read(4) #flush the first four bytes
        out += '\nVoices: ' + str(int.from_bytes(self.sClass.read(),byteorder='little'))
        out += '\nTracks: ' + str(int.from_bytes(self.sClass.read(2), byteorder='little')) + '\n'
        self.sClass.read()
        return out



    def stopAll(self):
        self.sClass.write([self.SOM1, self.SOM2, 5, 4, self.EOM])



    def outputVolume(self, output, gain):
        channel = output - 1 #channel indexing starts at 0 for some reason


        #acceptable channel values are between 1 and 8
        if channel not in range(8):
            raise ValueError('Your output value of {} was outside the range of 1 & 8'.format(gain))
        #acceptable gain values are between -70 and 10
        if gain not in range(-71, 11):
            raise ValueError('Your gain value of {} was outside the range of -70 & 10'.format(gain))

        gainBytesLSB, gainBytesMSB = littleEndianSplit(gain)


        self.sClass.write([self.SOM1, self.SOM2, 0x08, 0x05, channel, gainBytesLSB, gainBytesMSB, self.EOM])



    def trackVolume(self, track, gain):
        #acceptable gain values are between -70 and 10
        if gain not in range(-71, 11):
            raise ValueError('Your gain value of {} was outside the range of -70 & 10'.format(gain))

        trackBytesLSB, trackBytesMSB = littleEndianSplit(track)
        gainBytesLSB, gainBytesMSB = littleEndianSplit(gain)

        self.sClass.write([self.SOM1, self.SOM2, 0x09, 0x08, trackBytesLSB, trackBytesMSB, gainBytesLSB, gainBytesMSB, self.EOM])



    def resumeAllPaused(self):
        self.sClass.write([0xf0, 0xaa, 0x05, 0x0b, 0x55])



    def sampleRateOffset(self, output, offset):
        channel = output - 1 #channel indexing starts at 0 for some reason

        #acceptable channel values are between 1 and 8
        if channel not in range(8):
            raise ValueError('Your output value of {} was outside the range of 1 & 8'.format(channel))
        if offset not in range(-32769, 32768):
            raise ValueError('Your offset value of {} was outside the range of -32768 & 3276'.format(offset))

        offsetBytesLSB, offsetBytesMSB = littleEndianSplit(offset)

        self.sClass.write([0xf0, 0xaa, 0x08, 0x0c, channel, offsetBytesLSB, offsetBytesMSB, self.EOM])



    def trackFade(self, track, gain, time, stop):
        #acceptable gain values are between -70 and 10
        if gain not in range(-70, 10):
            raise ValueError('Your gain value of {} was outside the range of -70 & 10'.format(gain))

        trackBytesLSB, trackBytesMSB = littleEndianSplit(track)

        gainBytesLSB, gainBytesMSB = littleEndianSplit(gain)


        timeBytesLSB, timeBytesMSB = littleEndianSplit(time)


        stopBytes = 0x01 if stop else 0x00

        self.sClass.write([self.SOM1, self.SOM2, 0x0c, 0x0a, trackBytesLSB, trackBytesMSB, gainBytesLSB, gainBytesMSB, timeBytesLSB, timeBytesMSB, stopBytes, self.EOM])



    def controlTrack(self, track, controlCode, output):

        channel = output - 1 #channel indexing starts at 0 for some reason

        #acceptable channel values are between 1 and 8
        if channel not in range(8):
            raise ValueError('Your output value of {} was outside the range of 1 & 8'.format(channel))

        if controlCode not in ['play', 'pause', 'resume', 'stop', 'loop on', 'loop off', 'load']:
            raise ValueError('incorrect controlCode: {} is not a valid control code'.format(controlCode))

        codeConverter = {'play' : 1, 'pause' : 2, 'resume': 3, 'stop' : 4, 'loop on': 5, 'loop off': 6, 'load' : 7}
        code = codeConverter[controlCode]

        trackBytesLSB, trackBytesMSB = littleEndianSplit(track)

        self.sClass.write([self.SOM1, self.SOM2, 0x0a, 0x03, code, trackBytesLSB, trackBytesMSB, channel, 0x00, self.EOM])
    def closePort(self):
        self.sClass.close()
