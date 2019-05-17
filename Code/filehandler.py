import os
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