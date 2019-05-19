DSS = __import__('dss')
GUI = __import__('control')
midi = __import__('midi')
fh = __import__('filehandler')
t = __import__('tools')
b = __import__('bridge')
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


b.getParams(dss, gui)

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
    gui.egUpdate()

    #GUI functions - Main
    com = gui.execcommand
    if type(com) == str:
        #print('received command')
        if com == 'getparameters':
            b.getParams(dss, gui)
        elif com == 'setparameters':
            b.setParams(dss, gui)
        elif com == 'saveprogram':
            b.saveProgram(dss, gui)
        elif com == 'changeprogram':
            b.changeProgram(dss, gui)
        elif com == 'savefile':
            b.saveFile(dss, gui)
        elif com == 'loadfile':
            b.loadFile(dss, gui)
        elif com == 'updatecontrol':
            b.updateControl(dss, gui)
        elif com == 'multiopen':
            b.multisoundOpen(dss, gui)
        elif com == 'getpcm':
            b.getPCM(dss, gui)

        gui.execCom(0)

    #GUI functions - Multisound
    com = gui.mult.execcommand
    if type(com) == str:
        if com == 'getmultisound':
            b.getMultisound(dss, gui)

        gui.mult.execCom(0)

   


    #Check for sysex messages
    sysex = midi.getSysex(dss.input)
    if sysex[0]:
        dss.decodeSysex(sysex[1])

    if dss.updateGUI:
        b.updateControl(dss, gui)
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
