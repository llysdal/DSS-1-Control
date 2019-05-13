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
root = GUI.tk.Tk()
gui = GUI.DSS1main(root,
                  titlefont = ('Microgramma D Extended', 16), 
                  textfont  = ('Lucida Sans', 11), 
                  numberfont= ('Lucida Sans', 8))




#GUI functions
def getParams():
    dss.getParameters(int(gui.prog.get())-1)

def setParams():
    dss.setParameters(gui.progname.get())

def saveProgram():
    dss.saveProgram(int(gui.prog.get())-1)
    dss.getNameList()

def changeProgram():
    dss.programChange(int(gui.prog.get())-1)

    if gui.autoget.get():
        getParams()

def saveFile():
    name = gui.progname.get()
    dss.saveParameters(name)
    print('Saved ' + name + ' successfully')

def loadFile():
    name = gui.progname.get()
    if fh.checkFile(name):
        dss.loadParameters(name)
        print('Loaded ' + name + ' successfully')
    else:
        print('\'' + name + '\' not found')

def updateControl():
    #Program name
    gui.progname.delete(0, 100)
    gui.progname.insert(0, dss.namelist[int(gui.prog.get())-1])

    #Parameters
    parList = []
    for i, key in enumerate(dss.param.keys()):
        parList.append(dss.param[key]['v'])

    gui.progname.delete(0, 100)
    gui.progname.insert(0, dss.namelist[int(gui.prog.get())-1])
    gui.setValues(parList)

getParams()

#Startup sysex handling (handle all of the queue)
while True:
    sysex = midi.getSysex(dss.input)
    if sysex[0]:
        dss.decodeSysex(sysex[1])
    else:
        break


def updateTask():
    #EG Curves    
    gui.egUpdate(gui.egfc, (gui.egfat, gui.egfdt, gui.egfslt, gui.egfrt), (gui.egfa, gui.egfd, gui.egfb, gui.egfsl, gui.egfs, gui.egfr))
    gui.egUpdate(gui.egvc, (gui.egvat, gui.egvdt, gui.egvslt, gui.egvrt), (gui.egva, gui.egvd, gui.egvb, gui.egvsl, gui.egvs, gui.egvr))

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
        elif com == 'changeprogram':
            changeProgram()
        elif com == 'savefile':
            saveFile()
        elif com == 'loadfile':
            loadFile()

        gui.execCom(0)

   


    #Check for sysex messages
    sysex = midi.getSysex(dss.input)
    if sysex[0]:
        dss.decodeSysex(sysex[1])

    if dss.updateGUI:
        updateControl()
        dss.updateGUI = False

    #Control check
    values = gui.getValues()
    for i, key in enumerate(dss.param.keys()):
        if values[i] != dss.param[key]['v']:
            dss.param[key]['v'] = values[i]
            dss.setKey(key)

    gui.frame.after(50, updateTask)



root.protocol("WM_DELETE_WINDOW", lambda: quit())
updateTask()
root.mainloop()
