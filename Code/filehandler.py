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
            if configuration[0] == '#': continue
            splitPoint = configuration.index('=')
            if len(configuration) == splitPoint+1:
                config[configuration[0:splitPoint]] = None
            else:
                config[configuration[0:splitPoint]] = configuration[splitPoint+1:]

        return True, config
    except:
        print('Config file not found / wrong format - using defaults')
        return False, {}


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
        print(f'Unsupported bit width ({bitwidth} bits) for {loc}, cancelling')

    file.close()

    return bitwidth, waveData

def loadWavNormalize(loc):
    bitwidth, waveData = loadWav(loc)

    return [
        sample / (2 << (bitwidth-2))
        for sample in waveData
    ]