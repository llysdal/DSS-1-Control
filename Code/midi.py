from pygame import midi
t = __import__('tools')

midi.init()

#Gets all available midi devices, and information about them.
def getMidiDevices():
    midiInputs = {}
    midiOutputs = {}

    for deviceNum in range(midi.get_count()):
        n, name, input, output, n = midi.get_device_info(deviceNum)

        if input:
            #Trim the name, getting rid of the byte prefix
            midiInputs[str(name)[2:-1]] = deviceNum
        if output:
            midiOutputs[str(name)[2:-1]] = deviceNum

    return midiInputs, midiOutputs

def getDeviceInfo(id):
    info = midi.get_device_info(id)
    if type(info) == type(None):
        info = 0,0,0,0,0

    return info

def getMidiInputDevice(id):
    return midi.Input(id)

def getMidiOutputDevice(id):
    return midi.Output(id)

def clearMidi(device):
    device.read(1000)

def receiveAllMidi(device):
    message = device.read(1000)
    return message

def receiveMidi(device):
    dataPresent = device.poll()

    if dataPresent:
        message = device.read(1)
        return message
    else:
        return False

def sendMidi(device, status, data1, data2):
    device.write_short(status, data1, data2)

def sendSysex(device, message):
    device.write_sys_ex(0, bytes(message))

def checkSysex(device):
    data = receiveMidi(device)

    if not data:
        return False, data

    if 0xF0 in data[0][0]:
        return True, data
    else:
        return False, data

def getSysex(device):
    ''' Reads a sysex message from the device input.
        Returns it as a tuple with a value for each hexadecimal value (00 to FF)
        Always starts with a 0xF0, and ends with a 0xF7

        If no sysex was found, returns false
        If sysex was found, returns True and the sysex message'''

    for attempt in range(1):
        present, data = checkSysex(device)

        if present:
            break

        t.delay(0.001)

    if not present:
        return False, []

    sysex = list(data[0][0])

    while True:
        data = receiveMidi(device)

        if data == False:
            return False, []

        sysex[len(sysex):len(sysex)] = data[0][0]

        if 0xF7 in data[0][0]:
            return True, sysex[0:sysex.index(0xF7)+1]

        t.delay(0.002)
