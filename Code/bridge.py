DSS = __import__('dss')
GUI = __import__('control')
midi = __import__('midi')
fh = __import__('filehandler')
t = __import__('tools')

import json


#GUI functions
def getParams(dss, gui):
    prog = int(gui.prog.get())-1
    dss.queueOperation(lambda s, prog=prog: s.getParameters(prog))

def setParams(dss, gui):
    progname = gui.progname.get()
    dss.queueOperation(lambda s, progname=progname: s.setParameters(progname))

def saveProgram(dss, gui):
    prog = int(gui.prog.get())-1
    dss.queueOperation(lambda s, prog=prog: s.saveProgram(prog))
    dss.queueOperation(lambda s: s.getNameList())

def changeProgram(dss, gui):
    prog = int(gui.prog.get())-1
    dss.programChange(prog)

    if gui.autoget.get():
        getParams(dss, gui)

def saveFile(dss, gui):
    name = gui.progname.get()
    fh.savePatch(name, dss.extractParameters())

def loadFile(dss, gui):
    name = gui.progname.get()
    if fh.checkPatch(name):
        dss.putParameters(fh.loadPatch(name))
        dss.queueOperation(lambda s, name=name: s.setParameters(name))

def loadSystem(dss, gui):
    systemData = gui.systemData
    
    multisoundNumber = 0
    
    for operation in systemData:
        if operation[0] == 'pcm':
            sampleLocation = fh.curDir + '\\Data\\Systems' + operation[1]
            sampleOffset = operation[2]
                
            sampleName = sampleLocation.split('\\')[-1]
            
            wave = fh.loadWavNormalize(sampleLocation)
            length = len(wave)
            
            dss.addSample(sampleName, sampleOffset, length)
            dss.queueOperation(lambda s, wave=wave, start=sampleOffset: s.setPCM(wave, start))
        elif operation[0] == 'mlt':
            file = open(fh.curDir + '\\Data\\Systems' + operation[1], 'r')
            gui.mult.loadMultisoundDirect(file)
            
            msn = gui.mult.getValues()
            dss.queueOperation(lambda s, prog=multisoundNumber, msn=msn: s.setMultisound(prog, msn))
            #this could be optimized
            dss.queueOperation(lambda s, prog=multisoundNumber, msn=msn: s.setMultisoundsListAfterMultisoundSet(prog, msn))
            multisoundNumber += 1
        elif operation[0] == 'pgm':
            file = open(fh.curDir + '\\Data\\Systems' + operation[1], 'r')
            gui.loadProgramDirect(file)
            
            values = gui.getValues()
            paramList = {}
            for i, key in enumerate(dss.param.keys()):
                paramList[key] = values[i]
            
            progname = gui.progname.get()
            prog = operation[2]-1
            dss.queueOperation(lambda s, progname=progname, paramList=paramList: s.setParameters(progname, param=paramList))
            dss.queueOperation(lambda s, prog=prog: s.saveProgram(prog))
    
    dss.queueOperation(lambda s: s.getMultisoundsList())
    dss.queueOperation(lambda s: s.getNameList())
    prog = int(gui.prog.get())-1
    dss.queueOperation(lambda s, prog=prog: s.getParameters(prog))


def updateControl(dss, gui):
    #Program list
    gui.progname.delete(0, 100)
    gui.progname.insert(0, dss.namelist[int(gui.prog.get())-1])

    #Mode
    if dss.mode >= 0 and dss.mode <= 8:
        gui.mode.set(dss.modeNames[dss.mode] + ' Mode')
    else:
        gui.mode.set('Unknown Mode')
    
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
        dss.queueOperation(lambda s, msn=msn: s.getMultisound(msn))
    except:
        print('A: No multisound selected')

def setMultisound(dss, gui):
    prog = gui.mult.multisound.curselection()
    
    if len(prog) < 1: 
        print('A: No multisound slot selected')
        return
    prog = prog[0]
    
    if prog >= dss.multiAmount: prog = dss.multiAmount
    
    msn = gui.mult.getValues()
    dss.queueOperation(lambda s, prog=prog, msn=msn: s.setMultisound(prog, msn))
    dss.queueOperation(lambda s, prog=prog, msn=msn: s.setMultisoundsListAfterMultisoundSet(prog, msn))
    dss.queueOperation(lambda s: s.getMultisoundsList())
    getMultisound(dss, gui)

def deleteMultisound(dss, gui):
    prog = gui.mult.multisound.curselection()
    
    if len(prog) < 1: 
        print('A: No multisound slot selected')
        return
    prog = prog[0]
    
    if prog >= dss.multiAmount: 
        print('A: Can\'t delete empty multisound')
        return
    
    if prog != dss.multiAmount-1:
        print("A: Can only delete last multisound for now :(")
        return

    dss.queueOperation(lambda s, prog=prog: s.deleteMultisound(prog))
    dss.queueOperation(lambda s: s.getMultisoundsList())

def addSample(dss, gui):
    sampleLocation = gui.sample.sampleLocation
    sampleOffset = int(gui.sample.sampleOffset.get())
        
    sampleName = sampleLocation.split('/')[-1]
    start = sampleOffset
    
    wave = fh.loadWavNormalize(sampleLocation)
    length = len(wave)
    gui.sample.addOffset(length)
    
    dss.addSample(sampleName, start, length)
    dss.queueOperation(lambda s, wave=wave, start=start: s.setPCM(wave, start))
    
    dss.updateGUI = True

def loadSampleMap(dss, gui):
    dss.samples = gui.sample.loadedSampleMap.copy()
    gui.sample.sampleOffset.set(dss.getSampleMemoryFreeLoc())
    dss.updateGUI = True

def saveSampleMap(dss, gui):
    gui.sample.savesamplemap(dss.samples)
    
def setSampleOffsetToFree(dss, gui):
    gui.sample.sampleOffset.set(dss.getSampleMemoryFreeLoc())
    dss.updateGUI = True
    
def getPCM(dss, gui):
    start = int(gui.sample.pcm.pcmStart.get())
    end = int(gui.sample.pcm.pcmEnd.get())
    dss.queueOperation(lambda s, start=start, end=end: s.getPCM(start, end))