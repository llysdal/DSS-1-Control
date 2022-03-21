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

    #Mode
    gui.mode.set(dss.modeNames[dss.mode] + ' Mode')
    
    #Parameters
    parList = dss.extractParameters()
    gui.setValues(parList)
    
    #Multisound list - main window
    #Fetch current multisound values
    # osc1 = min(gui.oscms.index(gui.osc1w.get()), len(gui.oscms)-1)
    # osc2 = min(gui.oscms.index(gui.osc2w.get()), len(gui.oscms)-1)
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
    # gui.osc1w.set(gui.oscms[osc1])
    # gui.osc2w.set(gui.oscms[osc2])

    #Multisound list - multisound window
    gui.mult.multisound.delete(0, 100)
    for i, name in enumerate(dss.multiName):
        gui.mult.multisound.insert(i, name)

    #Multisound lengths
    gui.mult.multiLen = dss.multiLen

    #Multisound values
    multParList = dss.extractMultisoundParameters()
    gui.mult.setValues(multParList)
    
    #Program list - program list window
    gui.proglist.programs.delete(0, 1000)
    for i in range(32):
        gui.proglist.programs.insert(i, f'{i+1:02d} - {dss.namelist[i]}')
    
    #Samples
    gui.sample.setSamples(dss.samples)

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

def deleteMultisound(dss, gui):
    progno = gui.mult.multisound.curselection()
    
    if len(progno) < 1: 
        print('A: No multisound slot selected')
        return
    progno = progno[0]
    
    if progno >= dss.multiAmount: 
        print('A: Can\'t delete empty multisound')
        return
    
    if progno != dss.multiAmount-1:
        print("A: Can only delete last multisound for now :(")
        return

    dss.deleteMultisound(progno)
    dss.getMultisoundsList()

def addSample(dss, gui):
    sampleLocation = gui.sample.sampleLocation
    
    sampleName = sampleLocation.split('/')[-1]
    start = dss.getSampleMemoryFreeLoc()
    
    wave = fh.loadWavNormalize(sampleLocation)
    length = len(wave)
    
    dss.addSample(sampleName, start, length)
    dss.setPCM(wave, start)
    
    dss.updateGUI = True

def loadSampleMap(dss, gui):
    dss.samples = gui.sample.loadedSampleMap.copy()
    dss.updateGUI = True

def saveSampleMap(dss, gui):
    gui.sample.savesamplemap(dss.samples)
    
