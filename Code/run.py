DSS = __import__('dss')
GUI = __import__('control')
midi = __import__('midi')
fh = __import__('filehandler')
t = __import__('tools')
from time import clock

#Preinit config
configPresent, config = fh.getConfig()

#Handle config
pass

#Chose MIDI input and Output
devices = midi.getMidiDevices()
mIn, mOut = t.chooseDevices(devices, config)

#Setup DSS1 communication
dss = DSS.DSS(mIn, mOut)

#Get start information
dss.setPlayMode()
dss.getNameList()
dss.getMultisoundsList()

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
    fh.savePatch(name, dss.extractParameters())

def loadFile():
    name = gui.progname.get()
    if fh.checkPatch(name):
        dss.putParameters(fh.loadPatch(name))
        dss.setParameters(name)
        

def updateControl():
    #Program list
    gui.progname.delete(0, 100)
    gui.progname.insert(0, dss.namelist[int(gui.prog.get())-1])

    #Parameters
    parList = []
    for i, key in enumerate(dss.param.keys()):
        parList.append(dss.param[key]['v'])

    gui.progname.delete(0, 100)
    gui.progname.insert(0, dss.namelist[int(gui.prog.get())-1])
    gui.setValues(parList)

    #Multisound list - main window
    #Fetch current multisound values
    osc1 = min(gui.oscms.index(gui.osc1w.get()), len(gui.oscms)-1)
    osc2 = min(gui.oscms.index(gui.osc2w.get()), len(gui.oscms)-1)
    #Set new multisound names
    if len(dss.multiName) > 0:
        gui.oscms = dss.multiName
    
    m = gui.osc1wo.children['menu']
    m.delete(0,16)
    for i in range(len(gui.oscms)):
        m.add_command(label=gui.oscms[i], command=lambda value=gui.oscms[i]: gui.osc1w.set(value))

    m = gui.osc2wo.children['menu']
    m.delete(0,16)
    for i in range(len(gui.oscms)):
        m.add_command(label=gui.oscms[i], command=lambda value=gui.oscms[i]: gui.osc2w.set(value))

    #Set values to new option values
    gui.osc1w.set(gui.oscms[osc1])
    gui.osc2w.set(gui.oscms[osc2])

    #Multisound list - multisound window
    gui.mult.multisound.delete(0, 100)
    multiNameGui = dss.multiName.copy()
    while len(multiNameGui) < 16:
        multiNameGui.append('EMPTY')
    for num in range(16):
        gui.mult.multisound.insert(num, multiNameGui[num])

def multisoundOpen():
    dss.getMultisoundsList()
    updateControl()

def getMultisound():
    try:
        msn = gui.mult.multisound.curselection()[0]
        dss.getMultisound(msn)
    except:
        print('A: No multisound selected')

def getPCM():
    dss.getPCM(0, dss.pcmRange)


getParams()
#Startup sysex handling (handle all of the queue)
received = False
while True:
    sysex = midi.getSysex(dss.input)
    if sysex[0]:
        if not received:
            print('A: Communication established!')
            received = True
        dss.decodeSysex(sysex[1])
    else:
        break

if not received:
    print('A: Communications failed!')


def updateTask():
    #EG Curves    
    gui.egUpdate(gui.egfc, (gui.egfat, gui.egfdt, gui.egfslt, gui.egfrt), (gui.egfa, gui.egfd, gui.egfb, gui.egfsl, gui.egfs, gui.egfr))
    gui.egUpdate(gui.egvc, (gui.egvat, gui.egvdt, gui.egvslt, gui.egvrt), (gui.egva, gui.egvd, gui.egvb, gui.egvsl, gui.egvs, gui.egvr))

    #GUI functions - Main
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
        elif com == 'updatecontrol':
            updateControl()
        elif com == 'multiopen':
            multisoundOpen()
        elif com == 'getpcm':
            getPCM()

        gui.execCom(0)

    #GUI functions - Multisound
    com = gui.mult.execcommand
    if type(com) == str:
        if com == 'getmultisound':
            getMultisound()

        gui.mult.execCom(0)

   


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
