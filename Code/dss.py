from time import clock
midi = __import__('midi')
fh = __import__('filehandler')
t = __import__('tools')

exclst = 0b11110000
korgID = 0b01000010
formID = 0b00110000 #Controls the receive channel, configured as 1 here.
dss1ID = 0b00001011

sysexGet = {'mode'          : [0xF0, 0x42, 0x30, 0x0B, 0x12, 0xF7],
            'parameters'    : [0xF0, 0x42, 0x30, 0x0B, 0x10, 'program', 0xF7],
            'programlist'   : [0xF0, 0x42, 0x30, 0x0B, 0x17, 0xF7],
            'multisoundlist': [0xF0, 0x42, 0x30, 0x0B, 0x16, 0xF7]}

sysexSet = {'playmode'      : [0xF0, 0x42, 0x30, 0x0B, 0x13, 0xF7],
            'parameter'     : [0xF0, 0x42, 0x30, 0x0B, 0x41, 'parameter', 'value', 0xF7],
            'parameters'    : [0xF0, 0x42, 0x30, 0x0B, 0x40, 'parameters', 'name', 0xF7],
            'writeprogram'  : [0xF0, 0x42, 0x30, 0x0B, 0x11, 'program', 0xF7]}

class DSS():
    def __init__(self, inputID, outputID):
        self.input  = midi.getMidiInputDevice(inputID)
        self.output = midi.getMidiOutputDevice(outputID)
        
        self.updateGUI = False
        self.debug = True
        #Assume he's in playmode
        self.mode = 0
        #Namelist
        self.namelist = []
        for i in range(32):
            self.namelist.append('NO-COMM')
        #Multisound dictionary
        self.multiAmount = 0
        self.multiName = []
        self.multiLen = []
        #Initial DSS1 parameters
        self.param = {'osc1vol'         :   {'l': 0, 'h': 127, 'v': 100},   #osc 1 mix ratio
                      'osc2vol'         :   {'l': 0, 'h': 127, 'v':   0},   #osc 2 mix ratio
                      'autobendint'     :   {'l': 0, 'h': 127, 'v':   0},   #auto bend intensity
                      'noisevol'        :   {'l': 0, 'h':  63, 'v':   0},   #noise level
                      'vcfmode'         :   {'l': 0, 'h':   1, 'v':   1},   #vcf mode
                      'vcfegpol'        :   {'l': 0, 'h':   1, 'v':   1},   #vcf eg polarity
                      'vcfcutoff'       :   {'l': 0, 'h': 127, 'v': 127},   #vcf cutoff frequency
                      'vcfegint'        :   {'l': 0, 'h':  63, 'v':   0},   #vcf eg intensity
                      'vcfres'          :   {'l': 0, 'h':  63, 'v':   0},   #vcf resonance
                      'vcfkbd'          :   {'l': 0, 'h':  63, 'v':   0},   #vcf keyboard track
                      'vcfmgfreq'       :   {'l': 0, 'h':  63, 'v':  44},   #vcf mg-frequency
                      'vcfmgdelay'      :   {'l': 0, 'h':  63, 'v':   0},   #vcf mg-delay
                      'vcfmgint'        :   {'l': 0, 'h':  63, 'v':   0},   #vcf mg-intensity
                      'vcfega'          :   {'l': 0, 'h':  63, 'v':   0},   #vcf eg attack
                      'vcfegd'          :   {'l': 0, 'h':  63, 'v':  63},   #decay
                      'vcfegb'          :   {'l': 0, 'h':  63, 'v':  63},   #break point
                      'vcfegsl'         :   {'l': 0, 'h':  63, 'v':  63},   #slope
                      'vcfegs'          :   {'l': 0, 'h':  63, 'v':  63},   #sustain
                      'vcfegr'          :   {'l': 0, 'h':  63, 'v':   0},   #release
                      'vcadkbd'         :   {'l': 0, 'h': 127, 'v':   0},   #vca decay keyboard track (val above 63 negative)
                      'vcalevel'        :   {'l': 0, 'h':  63, 'v':  50},   #vca total level
                      'vcaega'          :   {'l': 0, 'h':  63, 'v':   0},   #vca eg attack
                      'vcaegd'          :   {'l': 0, 'h':  63, 'v':  63},   #decay
                      'vcageb'          :   {'l': 0, 'h':  63, 'v':  63},   #break point
                      'vcaegsl'         :   {'l': 0, 'h':  63, 'v':  63},   #slope
                      'vcaegs'          :   {'l': 0, 'h':  63, 'v':  63},   #sustain
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
                      'joypitchrange'   :   {'l': 0, 'h':  12, 'v':   2},   #joystick pitch bend range
                      'joyvcf'          :   {'l': 0, 'h':   1, 'v':   0},   #joystick vcf sweep
                      'eqtreble'        :   {'l': 0, 'h':  12, 'v':   4},   #equalizer treble
                      'eqbass'          :   {'l': 0, 'h':  12, 'v':   4},   #equalizer bass
                      'ddlmgafreq'      :   {'l': 0, 'h':  63, 'v':  20},   #delay mg-a frequency
                      'ddlmgbfreq.'     :   {'l': 0, 'h':  63, 'v':  20},   #delay mg-b frequency
                      'ddl1time'        :   {'l': 0, 'h': 500, 'v': 500},   #delay 1 time
                      'ddl1fb'          :   {'l': 0, 'h':  15, 'v':   0},   #delay 1 feedback
                      'ddl1level'       :   {'l': 0, 'h':  15, 'v':   0},   #delay 1 effect level
                      'ddl1mgaint'      :   {'l': 0, 'h':  63, 'v':   0},   #delay 1 mg a modulation intensity
                      'ddl1mgbint'      :   {'l': 0, 'h':  63, 'v':   0},   #delay 1 mg b modulation intensity
                      'ddl2input'       :   {'l': 0, 'h':   1, 'v':   0},   #delay 2 input select
                      'ddl2time'        :   {'l': 0, 'h': 500, 'v': 500},   #delay 2 time
                      'ddl2fb'          :   {'l': 0, 'h':  15, 'v':   0},   #delay 2 feedback
                      'ddl2level'       :   {'l': 0, 'h':  15, 'v':   0},   #delay 2 effect level
                      'ddl2mgaint'      :   {'l': 0, 'h':  63, 'v':   0},   #delay 2 mg a modulation intensity
                      'ddl2mgbint'      :   {'l': 0, 'h':  63, 'v':   0},   #delay 2 mg b modulation intensity
                      'ddl2modinv'      :   {'l': 0, 'h':   1, 'v':   0},   #delay 2 modulation invertion
                      'osc1ms'          :   {'l': 0, 'h':  15, 'v':   0},   #oscillator 1 multi sound number
                      'osc2ms'          :   {'l': 0, 'h':  15, 'v':   0},   #oscillator 2 multi sound number
                      'oscbendrange'    :   {'l': 0, 'h':  12, 'v':  12},   #do not touch?
                      'sync'            :   {'l': 0, 'h':   1, 'v':   0},   #osc 2 sync
                      'resolution'      :   {'l': 0, 'h':   4, 'v':   4},   #d/a resolution
                      'osc1oct'         :   {'l': 0, 'h':   2, 'v':   1},   #osc 1 octave
                      'osc2oct'         :   {'l': 0, 'h':   2, 'v':   1},   #osc 2 octave
                      'osc2detune'      :   {'l': 0, 'h':  63, 'v':   0},   #osc 2 detune
                      'osc2interval'    :   {'l': 0, 'h':  11, 'v':   0},   #osc 2 interval
                      'oscmgselect'     :   {'l': 0, 'h':   3, 'v':   3},   #modulation select
                      'oscmgfreq'       :   {'l': 0, 'h':  31, 'v':  18},   #osc mod freq
                      'oscmgint'        :   {'l': 0, 'h':  15, 'v':   0},   #osc mod intensity
                      'oscmgdelay'      :   {'l': 0, 'h':  15, 'v':   0},   #osc mod delay
                      'autobendselect'  :   {'l': 0, 'h':   3, 'v':   3},   #auto bend select
                      'autobendpol'     :   {'l': 0, 'h':   1, 'v':   1},   #auto bend polarity
                      'autobendtime'    :   {'l': 0, 'h':  31, 'v':   0},   #auto bend time
                      'unisondetune'    :   {'l': 0, 'h':   7, 'v':   7},   #unison detune
                      'veloscchange'    :   {'l': 0, 'h':  31, 'v':   0},   #???
                      'assign'          :   {'l': 0, 'h':   2, 'v':   1},   #poly2, poly1, unison
                      'unisonvoices'    :   {'l': 0, 'h':   3, 'v':   3}}   #amount of unison voices

    def decodeSysex(self, sysex):
        #Check if the sysex message is for us.
        if sysex[0:4] == [exclst, korgID, formID, dss1ID]:
            if sysex[4] == 0x42:
                #Mode Data
                if self.debug: print('R: Mode data')
                self.mode = sysex[5]

            elif sysex[4] == 0x45:
                #Multi Sound List
                if self.debug: print('R: Multi sound name list')
                self.multiLen = []
                self.multiName = []

                #Assigning data
                self.multiAmount = sysex[5]
                
                for i in range(self.multiAmount):
                    self.multiName.append(''.join(map(chr, sysex[6+14*i:6+14*i+8])))
                    lenSum = 0
                    for u in range(6):
                        lenSum = sysex[6+14*i+8:6+14*i+14][5-u] * 2**u
                    self.multiLen.append(lenSum)
                
                self.updateGUI = True

            elif sysex[4] == 0x44:
                #Multi Sound Parameter Dump
                if self.debug: print('R: Multi sound parameters')
                pass

            elif sysex[4] == 0x43:
                #PCM Data Dump
                if self.debug: print('R: PCM data dump')
                pass

            elif sysex[4] == 0x46:
                #Program Name List
                if self.debug: print('R: Program name list')
                for i in range(32):
                    self.namelist[i] = ''.join(map(chr, sysex[5+8*i:5+8*i+8]))
                    
                self.updateGUI = True

            elif sysex[4] == 0x40:
                #Program Parameter Dump
                if self.debug: print('R: Program parameters')

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
                
                self.updateGUI = True

            elif sysex[4] == 0x23:
                #Data Load Completed
                if self.debug: print('R: Data load complete')
                pass

            elif sysex[4] == 0x24:
                #Data Load Error
                if self.debug: print('R: Data load error')
                pass

            elif sysex[4] == 0x21:
                #Write Completed
                if self.debug: print('R: Write complete')
                pass

            elif sysex[4] == 0x22:
                #Write Error
                if self.debug: print('R: Write error')
                pass


    def getMode(self):
        midi.sendSysex(self.output, sysexGet['mode'])

    def setPlayMode(self):
        if self.debug: print('T: Set mode to playmode')
        midi.sendSysex(self.output, sysexSet['playmode'])

    def programChange(self, program):
        if self.debug: print('T: Changing program to '+ str(program+1))
        midi.sendMidi(self.output, 192, program, 0)
        self.updateGUI = True

    def getNameList(self):
        if self.debug: print('T: Get program name list')
        midi.sendSysex(self.output, sysexGet['programlist'])

    def getMultisoundsList(self):
        if self.debug: print('T: Get multi sound list')
        midi.sendSysex(self.output, sysexGet['multisoundlist'])         

    def getParameters(self, program):
        if self.debug: print('T: Get all parameters from program ' + str(program+1))
        #Getting the sysex command
        sysex = sysexGet['parameters'].copy()

        #Replacing the pointer with the program
        sysex[sysex.index('program')] = program

        #Sending the sysex request to the DSS-1
        midi.sendSysex(self.output, sysex)

    def setParameter(self, parameter, value):
        if self.debug: print('T: Set parameter ' + str(parameter) + ' to ' + str(value))
        #Get sysex command
        sysex = sysexSet['parameter'].copy()

        #Replacing pointers
        sysex[sysex.index('parameter')] = parameter

        valueIndex = sysex.index('value')

        if parameter == 46 or parameter == 52:
            sysex[valueIndex] = value//128
            sysex.insert(valueIndex, value%128)
        else:
            sysex[valueIndex] = value
    
        midi.sendSysex(self.output, sysex)

    def setKey(self, key):
        parNum = list(self.param.keys()).index(key)
        parVal = self.param[key]['v']

        self.setParameter(parNum, parVal)
        
    def setParameters(self, name):
        if self.debug: print('T: Set all parameters and send the name \"' + name + '\"')
        while len(name) < 8:
            name += ' '
        nameList = list(map(ord, name[0:8]))

        #Get all parameter values
        parameterList = [par['v'] for par in self.param.values()]
        
        #Treat the 2 delay times (address 46 and 52)
        dh, dl = parameterList[46]//128, parameterList[46]%128
        parameterList[46] = dl
        parameterList.insert(47, dh)
        #53 here, we inserted an additional value
        dh, dl = parameterList[53]//128, parameterList[53]%128
        parameterList[53] = dl
        parameterList.insert(54, dh)

        #Insert these 2 lists into the sysex
        sysex = sysexSet['parameters'].copy()
        parIndex = sysex.index('parameters')
        sysex[parIndex:parIndex+1] = parameterList
        nameIndex = sysex.index('name')
        sysex[nameIndex:nameIndex+1] = nameList

        #Send the finalized sysex patch
        midi.sendSysex(self.output, sysex)

    def saveProgram(self, program):
        if self.debug: print('T: Save program as program ' + str(program+1))
        #Getting the sysex command
        sysex = sysexSet['writeprogram'].copy()

        #Replacing the pointer with the program
        sysex[sysex.index('program')] = program

        midi.sendSysex(self.output, sysex)


    #Save parameters to file
    def saveParameters(self, name):
        parList = []
        for key in self.param.keys():
            parList.append(self.param[key]['v'])

        fh.saveFile(name, parList)

    #Load parameters to file
    def loadParameters(self, name):
        parList = fh.loadFile(name)

        for i, key in enumerate(self.param.keys()):
            self.param[key]['v'] = parList[i]

        self.updateGUI = True
