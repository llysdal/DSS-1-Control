import os, wave, struct
curDir = os.path.dirname(os.path.abspath(__file__))[0:-4]

def getRessourcePath(name):
    return curDir+'/Ressource/' + name

def getConfig():
    try:
        file = open(curDir+'/config.ini', 'r')
        data = file.read()
        file.close()

        dataSplit = data.split('\n')

        config = {}
        for configuration in dataSplit:
            splitPoint = configuration.index('=')
            if len(configuration) == splitPoint+1:
                config[configuration[0:splitPoint]] = None
            else:
                config[configuration[0:splitPoint]] = configuration[splitPoint+1:]

        return True, config
    except:
        print('FH: Config file not found / wrong format')
        return False, {}

def checkPatch(name):
    try:
        file = open(curDir+'/Patches/'+name, 'r')
        file.close()
        return True
    except:
        print('FH: \'' + name + '\' not found')
        return False

def savePatch(name, data):
    file = open(curDir+'/Patches/'+name, 'w')

    for i in range(len(data)-1):
        file.write(str(data[i]) + '\n')
    file.write(str(data[len(data)-1]))

    file.close()
    print('FH: Saved ' + name + ' successfully')

def loadPatch(name):
    file = open(curDir+'/Patches/'+name, 'r')
    data = file.read()
    file.close()

    dataSplit = data.split('\n')
    dataTreated = []
    for i in range(len(dataSplit)):
        dataTreated.append(int(dataSplit[i]))

    print('FH: Loaded ' + name + ' successfully')
    return dataTreated


def loadWav(loc):
    file = wave.open(loc, 'r')
    data = []
    
    samples = file.getnframes()
    bitwidth = file.getsampwidth() * 8
   
    if bitwidth == 16:
        frames = file.readframes(samples)
        waveData = struct.unpack_from('<%dh' % samples, frames)
    elif bitwidth == 24:
        waveData = []
        for i in range(0, samples-1):
            data = file.readframes(1)
            waveData.append(struct.unpack('<i', data + (b'\0' if data[2] < 128 else b'\xff'))[0])
    else:
        print(f'FH: Unsupported bit width ({bitwidth} bits) for {loc}')

    file.close()

    return bitwidth, waveData

def loadWavNormalize(loc):
    bitwidth, waveData = loadWav(loc)

    return [
        sample / (2 << (bitwidth-2))
        for sample in waveData
    ]