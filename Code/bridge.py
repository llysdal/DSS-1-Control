DSS = __import__('dss')
GUI = __import__('control')
midi = __import__('midi')
fh = __import__('filehandler')
t = __import__('tools')
grapher = __import__('grapher')


#GUI functions
def getParams(dss, gui):
    dss.getParameters(int(gui.prog.get())-1)

def setParams(dss, gui):
    dss.setParameters(gui.progname.get())

def saveProgram(dss, gui):
    dss.saveProgram(int(gui.prog.get())-1)
    dss.getNameList()

def changeProgram(dss, gui):
    dss.programChange(int(gui.prog.get())-1)

    if gui.autoget.get():
        getParams(dss, gui)

def saveFile(dss, gui):
    name = gui.progname.get()
    fh.savePatch(name, dss.extractParameters())

def loadFile(dss, gui):
    name = gui.progname.get()
    if fh.checkPatch(name):
        dss.putParameters(fh.loadPatch(name))
        dss.setParameters(name)


def updateControl(dss, gui):
    #Program list
    gui.progname.delete(0, 100)
    gui.progname.insert(0, dss.namelist[int(gui.prog.get())-1])

    #Parameters
    parList = dss.extractParameters()
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

    #Multisound values
    multParList = dss.extractMultisoundParameters()
    gui.mult.setValues(multParList)


def multisoundOpen(dss, gui):
    pass
    # updateControl(dss, gui)

def getMultisound(dss, gui):
    try:
        msn = gui.mult.multisound.curselection()[0]
        dss.getMultisound(msn)
    except:
        print('A: No multisound selected')

def setMultisound(dss, gui):
    progno = gui.mult.multisound.curselection()
    
    if len(progno) < 1: 
        print('A: No multisound slot selected')
        return
    progno = progno[0]
    
    if progno >= dss.multiAmount: progno = dss.multiAmount
    
    msn = gui.mult.getValues()
    dss.setMultisound(progno, msn)
    dss.setMultisoundsListAfterMultisoundSet(progno, msn)
    dss.getMultisoundsList()
    getMultisound(dss, gui)

def getPCM(dss, gui):
    dss.getPCM(0, 4096)
    
def setPCM(dss, gui):
    # wave = fh.loadWavNormalize('snare16b')
    wave = fh.loadWavNormalize('snare24b')
    dss.setPCM(wave)
