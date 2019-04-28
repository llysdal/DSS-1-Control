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


def getMidiInputDevice(id):
    return midi.Input(id)
    
def getMidiOutputDevice(id):
    return midi.Output(id)
    
    
def receiveMidi(device):
    message = device.read(100)
    return message

    
def sendSysex(device, message):  
    device.write_sys_ex(0, message)
    
def getSysex(device):
    sysex = []
    
    data = receiveMidi(device)
    
    if data == []:
        return False, []
    
    sysexPresent = False
    for i in range(len(data)):
        if data[i][0][0] == 240:
            sysexPresent = True
            sysexId = i
            
    if sysexPresent == False:
        return False, []
        
    for i in range(sysexId, len(data)):
        for u in range(len(data[i][0])):
            sysex.append(data[i][0][u])
            
            if data[i][0][u] == 247:
                return True, sysex
    
    return False, []
    
'''
print(getMidiDevices())

dIn  = getMidiInputDevice(2)
dOut = getMidiOutputDevice(5)

#[0xF0,0x42,0x30,0x0B,0x40,0x00,0xF7]
#mesg = [chr(0xF0), chr(0x42), chr(0x30), chr(0x0B), chr(0x40), chr(0x01), chr(0xF7)]
#mesg = b"\xF0\x42\x30\x0B\x40\x00\xF7"
mesg = b'\xF0\x42\x30\x0B\x12\xF7'

sendSysex(dOut, mesg)

while True:
    input('')
    
    receiveMidi(dIn)
'''