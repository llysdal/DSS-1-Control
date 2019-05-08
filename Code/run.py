DSS = __import__('dss')
GUI = __import__('control')
midi = __import__('midi')
fh = __import__('filehandler')
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
    if not dss.getParameters(int(gui.prog.get())-1):
        print('Couldn\'t get parameters')

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

def saveFile():
    name = gui.progname.get()
    dss.saveParameters(name)
    print('Saved ' + name + ' successfully')

def loadFile():
    name = gui.progname.get()
    if fh.checkFile(name):
        dss.loadParameters(name)
        print('Loaded ' + name + ' successfully')

        parList = []
        for key in dss.param.keys():
            parList.append(dss.param[key]['v'])
        gui.setValues(parList)
    else:
        print('\'' + name + '\' not found')


getParams()


def updateTask():
    #EG Curves    
    gui.egUpdate(gui.egfc, (gui.egfa, gui.egfd, gui.egfb, gui.egfsl, gui.egfs, gui.egfr))
    gui.egUpdate(gui.egvc, (gui.egva, gui.egvd, gui.egvb, gui.egvsl, gui.egvs, gui.egvr))

    #GUI functions
    com = gui.execcommand
    if type(com) == str:
        #print('received command')
        if com == 'getparameters':
            getParams()
        elif com == 'setparameters':
            setParams()
        elif com == 'saveprogram':
            saveProgram()
        elif com == 'updatename':
            updateName()
        elif com == 'savefile':
            saveFile()
        elif com == 'loadfile':
            loadFile()

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
