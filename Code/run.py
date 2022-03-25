DSS = __import__('dss')
GUI = __import__('control')
midi = __import__('midi')
fh = __import__('filehandler')
t = __import__('tools')
b = __import__('bridge')

# print('''
#          ___  __    ___      ___  __  __       _ 
#   /\ /\ /___\/__\  / _ \    /   \/ _\/ _\     / |
#  / //_///  // \// / /_\/   / /\ /\ \ \ \ _____| |
# / __ \/ \_// _  \/ /_\\   / /_// _\ \_\ \_____| |
# \/  \/\___/\/ \_/\____/  /___,'  \__/\__/     |_|
                                                 
# ''')
print("""
 .--.   .--.      ,-----.    .-------.      .-_'''-.           ______        .-'''-.    .-'''-.                 ,---.  
 |  | _/  /     .'  .-,  '.  |  _ _   \    '_( )_   \         |    _ `''.   / _     \  / _     \               /_   |  
 | (`' ) /     / ,-.|  \ _ \ | ( ' )  |   |(_ o _)|  '        | _ | ) _  \ (`' )/`--' (`' )/`--'                 ,_ |  
 |(_ ()_)     ;  \  '_ /  | :|(_ o _) /   . (_,_)/___|        |( ''_'  ) |(_ o _).   (_ o _).     _ _    _ _ ,-./  )|  
 | (_,_)   __ |  _`,/ \ _/  || (_,_).' __ |  |  .-----.       | . (_) `. | (_,_). '.  (_,_). '.  ( ' )--( ' )\  '_ '`) 
 |  |\ \  |  |: (  '\_/ \   ;|  |\ \  |  |'  \  '-   .'       |(_    ._) '.---.  \  :.---.  \  :(_{;}_)(_{;}_)> (_)  ) 
 |  | \ `'   / \ `"/  \  ) / |  | \ `'   / \  `-'`   |        |  (_.\.' / \    `-'  |\    `-'  | (_,_)--(_,_)(  .  .-' 
 |  |  \    /   '. \_/``".'  |  |  \    /   \        /        |       .'   \       /  \       /               `-'`-'|  
 `--'   `'-'      '-----'    ''-'   `'-'     `'-...-'         '-----'`      `-...-'    `-...-'                  '---'  

""")

#Preinit config
configPresent, config = fh.getConfig()

#Handle config
debug = config.get('debug', None) == 'true'
logParameterChanges = config.get('logParameterChanges', None) == 'true'

#Chose MIDI input and Output
devices = midi.getMidiDevices()
mIn, mOut = t.chooseDevices(devices, config)

#Setup DSS1 communication
dss = DSS.DSS(mIn, mOut, debug=debug, logParameterChanges=logParameterChanges)



#Start GUI
root = GUI.tk.Tk()
gui = GUI.DSS1main(root,
                  titlefont = ('Microgramma D Extended', 16),
                  textfont  = ('Lucida Sans', 11),
                  numberfont= ('Lucida Sans', 8))

#Get start information
dss.setPlayMode()
dss.getNameList() #first sysex not queued to kickstart communications
dss.queueOperation(lambda s: s.getMultisoundsList())
b.getParams(dss, gui)
t.delay(0.1)

#Startup sysex handling (handle all of the queue)
sysexBuffer = []
received = False
while True:
    recv, sysex, sysexBuffer = midi.getSysex(dss.input, sysexBuffer)
    if recv:
        if not received:
            print('├────── Communication established!')
            received = True
        dss.decodeSysex(sysex)
    else:
        break
if not received:
    print('└──//── Communications failed!')
    input('...')

b.updateControl(dss, gui)

def updateTask(sysexBuffer):
    #EG Curves
    gui.egUpdate(proportional = False)

    #GUI functions - Main
    com = gui.execcommand
    if type(com) == str:
        #print('received command')
        if com == 'getparameters':
            b.getParams(dss, gui)
        elif com == 'setparameters':
            b.setParams(dss, gui)
        elif com == 'getprogramlist':
            dss.queueOperation(lambda s: s.getNameList())
        elif com == 'saveprogram':
            b.saveProgram(dss, gui)
        elif com == 'getmode':
            dss.queueOperation(lambda s: s.getMode())
        elif com == 'playmode':
            dss.setPlayMode()
            dss.queueOperation(lambda s: s.getMode())
        elif com == 'changeprogram':
            b.changeProgram(dss, gui)
        elif com == 'savefile':
            b.saveFile(dss, gui)
        elif com == 'loadfile':
            b.loadFile(dss, gui)
        elif com == 'loadsystem':
            b.loadSystem(dss, gui)
        elif com == 'updatecontrol':
            b.updateControl(dss, gui)
        elif com == 'getpcm':
            b.getPCM(dss, gui)
        elif com == 'setpcm':
            b.setPCM(dss, gui)

        gui.execCom(0)
        
    com = gui.proglist.execcommand
    if type(com) == str:
        if com == 'getprogramlist':
            dss.queueOperation(lambda s: s.getNameList())
            
        gui.proglist.execCom(0)

    #GUI functions - Multisound
    com = gui.mult.execcommand
    if type(com) == str:
        if com == 'getmultisound':
            b.getMultisound(dss, gui)
        elif com == 'setmultisound':
            b.setMultisound(dss, gui)
        elif com == 'deletemultisound':
            b.deleteMultisound(dss, gui)
        elif com == 'getmultisoundlist':
            dss.queueOperation(lambda s: s.getMultisoundsList())

        gui.mult.execCom(0)
        
    #GUI functions - Sample Memory
    com = gui.sample.execcommand
    if type(com) == str:
        if com == 'addsample':
            b.addSample(dss, gui)
        elif com == 'loadsamplemap':
            b.loadSampleMap(dss, gui)
        elif com == 'savesamplemap':
            b.saveSampleMap(dss, gui)
        elif com == 'setsampleoffsettofree':
            b.setSampleOffsetToFree(dss, gui)
        
        gui.sample.execCom(0)

    com = gui.sample.pcm.execcommand
    if type(com) == str:
        if com == 'fetchsample':
            b.getPCM(dss, gui)
        
        gui.sample.pcm.execCom(0)


    #Check for sysex messages
    recv, sysex, sysexBuffer = midi.getSysex(dss.input, sysexBuffer)
    if recv:
        dss.decodeSysex(sysex)

    if dss.updateGUI:
        b.updateControl(dss, gui)
        dss.updateGUI = False
        
    if dss.emitPCM:
        gui.sample.pcm.saveData(dss.pcm)
        dss.emitPCM = False

    #Control check
    values = gui.getValues()
    for i, key in enumerate(dss.param.keys()):
        if values[i] != dss.param[key]['v']:
            dss.param[key]['v'] = values[i]
            dss.setKey(key)
            
    #dss queue
    dss.handleQueue()

    gui.frame.after(50, updateTask, sysexBuffer)



root.protocol("WM_DELETE_WINDOW", lambda: quit())
updateTask(sysexBuffer)
root.mainloop()
