import sys
import serial
import tsunamiSerial


    ##################################################
    # Serial Port to be used. Look in device manager #
    # for COM port name. Should look like "COM4"     #
    ##################################################

interfacePort = 'COM4'


##################################################
################ Begin Parser ####################
##################################################



if len(sys.argv)  == 1:
    sys.exit("Command Line Interface for the Tsunami WAV Trigger"+
          "\n\nUsage: python audioInterface.py [command] [command args]"+
          "\nExample: python audioInterface.py play 1 1"+
          "\n\nCommands:\n info\n play\n pause\n stop\n resume\n track_volume\n output_volume\n loop\n fade\n sample_offset\n load\n"+
          "\n\n\nRefer to documentation for more info on each command")

if interfacePort == '':
    print("\n\n+---------------------------------------------+")
    print("| PLEASE SET SERIAL PORT IN audioInterface.py |")
    print("+---------------------------------------------+\n")

    sys.exit(1)


if '-h' in sys.argv or '--help' in sys.argv:
    print("Command Line Interface for the Tsunami WAV Trigger"+
          "\n\nUsage: python audioInterface.py [command] [command args]"+
          "\nExample: python audioInterface.py play 1 1"+
          "\n\nCommands:\n info\n play\n pause\n stop\n resume\n track_volume\n output_volume\n loop\n fade\n sample_offset\n load\n"+
          "\n\n\nRefer to documentation for more info on each command")
    sys.exit(0)

print('Opening port on \"{}\"...\n'.format(interfacePort))

serialControl = tsunamiSerial.TsunamiSerial(interfacePort)


#info command
if sys.argv[1] == 'info':
    print(serialControl.getSysInfo())


#Stop command
if sys.argv[1] == 'stop':
    if len(sys.argv) == 2:
        serialControl.stop_all()
    elif len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the STOP command. If you\'re trying to stop a \nspecific track, it should be of the form: stop [track] [output]')
    else:
        serialControl.controlTrack(sys.argv[2], 'stop', sys.argv[3])
        print("Stop command for track {} sent".format(sys.argv[2]))


#Resume command
if sys.argv[1] == 'resume':
    if len(sys.argv) == 2:
        resumeAllPaused()
    elif len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the RESUME command. If you\'re trying to resume a \nspecific track, it should be of the form: resume [track] [output]')
    else:
        serialControl.controlTrack(sys.argv[2], 'resume', sys.argv[3])
        print("Resume command for track {} sent".format(sys.argv[2]))


#output_volume command
if sys.argv[1] == 'output_volume':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the output_volume command. It should be of the form: output_volume [output] [gain]')
    else:
        serialControl.outputVolume(sys.argv[2], sys.argv[3])
        print("Volume command for output {} sent".format(sys.argv[2]))

#track_volume command
if sys.argv[1] == 'track_volume':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the track_volume command. It should be of the form: track_volume [track] [gain]')
    else:
        serialControl.trackVolume(sys.argv[2], sys.argv[3])
        print("Volume command for track {} sent".format(sys.argv[2]))


#sample_offset command
if sys.argv[1] == 'sample_offset':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the sample_offset command. It should be of the form: sample_offset [output] [offset]')
    else:
        serialControl.sampleRateOffset(sys.argv[2], sys.argv[3])
        print("Offset command for output {} sent".format(sys.argv[2]))


#Play command
if sys.argv[1] == 'play':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the PLAY command. It should be of the form: play [track] [output]')
    else:
        serialControl.controlTrack(int(sys.argv[2]), 'play', int(sys.argv[3]))
        print("Play command for track {} sent".format(sys.argv[2]))

#Pause command
if sys.argv[1] == 'pause':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the PAUSE command. It should be of the form: pause [track] [output]')
    else:
        serialControl.controlTrack(sys.argv[2], 'pause', sys.argv[3])
        print("Pause command for track {} sent".format(sys.argv[2]))

#Load command
if sys.argv[1] == 'load':
    if len(sys.argv) != 4:
        sys.exit('Too many or too few arguments for the LOAD command. It should be of the form: load [track] [output]')
    else:
        serialControl.controlTrack(sys.argv[2], 'load', sys.argv[3])
        print("Load command for track {} onto output {} sent".format(sys.argv[2], sys.argv[3]))


#Fade command
if sys.argv[1] == 'fade':
    if len(sys.argv) != 6:
        sys.exit('Too many or too few arguments for the FADE command. It should be of the form: fade [track] [gain] [time] [stop]')
    else:
        serialControl.trackFade(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        print("Fading track {} {}dB over {} sent".format(sys.argv[2], sys.argv[3], sys.argv[4]))
#Loop command
if sys.argv[1] == 'loop':
    if len(sys.argv) != 5:
        sys.exit('Too many or too few arguments for the LOOP command. It should be of the form: loop [track] [output] [on/off]')
    if sys.argv[5] not in ['on', 'off']:
        sys.exit('Third argument for command LOOP should either be on or off')
    else:
        serialControl.controlTrack(sys.argv[2], ('loop on' if sys.argv[5] == 'on' else 'loop off'), sys.argv[3])
        print("Loop command for track {} onto output {} sent".format(sys.argv[2], sys.argv[3]))


serialControl.closePort()
print("\nClosing connection on {}...".format(interfacePort))
