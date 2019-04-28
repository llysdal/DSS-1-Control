from time import clock
midi = __import__('midi')


print(midi.getMidiDevices())


korgID = 0b01000010
format = 0b00110000
dss1ID = 0b00001011

sysexGet = {'mode'      : b'\xF0\x42\x30\x0B\x12\xF7',
            'parameters': b'\xF0\x42\x30\x0B\x10\xaa\xF7'}

sysexSet = {'playmode': b'\xF0\x42\x30\x0B\x13\xF7'}


class DSS():
    def __init__(self, inputID, outputID):
        self.input  = midi.getMidiInputDevice(inputID)
        self.output = midi.getMidiOutputDevice(outputID)
        
        #Assume he's in playmode
        self.mode = 0
        #Initial DSS1 parameters
        self.param = {'osc 1 mix ratio'     : 100,
                      'osc 2 mix ratio'     :   0,
                      'auto bend intensity' :   0,
                      'noise level'         :   0,
                      'vcf mode'            :   1,
                      'vcf eg polarity'     :   1,
                      'vcf cutoff'          : 127,
                      'vcf eg intensity'    :   0,
                      'vcf resonance'       :   0,
                      'vcf kbdtrack'        :   0,
                      'vcf mg-frequency'    :  44,
                      'vcf mg-delay'        :   0,
                      'vcf mg-intensity'    :   0,
                      'vcf eg-attack'       :   0,
                      'vcf eg-decay'        :  63,
                      'vcf eg-break point'  :  63,
                      'vcf eg-slope'        :  63,
                      'vcf eg-sustain'      :  63,
                      'vcf eg-release'      :   0,
                      'vca decay kbdtrack'  :   0,
                      'vca total level'     :  50,
                      'vca eg-attack'       :   0,
                      'vca eg-decay'        :  63,
                      'vca eg-break point'  :  63,
                      'vca eg-slope'        :  63,
                      'vca eg-sustain'      :  63,
                      'vca eg-release'      :   0,
                      'vel. sens.- a. bend intensity'   :   0,
                      'vel. sens.- vcf cutoff'          :   0,
                      'vel. sens.- vcf eg attack'       :   0,
                      'vel. sens.- vcf eg decay'        :   0,
                      'vel. sens.- vcf eg slope'        :   0,
                      'vel. sens.- vca eg level'        :   0,
                      'vel. sens.- vca eg attack'       :   0,
                      'vel. sens.- vca eg decay'        :   0,
                      'vel. sens.- vca eg slope'        :   0,
                      'aft. touch- osc mg intensity'    :   0,
                      'aft. touch- vcf (mg/cutoff)'     :   0,
                      'aft. touch- vcf parameter slot.' :   0,
                      'aft. touch- vca level'           :   0,
                      'joystick pitch bend range'       :   2,
                      'joystick vcf sweep'              :   0,
                      'equalizer treble'    :   4,
                      'equalizer bass'      :   4,
                      'ddl mg-a freq.'      :  20,
                      'ddl mg-b freq.'      :  20,
                      'ddl-1 time low'      :  72,
                      'ddl-1 time high'     :   1,  #!!
                      'ddl-1 feedback'      :   0,
                      'ddl-1 effect level'  :   0,
                      'ddl-1 mg-a intensity':   0,
                      'ddl-1 mg-b intensity':   0,
                      'ddl-2 input select'  :   0,
                      'ddl-2 time low'      :  72,
                      'ddl-2 time high'     :   1,  #!!
                      'ddl-2 feedback'      :   0,
                      'ddl-2 effect level'  :   0,
                      'ddl-2 mg-a intensity':   0,
                      'ddl-2 mg-b intensity':   0,
                      'ddl-2 mod. invert sw':   0,
                      'osc 1 multi sound no.'           :   0,
                      'osc 2 multi sound no.'           :   0,
                      'max osc bend range'  :   6,
                      'sync mode sw'        :   0,
                      'd a resolution'      :   4,
                      'osc 1 octave'        :   1,
                      'osc 2 octave'        :   1,
                      'osc 2 detune'        :   0,
                      'osc 2 interval'      :   0,
                      'osc mg select'       :   3,
                      'osc mg-frequency'    :  18,
                      'osc mg-intensity'    :   0,
                      'osc mg-delay'        :   0,
                      'auto bend select'    :   3,
                      'auto bend-polarity'  :   1,
                      'auto bend-time'      :   0,
                      'unison detune'       :   7,
                      'vel. sens.- osc change'          :   0,
                      'key assign mode'     :   1,
                      'unison voices'       :   3}

    #Gets the current mode
    def getMode(self):
        midi.sendSysex(self.output, sysexGet['mode'])
        received, sysex = midi.getSysex(self.input)
        if received:
            if sysex[1] != korgID:
                return
            if sysex[3] != dss1ID:
                return
          
            self.mode = sysex[5]
    
    #Sets the mode to playmode
    def setPlayMode(self):
        midi.sendSysex(self.output, sysexSet['playmode'])
        
    #Not realtime. Can only get parameters saved in memory
    def getParameters(self, program):
        programByte = bytes([program])
        sysex = sysexGet['parameters'].replace(b'\xaa',programByte)
        
        midi.sendSysex(self.output, sysex)
        
        received, sysex = midi.getSysex(self.input)
        
        if received:
            #Check to see if we received the right stuff
            if sysex[1] != korgID:
                return
            if sysex[3] != dss1ID:
                return
            
            for i, key in enumerate(self.param.keys()):
                self.param[key] = sysex[5:-1][i]
        
      
dss = DSS(2,5)


while True:
    t = clock()
    
    dss.getParameters(0)
    
    print(dss.param)
    
    while clock() < t + 1:
        pass
    