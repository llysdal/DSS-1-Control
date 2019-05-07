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
print()

#Setup DSS1 communication
dss = DSS.DSS(i,o)

#Attempt communication
if dss.checkCom() == False:
    print('Communication link failed!')
    while True:
        pass
print('Communications established!')

#Get program names
dss.setPlayMode()
dss.getNameList()

#Start GUI
gui = GUI.DSS1gui(titlefont = ('Microgramma D Extended', 16), 
                  textfont  = ('Lucida Sans', 11), 
                  numberfont= ('Lucida Sans', 8))

    #VCA Kbd Decay might be fucked!
def getParams():
    dss.getParameters(int(gui.prog.get())-1)

    parList = []
    for i, key in enumerate(dss.param.keys()):
        parList.append(dss.param[key]['v'])

    gui.progname.delete(0, 100)
    gui.progname.insert(0, dss.namelist[int(gui.prog.get())-1])
    gui.setValues(parList)

def setParams():
    dss.setParameters(gui.progname.get())

def saveProgram():
    dss.saveProgram(int(gui.prog.get())-1)

def updateName():
    dss.getNameList()
    dss.programChange(int(gui.prog.get())-1)
    gui.progname.delete(0, 100)
    gui.progname.insert(0, dss.namelist[int(gui.prog.get())-1])

getParams()

#Keep GUI updated
def updateTask():
    #EG Curves    
    gui.egCanvas(gui.egfc, (gui.egfa, gui.egfd, gui.egfb, gui.egfsl, gui.egfs, gui.egfr))
    gui.egCanvas(gui.egvc, (gui.egva, gui.egvd, gui.egvb, gui.egvsl, gui.egvs, gui.egvr))

    com = gui.execcommand
    if type(com) == str:
        #print('received command')
        if com == 'getparameters':
            getParams()
        if com == 'setparameters':
            setParams()
        if com == 'saveprogram':
            saveProgram()
        if com == 'updatename':
            updateName()

        gui.execCom(0)

    

    #Control check
    values = gui.getValues()
    for i, key in enumerate(dss.param.keys()):
        if values[i] != dss.param[key]['v']:
            dss.param[key]['v'] = values[i]
            dss.setKey(key)

    gui.after(10, updateTask)



gui.master.protocol("WM_DELETE_WINDOW", lambda: quit())
updateTask()
gui.master.mainloop()
