from time import clock
midi = __import__('midi')


print(midi.getMidiDevices())


korgID = 0b01000010
format = 0b00110000
dss1ID = 0b00001011

sysexGet = {'mode'       : [0xF0, 0x42, 0x30, 0x0B, 0x12, 0xF7],
            'parameters' : [0xF0, 0x42, 0x30, 0x0B, 0x10, 'program', 0xF7],
            'programlist': [0xF0, 0x42, 0x30, 0x0B, 0x17, 0xF7]}

sysexSet = {'playmode': [0xF0, 0x42, 0x30, 0x0B, 0x13, 0xF7],
            'parameter': [0xF0, 0x42, 0x30, 0x0B, 0x41, 'parameter', 'value', 0xF7],
            'parameters': [0xF0, 0x42, 0x30, 0x0B, 0x40, 'parameters', 'name', 0xF7]}


class DSS():
    def __init__(self, inputID, outputID):
        self.input  = midi.getMidiInputDevice(inputID)
        self.output = midi.getMidiOutputDevice(outputID)
        
        #Assume he's in playmode
        self.mode = 0
        #Namelist
        self.namelist = []
        for i in range(32):
            self.namelist.append(str(i))
        #Initial DSS1 parameters
        self.param = {'osc1vol'         :   {'l': 0, 'h': 127, 'v':   0},   #osc 1 mix ratio
                      'osc2vol'         :   {'l': 0, 'h': 127, 'v':   0},   #osc 2 mix ratio
                      'autobendint'     :   {'l': 0, 'h': 127, 'v':   0},   #auto bend intensity
                      'noisevol'        :   {'l': 0, 'h':  63, 'v':   0},   #noise level
                      'vcfmode'         :   {'l': 0, 'h':   1, 'v':   0},   #vcf mode
                      'vcfegpol'        :   {'l': 0, 'h':   1, 'v':   0},   #vcf eg polarity
                      'vcfcutoff'       :   {'l': 0, 'h': 127, 'v':   0},   #vcf cutoff frequency
                      'vcfegint'        :   {'l': 0, 'h':  63, 'v':   0},   #vcf eg intensity
                      'vcfres'          :   {'l': 0, 'h':  63, 'v':   0},   #vcf resonance
                      'vcfkbd'          :   {'l': 0, 'h':  63, 'v':   0},   #vcf keyboard track
                      'vcfmgfreq'       :   {'l': 0, 'h':  63, 'v':   0},   #vcf mg-frequency
                      'vcfmgdelay'      :   {'l': 0, 'h':  63, 'v':   0},   #vcf mg-delay
                      'vcfmgint'        :   {'l': 0, 'h':  63, 'v':   0},   #vcf mg-intensity
                      'vcfega'          :   {'l': 0, 'h':  63, 'v':   0},   #vcf eg attack
                      'vcfegd'          :   {'l': 0, 'h':  63, 'v':   0},   #decay
                      'vcfegb'          :   {'l': 0, 'h':  63, 'v':   0},   #break point
                      'vcfegsl'         :   {'l': 0, 'h':  63, 'v':   0},   #slope
                      'vcfegs'          :   {'l': 0, 'h':  63, 'v':   0},   #sustain
                      'vcfegr'          :   {'l': 0, 'h':  63, 'v':   0},   #release
                      'vcadkbd'         :   {'l': 0, 'h': 127, 'v':   0},   #vca decay keyboard track (val above 63 negative)
                      'vcalevel'        :   {'l': 0, 'h':  63, 'v':   0},   #vca total level
                      'vcaega'          :   {'l': 0, 'h':  63, 'v':   0},   #vca eg attack
                      'vcaegd'          :   {'l': 0, 'h':  63, 'v':   0},   #decay
                      'vcageb'          :   {'l': 0, 'h':  63, 'v':   0},   #break point
                      'vcaegsl'         :   {'l': 0, 'h':  63, 'v':   0},   #slope
                      'vcaegs'          :   {'l': 0, 'h':  63, 'v':   0},   #sustain
                      'vcaegr'          :   {'l': 0, 'h':  63, 'v':   0},   #release
                      'vel-autobendint' :   {'l': 0, 'h':  63, 'v':   0},   #velocity sensitive auto bend intensity
                      'vel-vcfcutoff'   :   {'l': 0, 'h':  63, 'v':   0},   #cutoff
                      'vel-vcfega'      :   {'l': 0, 'h':  63, 'v':   0},   #vcf eg attack
                      'vel-vcfegd'      :   {'l': 0, 'h':  63, 'v':   0},   #vcf eg decay
                      'vel-vcfegsl'     :   {'l': 0, 'h':  63, 'v':   0},   #vcf eg slope
                      'vel-vcaeglevel'  :   {'l': 0, 'h':  63, 'v':   0},   #vca eg level
                      'vel-vcaega'      :   {'l': 0, 'h':  63, 'v':   0},   #vca eg attack
                      'vel-vcaegd'      :   {'l': 0, 'h':  63, 'v':   0},   #vca eg decay
                      'vel-vcaegsl'     :   {'l': 0, 'h':  63, 'v':   0},   #vca eg slope
                      'aft-oscmgint'    :   {'l': 0, 'h':  15, 'v':   0},   #after touch oscillator mg intensity
                      'aft-vcfmod'      :   {'l': 0, 'h':  15, 'v':   0},   #vcf mod (cutoff / mg)
                      'aft-vcfpar.'     :   {'l': 0, 'h':   1, 'v':   0},   #vcf mod slot
                      'aft-vcalevel'    :   {'l': 0, 'h':  15, 'v':   0},   #vca level
                      'joypitchrange'   :   {'l': 0, 'h':  12, 'v':   0},   #joystick pitch bend range
                      'joyvcf'          :   {'l': 0, 'h':   1, 'v':   0},   #joystick vcf sweep
                      'eqtreble'        :   {'l': 0, 'h':  12, 'v':   0},   #equalizer treble
                      'eqbass'          :   {'l': 0, 'h':  12, 'v':   0},   #equalizer bass
                      'ddlmgafreq'      :   {'l': 0, 'h':  63, 'v':   0},   #delay mg-a frequency
                      'ddlmgbfreq.'     :   {'l': 0, 'h':  63, 'v':   0},   #delay mg-b frequency
                      'ddl1time'        :   {'l': 0, 'h': 500, 'v':   0},   #delay 1 time
                      'ddl1fb'          :   {'l': 0, 'h':  15, 'v':   0},   #delay 1 feedback
                      'ddl1level'       :   {'l': 0, 'h':  15, 'v':   0},   #delay 1 effect level
                      'ddl1mgaint'      :   {'l': 0, 'h':  63, 'v':   0},   #delay 1 mg a modulation intensity
                      'ddl1mgbint'      :   {'l': 0, 'h':  63, 'v':   0},   #delay 1 mg b modulation intensity
                      'ddl2input'       :   {'l': 0, 'h':   1, 'v':   0},   #delay 2 input select
                      'ddl2time'        :   {'l': 0, 'h': 500, 'v':   0},   #delay 2 time
                      'ddl2fb'          :   {'l': 0, 'h':  15, 'v':   0},   #delay 2 feedback
                      'ddl2level'       :   {'l': 0, 'h':  15, 'v':   0},   #delay 2 effect level
                      'ddl2mgaint'      :   {'l': 0, 'h':  63, 'v':   0},   #delay 2 mg a modulation intensity
                      'ddl2mgbint'      :   {'l': 0, 'h':  63, 'v':   0},   #delay 2 mg b modulation intensity
                      'ddl2modinv'      :   {'l': 0, 'h':   1, 'v':   0},   #delay 2 modulation invertion
                      'osc1ms'          :   {'l': 0, 'h':  15, 'v':   0},   #oscillator 1 multi sound number
                      'osc2ms'          :   {'l': 0, 'h':  15, 'v':   0},   #oscillator 2 multi sound number
                      'oscbendrange'    :   {'l': 0, 'h':  12, 'v':   0},   #do not touch?
                      'sync'            :   {'l': 0, 'h':   1, 'v':   0},   #osc 2 sync
                      'resolution'      :   {'l': 0, 'h':   4, 'v':   0},   #d/a resolution
                      'osc1oct'         :   {'l': 0, 'h':   2, 'v':   0},   #osc 1 octave
                      'osc2oct'         :   {'l': 0, 'h':   2, 'v':   0},   #osc 2 octave
                      'osc2detune'      :   {'l': 0, 'h':  63, 'v':   0},   #osc 2 detune
                      'osc2interval'    :   {'l': 0, 'h':  11, 'v':   0},   #osc 2 interval
                      'oscmgselect'     :   {'l': 0, 'h':   3, 'v':   0},   #modulation select
                      'oscmgfreq'       :   {'l': 0, 'h':  31, 'v':   0},   #osc mod freq
                      'oscmgint'        :   {'l': 0, 'h':  15, 'v':   0},   #osc mod intensity
                      'oscmgdelay'      :   {'l': 0, 'h':  15, 'v':   0},   #osc mod delay
                      'autobendselect'  :   {'l': 0, 'h':   3, 'v':   0},   #auto bend select
                      'autobendpol'     :   {'l': 0, 'h':   1, 'v':   0},   #auto bend polarity
                      'autobendtime'    :   {'l': 0, 'h':  31, 'v':   0},   #auto bend time
                      'unisondetune'    :   {'l': 0, 'h':   7, 'v':   0},   #unison detune
                      'veloscchange'    :   {'l': 0, 'h':  31, 'v':   0},   #???
                      'assign'          :   {'l': 0, 'h':   2, 'v':   0},   #poly2, poly1, unison
                      'unisonvoices'    :   {'l': 0, 'h':   3, 'v':   0}}   #amount of unison voices

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

    #Gets the program names on the synth
    def getNameList(self):
        midi.sendSysex(self.output, sysexGet['programlist'])
        recieved, sysex = midi.getSysex(self.input)

        if recieved:
            #Validity check
            if sysex[0:5] == [0xF0, 0x42, 0x30, 0x0B, 0x46]:
                #Names recieved, put them in self.namelist
                for i in range(32):
                    self.namelist[i] = ''.join(map(chr, sysex[5+8*i:5+8*i+8]))

    #Not realtime. Can only get parameters saved in memory
    def getParameters(self, program):
        #Getting the sysex command
        sysex = sysexGet['parameters'].copy()

        #Replacing the pointer with the program
        sysex[sysex.index('program')] = program

        #Sending the sysex request to the DSS-1
        midi.sendSysex(self.output, sysex)
        
        #Seeing if we recieved the message, and putting it in sysex
        received, sysex = midi.getSysex(self.input)

        if received:
            #Check to see if we received the right stuff
            if sysex[0:5] == [0xF0, 0x42, 0x30, 0x0B, 0x40]:
                
                sysex = sysex[5:-1]
                #Replace the stored parameters with the sysex gotten ones
                for i, key in enumerate(self.param.keys()):
                    if i != 46 and i != 52:
                        self.param[key]['v'] = sysex[0]
                        sysex.pop(0)
                    else:
                        #Special case for the delay times, where instead of 1 byte we receive 2 bytes.
                        self.param[key]['v'] = sysex[0] + sysex[1]*128
                        sysex.pop(0)
                        sysex.pop(0)

    #Sets the parameters to the ones in the controller, and assigns it a name
    def setParameters(self, program):
        midi.sendSysex(self.output, sysexSet['writeprogram'])

    def setParameter(self, parameter, value):
        #Get sysex command
        sysex = sysexSet['parameter'].copy()

        #Replacing pointers
        sysex[sysex.index('parameter')] = parameter

        valueIndex = sysex.index('value')

        if parameter == 46 or parameter == 52:
            sysex[valueIndex] = value%127
            sysex.insert(valueIndex, value//127)
        else:
            sysex[valueIndex] = value
        
            

        #Sending the sysex request to the DSS-1
        midi.sendSysex(self.output, sysex)

        
        

    '''
    def setParameters(self):
        parameterBytes = list(self.param.values())
        nameBytes = [0,0,0,0,0,0,0,0]

        print(list(self.param.values()))
        print(parameterBytes)

        sysex = sysexSet['parameters'].replace(b'\xaa', parameterBytes).replace(b'\xbb', nameBytes)
        
        

        #print(sysex)

        midi.sendSysex(self.output, sysex)
    '''
      
dss = DSS(1,4)

iter = 0
while True:
    iter += 5
    t = clock()
    
    #print(dss.namelist)

    #dss.getNameList()

    dss.getParameters(0)
    
    print(dss.param)
    
    while clock() < t + 0.1:
        pass
    