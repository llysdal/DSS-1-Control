import os
curDir = os.path.dirname(os.path.abspath(__file__))[0:-4]

def getRessourcePath(name):
    return curDir+'/Ressource/' + name

def checkFile(name):
    try: 
        file = open(curDir+'/Patches/'+name, 'r')
        file.close()
        return True
    except:
        return False

def saveFile(name, data):
    file = open(curDir+'/Patches/'+name, 'w')

    for i in range(len(data)-1):
        file.write(str(data[i]) + '\n')
    file.write(str(data[len(data)-1]))

    file.close()

def loadFile(name):
    file = open(curDir+'/Patches/'+name, 'r')
    data = file.read()
    file.close()

    dataSplit = data.split('\n')
    dataTreated = []
    for i in range(len(dataSplit)):
        dataTreated.append(int(dataSplit[i]))

    return dataTreated