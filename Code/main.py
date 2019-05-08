DSS = __import__('dss')
GUI = __import__('control')
midi = __import__('midi')
t = __import__('tools')

#Chose MIDI input and Output
devices = midi.getMidiDevices()

i, o = t.chooseDevices(devices)


#Setup DSS1 communication
dss = DSS.DSS(i,o)

#Attempt communication
t.comCheck(dss)

#Get program names
dss.setPlayMode()
dss.getNameList()

#Start GUI
gui = GUI.DSS1gui(titlefont = ('Microgramma D Extended', 16), 
                  textfont  = ('Lucida Sans', 11), 
                  numberfont= ('Lucida Sans', 8))


#GUI functions
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


def updateTask():
    #EG Curves    
    gui.egCanvas(gui.egfc, (gui.egfa, gui.egfd, gui.egfb, gui.egfsl, gui.egfs, gui.egfr))
    gui.egCanvas(gui.egvc, (gui.egva, gui.egvd, gui.egvb, gui.egvsl, gui.egvs, gui.egvr))

    #GUI functions
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
