midi = __import__('midi')
from time import clock


def delay(time = 0.1):
    t = clock()
    while clock() < t+time:
        pass

def chooseDevices(devices):
    valid = False
    while not valid:
        for acc in range(len(devices[0])):
            print(str(list(devices[0].values())[acc]) + ' - ' + list(devices[0].keys())[acc])
        try:
            i = int(input('Input> '))
        except:
            print('Invalid ID\n')
            continue

        if midi.getDeviceInfo(i)[2]:
            valid = True
            print()
            break
        print('Invalid ID\n')

    valid = False
    while not valid:
        for acc in range(len(devices[1])):
            print(str(list(devices[1].values())[acc]) + ' - ' + list(devices[1].keys())[acc])
        try:
            o = int(input('Output> '))
        except:
            print('Invalid ID\n')
            continue

        if midi.getDeviceInfo(o)[3]:
            valid = True
            print()
            break
        print('Invalid ID\n')

    return i, o 

def comCheck(dss):
    if dss.getMode() == False:
        print('Communication link failed!\n')
    else:
        print('Communications established!\n')