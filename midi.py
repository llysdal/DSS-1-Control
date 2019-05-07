from pygame import midi

midi.init()


#Gets all available midi devices, and information about them.
def getMidiDevices():
    midiInputs = {}
    midiOutputs = {}
    
    for deviceNum in range(midi.get_count()):
        n, name, input, output, n = midi.get_device_info(deviceNum)
        
        if input:
            midiInputs[str(name)[2:-1]] = deviceNum
        if output:
            midiOutputs[str(name)[2:-1]] = deviceNum
    
    return midiInputs, midiOutputs

def getDeviceInfo(id):
    print(midi.get_device_info(id))

def getMidiInputDevice(id):
    return midi.Input(id)
    
def getMidiOutputDevice(id):
    return midi.Output(id)
    
def clearMidi(device):
    device.read(1000)

def receiveMidi(device):
    message = device.read(1000)
    return message

def sendMidi(device, status, data1, data2):
    device.write_short(status, data1, data2)

def sendSysex(device, message):  
    device.write_sys_ex(0, bytes(message))
    
def getSysex(device):
    sysex = []
    
    data = receiveMidi(device)
    
    if data == []:
        return False, []
    
    sysexPresent = False
    for i in range(len(data)):
        if data[i][0][0] == 0xF0:
            sysexPresent = True
            sysexId = i
            
    if sysexPresent == False:
        return False, []
        
    for i in range(sysexId, len(data)):
        for u in range(len(data[i][0])):
            sysex.append(data[i][0][u])
            
            if data[i][0][u] == 0xF7:
                return True, sysex
    
    return False, []
    