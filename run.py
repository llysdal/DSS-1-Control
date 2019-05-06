DSS = __import__('dss')
GUI = __import__('control')
midi = __import__('midi')
from time import clock

def delay(time = 0.01):
    t = clock()
    while clock() < t+time:
        pass

#Chose MIDI input and Output
devices = midi.getMidiDevices()

for acc in range(len(devices[0])):
    print(str(list(devices[0].values())[acc]) + ' - ' + list(devices[0].keys())[acc])
i = int(input('Input> '))

print()
for acc in range(len(devices[1])):
    print(str(list(devices[1].values())[acc]) + ' - ' + list(devices[1].keys())[acc])
o = int(input('Output> '))

#Setup DSS1 communication
dss = DSS.DSS(i,o)

#Start GUI
gui = GUI.DSS1gui()

gui.setValues([100, 0, 0, 0, 1, 1, 127, 0, 0, 0, 44, 0, 0, 0, 63, 63, 63, 63, 0, 0, 50, 0, 63, 63, 63, 63, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 4, 20, 20, 500, 0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 12, 0, 4, 1, 1, 0, 0, 3, 18, 0, 0, 3, 1, 0, 7, 0, 1, 3])

    #VCA Kbd Decay might be fucked!
def getParam():
    dss.getParameters(0)

    parList = []
    for i, key in enumerate(dss.param.keys()):
        parList.append(dss.param[key]['v'])

    gui.setValues(parList)


#Keep GUI updated
def updateTask():
    #EG Curves    
    gui.egCanvas(gui.egfc, (gui.egfa, gui.egfd, gui.egfb, gui.egfsl, gui.egfs, gui.egfr))
    gui.egCanvas(gui.egvc, (gui.egva, gui.egvd, gui.egvb, gui.egvsl, gui.egvs, gui.egvr))

    com = gui.execcommand
    if com:
        print('received command')
        if com == 1:
            getParam()

        gui.execCom(0)

    #Control check
    values = gui.getValues()
    for i, key in enumerate(dss.param.keys()):
        if values[i] != dss.param[key]['v']:
            dss.param[key]['v'] = values[i]

            print(key)
            print(dss.param[key])
            print()

    gui.after(10, updateTask)



gui.master.protocol("WM_DELETE_WINDOW", lambda: quit())
updateTask()
gui.master.mainloop()
