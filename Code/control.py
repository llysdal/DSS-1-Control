fh = __import__('filehandler')
import tkinter as tk
from tkinter import N,S,E,W, HORIZONTAL, VERTICAL, BROWSE
from math import exp

midiKeys = []
for o in range(-1, 10):
    for k in range(0,12):
        midiKeys.append(('C','C#','D','D#','E','F','F#','G','G#','A','A#','B')[k] + str(o))
midiKeys = midiKeys[0:128]


class spinbox(tk.Spinbox):
    def set(self, value):
        self.delete(0,100)
        self.insert(0,value)

class Application():
    def init(self, master, titlefont, textfont, numberfont):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid(sticky=N+S+E+W)

        #Resizeability
        self.top = self.frame.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        self.black = "#212121"
        self.grey  = '#2e2e2e'
        self.white = '#e2e2e2'
        self.blue  = '#336ece'

        self.titlefont = titlefont
        self.textfont = textfont
        self.numberfont = numberfont

        self.frame.configure(background = self.black)

    def createCanvas(self, gridpos, columnspan = 1, rowspan = 1, size = (100,100)):
        canvas = tk.Canvas(self.frame, width = size[0], height = size[1], bg = 'black')
        canvas.grid(column = gridpos[0], row = gridpos[1], columnspan = columnspan, rowspan = rowspan, sticky = N+S+E+W)

        return canvas

    def createSlider(self, gridpos, val, res = 1, start = 0, length = 100, width = 15, orient = 0, columnspan = 1, rowspan = 1, showvalue = True, sticky = E+S):
        slider = tk.Scale(self.frame, from_ = val[0], to = val[1], resolution = res,\
                       orient = (HORIZONTAL, VERTICAL)[orient], length = length, showvalue = showvalue, width = width)
        slider.configure(background = self.black, foreground = self.white, highlightthickness = 0, troughcolor = self.grey, activebackground = self.white, font = self.numberfont)
        slider.grid(column = gridpos[0], row = gridpos[1], rowspan = rowspan, columnspan = columnspan, sticky = sticky)

        slider.set(start)

        return slider

    def createDropdown(self, gridpos, values = [1,2,3], start = 1, columnspan = 1, requestparent = False):
        string = tk.StringVar(self.frame)
        string.set(start)

        dropdown = tk.OptionMenu(self.frame, string, *values)
        dropdown.configure(background = self.black, foreground = self.white, highlightthickness = 0, borderwidth = 2)#, activebackground = self.blue)
        dropdown.grid(column = gridpos[0], row = gridpos[1], columnspan = columnspan, sticky = E+S)

        if requestparent:
            return string, dropdown

        return string

    def createButton(self, gridpos, text, function):
        button = tk.Button(self.frame, text = text, command = function)
        button.configure(background = self.black, foreground = self.white)
        button.grid(column = gridpos[0], row = gridpos[1], stick = N+S+E+W)

    def createText(self, gridpos, text, columnspan = 1, sticky = W+S):
        label = tk.Label(self.frame, text = text, font = self.textfont, justify = 'left')
        label.configure(background = self.black, foreground = self.white)
        label.grid(column = gridpos[0], row = gridpos[1], columnspan = columnspan, sticky = sticky)

        return label

    def createTitle(self, gridpos, text, columnspan = 1):
        label = tk.Label(self.frame, text = text, font = self.titlefont, justify = 'left')
        label.configure(background = self.black, foreground = self.white)
        label.grid(column = gridpos[0], row = gridpos[1], columnspan = columnspan, sticky = E+W)

        return label

    def createDynText(self, gridpos, columnspan = 1):
        stringvar = tk.StringVar()

        label = tk.Label(self.frame, textvariable = stringvar, font = self.numberfont, justify = 'left')
        label.configure(background = self.black, foreground = self.white)
        label.grid(column = gridpos[0], row = gridpos[1], columnspan = columnspan, sticky = E+N)

        return stringvar

    def createCheckbutton(self, gridpos, text, columnspan = 1, sticky = E+S):
        intvar = tk.IntVar()

        button = tk.Checkbutton(self.frame, text = text, variable = intvar, onvalue = 1, offvalue = 0)
        button.configure(background = self.black)#, activebackground = self.blue)
        button.grid(column = gridpos[0], row = gridpos[1], columnspan = columnspan, sticky = sticky)

        return intvar

    def createSpinbox(self, gridpos, from_ = 0, to = 10, values = [], width = 2, sticky = E+N):
        if len(values) > 0:
            spin = spinbox(self.frame, values = values, width = width)
        else:
            spin = spinbox(self.frame, from_=from_, to=to, width = width)
        spin.grid(column = gridpos[0], row = gridpos[1], sticky = sticky)

        return spin

    def createMenu(self):
        menubar = tk.Menu(self.frame)
        self.top.config(menu=menubar)

        return menubar

    def minSizeX(self, x, width):
        self.frame.columnconfigure((x,0), minsize = width)

    def minSizeY(self, y, width):
        self.frame.rowconfigure((0,y), minsize = width)


class DSS1multi(Application):
    def __init__(self, master, titlefont, textfont, numberfont):
        self.init(master, titlefont, textfont, numberfont)
        self.setup()

        self.execcommand = 0

    def execCom(self, val):
        self.execcommand = val

    def setup(self):
        self.master.title('Korg DSS-1 Multisound Control')
        self.master.iconbitmap(fh.getRessourcePath('dss.ico'))

        self.menu = self.createMenu()
        self.menu.add_command(label='Get Multisound', command = lambda: self.execCom('getmultisound'))
        self.menu.add_command(label='*/Set Multisound/*', command = lambda: self.execCom('setmultisound'))


        #Multisound selector
        self.createTitle((0,0), 'Multisound')

        self.multisound = tk.Listbox(self.frame, selectmode=BROWSE, height = 16)
        for i in range(16):
            self.multisound.insert(1000, str(i+1))
        self.multisound.grid(row = 1, column = 0, rowspan = 16, sticky = W+N)

        o = 2
        #Multisound editing
        self.createText((o, 1), 'Name', sticky = W+N)
        self.mulname = tk.Entry(self.frame, width = 12)
        self.mulname.grid(row = 1, column = o+1, sticky = E+N)

        self.createText((o, 2), 'Length', sticky = W+N)
        self.length = self.createDynText((o+1, 2))

        self.createText((o, 3), 'Looping', sticky = W+N)
        self.loop = self.createCheckbutton((o+1, 3), text = '', sticky = E+N)

        self.createText((o, 4), 'Sounds', sticky = W+N)
        self.sounds = spinbox(self.frame, from_=1, to=16, width = 2, command = lambda: self.execCom('reloadsounds'))
        self.sounds.grid(row = 4, column = o+1, sticky = E+N)

        self.createText((o, 5), 'Max interval', sticky = W+N)
        self.maxint = self.createDynText((o+1, 5))

        #self.createText((o, 6), 'Checksum', sticky = W+N)
        #self.checksum = self.createDynText((o+1, 6))

        o+=2

        self.soundframe = []
        for s in range(16):
            self.soundframe.append(Application())

            f = self.soundframe[s]

            f.init(self.frame, self.titlefont, self.textfont, self.numberfont)

            if s < 6:
                f.frame.grid(column = o+s, row = 1, rowspan = 18)
            elif s >= 12:
                f.frame.grid(column = o+s-12, row = 21)
            else:
                f.frame.grid(column = o+s-6, row = 20)

            f.createTitle((0, 0), str(s+1), columnspan = 2)

            f.createText((0, 1), 'Top Key')
            f.topkey = f.createSpinbox((1, 1), values = midiKeys, width = 4)

            f.createText((0, 2), 'Orig. Key')
            f.origkey = f.createSpinbox((1, 2), values = midiKeys, width = 4)

            f.createText((0, 3), 'Tune')
            f.tune = f.createSlider((1, 3), (-63, 63), start = 0)

            f.createText((0, 4), 'Level')
            f.level = f.createSlider((1, 4), (1, 64), start = 64)

            f.createText((0, 5), 'Cutoff')
            f.cutoff = f.createSlider((1, 5), (1, 64), start = 64)

            f.createText((0, 6), 'Transpose')
            f.transpose = f.createCheckbutton((1, 6), '')

            f.createText((0, 7), 'Samp. Freq.')
            f.freq = f.createDropdown((1, 7), ['32kHz', '24kHz', '16kHz', '48kHz'], start = '32kHz')

            f.createText((0, 8), 'Word Adr.')
            f.soundwadr = f.createDynText((1, 8))
            f.createText((0, 9), 'Start Adr.')
            f.soundsadr = f.createDynText((1, 9))
            f.createText((0, 10), 'Length')
            f.soundlen = f.createDynText((1, 10))

            f.createText((0, 11), 'Loop S. Adr.')
            f.loopsadr = f.createDynText((1, 11))
            f.createText((0, 12), 'Loop Length')
            f.looplen = f.createDynText((1, 12))

            f.frame.grid_remove()



    def setValues(self, values):
        self.mulname.delete(0,100)
        self.mulname.insert(0, values[1])
        self.length.set(values[2])
        self.loop.set(values[3])
        self.sounds.set(values[4])
        self.maxint.set(values[5])
        #self.checksum.set(values[6])

        for s in range(16):
            self.soundframe[s].frame.grid_remove()

        for s in range(values[4]):
            self.soundframe[s].topkey.set(midiKeys[values[7][s][0]])
            self.soundframe[s].origkey.set(midiKeys[values[7][s][1]])
            self.soundframe[s].tune.set(values[7][s][2]-63)
            self.soundframe[s].level.set(values[7][s][3])
            self.soundframe[s].cutoff.set(values[7][s][4])
            self.soundframe[s].soundwadr.set(values[7][s][5])
            self.soundframe[s].soundsadr.set(values[7][s][6])
            self.soundframe[s].soundlen.set(values[7][s][7])
            self.soundframe[s].loopsadr.set(values[7][s][8])
            self.soundframe[s].looplen.set(values[7][s][9])
            self.soundframe[s].transpose.set(values[7][s][10])
            self.soundframe[s].freq.set(['32kHz', '24kHz', '16kHz', '48kHz'][values[7][s][11]])
            self.soundframe[s].frame.grid()


class DSS1main(Application):
    def __init__(self, master, titlefont, textfont, numberfont):
        self.init(master, titlefont, textfont, numberfont)
        self.setup()

        self.execcommand = 0

        #Workaround
        self.oscrange = 0

    def egUpdate(self):

        for param in ((self.egfc, (self.egfat, self.egfdt, self.egfslt, self.egfrt), (self.egfa, self.egfd, self.egfb, self.egfsl, self.egfs, self.egfr)),
                      (self.egvc, (self.egvat, self.egvdt, self.egvslt, self.egvrt), (self.egva, self.egvd, self.egvb, self.egvsl, self.egvs, self.egvr))):
            canvas = param[0]
            dyntext = param[1]
            egpar = param[2]

            #Canvas
            w,h = canvas.winfo_width(), canvas.winfo_height()
            h2 = h-10
            canvas.delete('all')
            attack = (w/4 * egpar[0].get()/63, h-h2)
            decay = (w/4 * egpar[1].get()/63+attack[0], h-h2*egpar[2].get()/63)
            slope = (w/4 * egpar[3].get()/63+decay[0], h-h2*egpar[4].get()/63)
            sustain = (w-w/4 * egpar[5].get()/63, h-h2*egpar[4].get()/63)
            release = (w, h)

            canvas.create_line((0, h, attack[0], attack[1]), fill = '#2b7cff')
            canvas.create_line((attack[0], attack[1], decay[0], decay[1]), fill = '#2b7cff')
            canvas.create_line((decay[0], decay[1], slope[0], slope[1]), fill = '#2b7cff')
            canvas.create_line((slope[0], slope[1], sustain[0], sustain[1]), fill = '#2b7cff')
            canvas.create_line((sustain[0], sustain[1], release[0], release[1]), fill = '#2b7cff')

            #Text
            attackTime  = 5*exp(0.15*egpar[0].get())
            decayTime   = 5*exp(0.135*egpar[1].get())
            slopeTime   = 5*exp(0.15*egpar[3].get())
            releaseTime = 5*exp(0.135*egpar[5].get())

            #print('decay = ' + str(egpar[1].get()) + '  -  ' + str(decayTime))

            for i, time in enumerate((attackTime, decayTime, slopeTime, releaseTime)):
                if time < 9.9:
                    dyntext[i].set('{0:.1g}ms'.format(min(time,9)))
                elif time < 99:
                    dyntext[i].set('{0:.2g}ms'.format(min(time,99)))
                else:
                    dyntext[i].set('{0:.2g}s'.format(time/1000))

    def openMultisoundGUI(self):
        self.multWindow.deiconify()

    def execCom(self, val):
        self.execcommand = val

    def setValues(self, values):
        self.osc1v.set(values[0])
        self.osc2v.set(values[1])
        self.autoi.set(values[2])
        self.noise.set(values[3])
        self.filterm.set(('12dB','24dB')[values[4]])
        self.filterinv.set(1-values[5])
        self.filterc.set(values[6])
        self.filtereg.set(values[7])
        self.filterr.set(values[8])
        self.filterk.set(values[9])
        self.fmgf.set(values[10])
        self.fmgd.set(values[11])
        self.fmgi.set(values[12])
        self.egfa.set(values[13])
        self.egfd.set(values[14])
        self.egfb.set(values[15])
        self.egfsl.set(values[16])
        self.egfs.set(values[17])
        self.egfr.set(values[18])
        self.vcad.set((values[19], 64-values[19])[values[19] > 63])
        self.vcal.set(values[20])
        self.egva.set(values[21])
        self.egvd.set(values[22])
        self.egvb.set(values[23])
        self.egvsl.set(values[24])
        self.egvs.set(values[25])
        self.egvr.set(values[26])
        self.vela.set(values[27])
        self.velfc.set(values[28])
        self.velfa.set(values[29])
        self.velfd.set(values[30])
        self.velfs.set(values[31])
        self.velvl.set(values[32])
        self.velva.set(values[33])
        self.velvd.set(values[34])
        self.velvs.set(values[35])
        self.aftmgi.set(values[36])
        self.aftf.set(values[37])
        self.aftfm.set(('MG Int', 'Cutoff')[values[38]])
        self.aftvl.set(values[39])
        self.joyr.set(values[40])
        self.joyf.set(values[41])
        self.bass.set(values[42]-4)
        self.treb.set(values[43]-4)
        self.mgaf.set(values[44])
        self.mgbf.set(values[45])
        self.d1t.set(values[46])
        self.d1f.set(values[47])
        self.d1e.set(values[48])
        self.mgam1.set(values[49])
        self.mgbm1.set(values[50])
        self.d2s.set(('Direct', 'Delay 1')[values[51]])
        self.d2t.set(values[52])
        self.d2f.set(values[53])
        self.d2e.set(values[54])
        self.mgam2.set(values[55])
        self.mgbm2.set(values[56])
        self.d2mi.set(values[57])
        self.osc1w.set(self.oscms[values[58]])
        self.osc2w.set(self.oscms[values[59]])
        self.oscrange = values[60]
        self.osc2s.set(values[61])
        self.oscres.set(('6 bits', '7 bits', '8 bits', '10 bits', '12 bits')[values[62]])
        self.osc1o.set((16,8,4)[values[63]])
        self.osc2o.set((16,8,4)[values[64]])
        self.osc2d.set(values[65])
        self.osc2i.set(values[66])
        self.omgm.set(('Off', 'Osc1', 'Osc2', 'Both')[values[67]])
        self.omgf.set(values[68])
        self.omgi.set(values[69])
        self.omgd.set(values[70])
        self.autom.set(('Off', 'Osc1', 'Osc2', 'Both')[values[71]])
        self.autop.set(('Down', 'Up')[values[72]])
        self.autot.set(values[73])
        self.unid.set(values[74])
        self.oscx.set(values[75])
        self.assign.set(('Poly 1', 'Poly 2', 'Unison')[values[76]])
        self.unia.set((1,2,4,8)[values[77]])

    def getValues(self):
        return (self.osc1v.get(),
                self.osc2v.get(),
                self.autoi.get(),
                self.noise.get(),
                ('12dB','24dB').index(self.filterm.get()),
                1-self.filterinv.get(),
                self.filterc.get(),
                self.filtereg.get(),
                self.filterr.get(),
                self.filterk.get(),
                self.fmgf.get(),
                self.fmgd.get(),
                self.fmgi.get(),
                self.egfa.get(),
                self.egfd.get(),
                self.egfb.get(),
                self.egfsl.get(),
                self.egfs.get(),
                self.egfr.get(),
                (self.vcad.get(), 64-self.vcad.get())[self.vcad.get() < 0],
                self.vcal.get(),
                self.egva.get(),
                self.egvd.get(),
                self.egvb.get(),
                self.egvsl.get(),
                self.egvs.get(),
                self.egvr.get(),
                self.vela.get(),
                self.velfc.get(),
                self.velfa.get(),
                self.velfd.get(),
                self.velfs.get(),
                self.velvl.get(),
                self.velva.get(),
                self.velvd.get(),
                self.velvs.get(),
                self.aftmgi.get(),
                self.aftf.get(),
                ('MG Int', 'Cutoff').index(self.aftfm.get()),
                self.aftvl.get(),
                self.joyr.get(),
                self.joyf.get(),
                self.bass.get()+4,
                self.treb.get()+4,
                self.mgaf.get(),
                self.mgbf.get(),
                self.d1t.get(),
                self.d1f.get(),
                self.d1e.get(),
                self.mgam1.get(),
                self.mgbm1.get(),
                ('Direct', 'Delay 1').index(self.d2s.get()),
                self.d2t.get(),
                self.d2f.get(),
                self.d2e.get(),
                self.mgam2.get(),
                self.mgbm2.get(),
                self.d2mi.get(),
                self.oscms.index(self.osc1w.get()),
                self.oscms.index(self.osc2w.get()),
                self.oscrange,
                self.osc2s.get(),
                ('6 bits', '7 bits', '8 bits', '10 bits', '12 bits').index(self.oscres.get()),
                (16,8,4).index(int(self.osc1o.get())),
                (16,8,4).index(int(self.osc2o.get())),
                self.osc2d.get(),
                self.osc2i.get(),
                ('Off', 'Osc1', 'Osc2', 'Both').index(self.omgm.get()),
                self.omgf.get(),
                self.omgi.get(),
                self.omgd.get(),
                ('Off', 'Osc1', 'Osc2', 'Both').index(self.autom.get()),
                ('Down', 'Up').index(self.autop.get()),
                self.autot.get(),
                self.unid.get(),
                self.oscx.get(),
                ('Poly 1', 'Poly 2', 'Unison').index(self.assign.get()),
                (1,2,4,8).index(int(self.unia.get())))

    #Gui setup, this is gonna be long
    #Dont touch anything here please
    def setup(self):
        self.master.title('Korg DSS-1 Main Control')
        self.master.iconbitmap(fh.getRessourcePath('dss.ico'))

        self.multWindow = tk.Toplevel(self.master)
        self.mult = DSS1multi(self.multWindow, self.titlefont, self.textfont, self.numberfont)
        self.multWindow.withdraw()
        self.multWindow.protocol("WM_DELETE_WINDOW", lambda: self.multWindow.withdraw())

        self.menu = self.createMenu()

        optionmenu = tk.Menu(self.menu, tearoff=0)
        self.autoget = tk.IntVar()
        optionmenu.add_checkbutton(label="Autoget parameters", variable=self.autoget)
        self.menu.add_cascade(label='Options', menu=optionmenu)
        self.menu.add_separator()

        self.menu.add_command(label='Get Parameters', command = lambda: self.execCom('getparameters'))
        self.menu.add_command(label='Set Parameters', command = lambda: self.execCom('setparameters'))
        self.menu.add_command(label='Save Program',   command = lambda: self.execCom('saveprogram'))
        self.menu.add_separator()


        localmenu = tk.Menu(self.menu, tearoff=0)
        localmenu.add_command(label='Save to file',   command = lambda: self.execCom('savefile'))
        localmenu.add_command(label='Load from file', command = lambda: self.execCom('loadfile'))
        self.menu.add_cascade(label='Local', menu=localmenu)

        self.menu.add_separator()
        self.menu.add_command(label='Multisounds', command = lambda: self.openMultisoundGUI() and self.execCom('multiopen'))

        self.menu.add_separator()
        self.menu.add_command(label='Get Soundmemory', command = lambda: self.execCom('getpcm'))


        #Background
        backimage = tk.PhotoImage(file = fh.getRessourcePath('background.png'))
        backlabel = tk.Label(self.frame, image=backimage, bd = 0)
        #backlabel.place(x=0, y=0)
        backlabel.image = backimage


        self.minSizeY( 0, 5)
        self.minSizeX( 0, 5)
        self.minSizeX(33, 5)
        self.minSizeY(28, 5)

    #Program management
        self.createText((1, 0), 'Program', sticky = W+S)
        self.prog = tk.Spinbox(self.frame, from_=1, to=32, width = 2, command = lambda: self.execCom('changeprogram'))
        self.prog.grid(row = 0, column = 2, sticky = E+S)

        self.progname = tk.Entry(self.frame, width = 12)
        self.progname.grid(row = 1, column = 2, sticky = E+N)

        o = 1
    #Autobend
        self.createTitle((o, 10), 'Autobend', columnspan = 2)
        self.createText((o, 11), 'Mode')
        self.autom = self.createDropdown((o+1, 11), ['Off', 'Osc1', 'Osc2', 'Both'], start = 'Both')
        self.createText((o, 12), 'Polarity')
        self.autop = self.createDropdown((o+1, 12), ['Down', 'Up'], start = 'Up')
        self.createText((o, 13), 'Intensity')
        self.autoi = self.createSlider((o+1, 13), (0,127))
        self.createText((o, 14), 'Time')
        self.autot = self.createSlider((o+1, 14), (0,31))
        self.minSizeX(o+1, 80)
        o += 2

        #Gap
        self.minSizeX(o, 30)
        o += 1

    #Oscillator 1
        self.createTitle((o, 10), 'Oscillator 1', columnspan = 2)
        self.createText((o, 11), 'Multisound')
        self.oscms  = list(map(str, range(1,17)))
        self.osc1w, self.osc1wo = self.createDropdown((o+1, 11), self.oscms, start = self.oscms[0], requestparent = True)
        self.createText((o, 12), 'Octave')
        self.osc1o  = self.createDropdown((o+1, 12), [4,8,16], start = 8)
        self.createText((o, 14), 'D/A Resolution')
        self.oscres = self.createDropdown((o+1, 14), ['6 bits', '7 bits', '8 bits', '10 bits', '12 bits'], start = '12 bits')
        self.minSizeX(o+1, 80)
        o += 2

        #Gap
        self.minSizeX(o, 20)
        o += 1

    #Oscillator 2
        self.createTitle((o, 10), 'Oscillator 2', columnspan = 2)
        self.createText((o, 11), 'Multisound')
        self.osc2w, self.osc2wo = self.createDropdown((o+1, 11), self.oscms, start = self.oscms[0], requestparent = True)
        self.createText((o, 12), 'Octave')
        self.osc2o = self.createDropdown((o+1, 12), [4,8,16], start = 8)
        self.createText((o, 13), 'Interval')
        self.osc2i = self.createSlider((o+1, 13), (0,11))
        self.createText((o, 14), 'Detune')
        self.osc2d = self.createSlider((o+1, 14), (0,63))
        self.createText((o, 15), 'Sync')
        self.osc2s = self.createCheckbutton((o+1, 15), text = '')
        o += 2

        #Gap
        self.minSizeX(o, 30)
        o += 1

    #Mixer
        self.createTitle((o, 10), 'Mixer', columnspan = 3)
        self.createText((o, 14), '1', sticky = E+S)
        self.osc1v = self.createSlider((o, 11), (100,0), orient = 1, rowspan = 3)
        self.createText((o+1, 14), '2', sticky = E+S)
        self.osc2v = self.createSlider((o+1, 11), (100,0), orient = 1, rowspan = 3)
        self.createText((o+2, 14), 'Noise', sticky = E+S)
        self.noise = self.createSlider((o+2, 11), (63,0), orient = 1, rowspan = 3)
        o += 3

        #Gap
        self.minSizeX(o, 30)
        o += 1

    #Filter
        self.createTitle((o, 10), 'Filter', columnspan = 6)
        self.createText((o, 11), 'Mode', columnspan = 3)
        self.filterm  = self.createDropdown((o+3, 11), ['12dB', '24dB'], start = '24dB', columnspan = 3)
        self.createText((o, 12), 'Cutoff', columnspan = 3)
        self.filterc  = self.createSlider((o+3, 12), (0,127), columnspan = 3)
        self.createText((o, 13), 'Resonance', columnspan = 3)
        self.filterr  = self.createSlider((o+3, 13), (0, 63), columnspan = 3)
        self.createText((o, 14), 'KBD Track', columnspan = 3)
        self.filterk  = self.createSlider((o+3, 14), (0, 63), columnspan = 3)
        self.createText((o, 15), 'Filter EG', columnspan = 3)
        self.filtereg = self.createSlider((o+3, 15), (0, 63), columnspan = 3)
        self.createText((o, 16), 'EG Invert', columnspan = 3)
        self.filterinv= self.createCheckbutton((o+3, 16), text = '', columnspan = 3)

    #Filter EG
        self.egfc = self.createCanvas((o, 17), columnspan = 6, rowspan = 2, size=(225,100))
        self.egfa = self.createSlider((o, 19),   (63,0), orient = 1, rowspan = 2)
        self.egfd = self.createSlider((o+1, 19), (63,0), orient = 1, rowspan = 2)
        self.egfb = self.createSlider((o+2, 19), (63,0), orient = 1, rowspan = 2)
        self.egfsl= self.createSlider((o+3, 19), (63,0), orient = 1, rowspan = 2)
        self.egfs = self.createSlider((o+4, 19), (63,0), orient = 1, rowspan = 2)
        self.egfr = self.createSlider((o+5, 19), (63,0), orient = 1, rowspan = 2)
        self.egfat = self.createDynText((o, 21))
        self.egfdt = self.createDynText((o+1, 21))
        #self.egfbt = self.createDynText((21,o+2))
        self.egfslt= self.createDynText((o+3, 21))
        #self.egfst = self.createDynText((21,o+4))
        self.egfrt = self.createDynText((o+5, 21))
        o += 6

        #Gap
        self.minSizeX(o, 30)
        o += 1

    #VCA
        self.createTitle((o, 10), 'VCA', columnspan = 6)
        self.createText((o, 11), 'Level', columnspan = 3)
        self.vcal = self.createSlider((o+3, 11), (0,63), columnspan = 3)
        self.createText((o, 12), 'KBD Decay', columnspan = 3)
        self.vcad = self.createSlider((o+3, 12), (-63,63), columnspan = 3)
        self.createText((o, 13), 'Treble', columnspan = 3)
        self.treb = self.createSlider((o+3, 13), (-4,8), columnspan = 3)
        self.createText((o, 14), 'Bass', columnspan = 3)
        self.bass = self.createSlider((o+3, 14), (-4,8), columnspan = 3)

    #VCA EG
        self.egvc = self.createCanvas((o, 17), columnspan = 6, rowspan = 2, size=(225,100))
        self.egva = self.createSlider((o, 19),   (63,0), orient = 1, rowspan = 2)
        self.egvd = self.createSlider((o+1, 19), (63,0), orient = 1, rowspan = 2)
        self.egvb = self.createSlider((o+2, 19), (63,0), orient = 1, rowspan = 2)
        self.egvsl= self.createSlider((o+3, 19), (63,0), orient = 1, rowspan = 2)
        self.egvs = self.createSlider((o+4, 19), (63,0), orient = 1, rowspan = 2)
        self.egvr = self.createSlider((o+5, 19), (63,0), orient = 1, rowspan = 2)
        self.egvat = self.createDynText((o, 21))
        self.egvdt = self.createDynText((o+1, 21))
        #self.egvbt = self.createDynText((21,o+2))
        self.egvslt= self.createDynText((o+3, 21))
        #self.egvst = self.createDynText((21,o+4))
        self.egvrt = self.createDynText((o+5, 21))
        o += 6

        #Gap
        self.minSizeX(o, 30)
        o += 1

    #Delay 1
        self.createTitle((o, 10), 'Delay 1', columnspan = 2)
        self.createText((o, 11), 'Time')
        self.d1t = self.createSlider((o+1, 11), (0,500))
        self.createText((o, 12), 'Feedback')
        self.d1f = self.createSlider((o+1, 12), (0,15))
        self.createText((o, 13), 'Effect Level')
        self.d1e = self.createSlider((o+1, 13), (0,15))
        o += 2

        #Gap
        self.minSizeX(o, 20)
        o += 1

    #Delay 2
        self.createTitle((o, 10), 'Delay 2', columnspan = 2)
        self.createText((o, 11), 'Time')
        self.d2t = self.createSlider((o+1, 11), (0,500))
        self.createText((o, 12), 'Feedback')
        self.d2f = self.createSlider((o+1, 12), (0,15))
        self.createText((o, 13), 'Effect Level')
        self.d2e = self.createSlider((o+1, 13), (0,15))
        self.createText((o, 14), 'Source')
        self.d2s = self.createDropdown((o+1, 14), ['Direct', 'Delay 1'], start = 'Direct')
        self.createText((o, 15), 'Mod Invert')
        self.d2mi = self.createCheckbutton((o+1, 15), text = '')

    #MOD Section
        o = 4
        h = 16

    #MG
        self.createTitle((o, h), 'Osc MG', columnspan = 2)
        self.createText((o, h+1), 'Frequency')
        self.omgf = self.createSlider((o+1, h+1), (0,31))
        self.createText((o, h+2), 'Intensity')
        self.omgi = self.createSlider((o+1, h+2), (0,15))
        self.createText((o, h+3), 'Delay')
        self.omgd = self.createSlider((o+1, h+3), (0,15))
        self.createText((o, h+4), 'Mode')
        self.omgm = self.createDropdown((o+1, h+4), ['Off', 'Osc1', 'Osc2', 'Both'], start = 'Both')

        o += 3

        self.createTitle((o, h), 'Filter MG', columnspan = 2)
        self.createText((o, h+1), 'Frequency')
        self.fmgf = self.createSlider((o+1, h+1), (0,63))
        self.createText((o, h+2), 'Intensity')
        self.fmgi = self.createSlider((o+1, h+2), (0,63))
        self.createText((o, h+3), 'Delay')
        self.fmgd = self.createSlider((o+1, h+3), (0,63))

        o += 21

    #DDL MG
        self.createTitle((o, h), 'MG A', columnspan = 2)
        self.createText((o, h+1), 'Frequency')
        self.mgaf  = self.createSlider((o+1, h+1), (0,63))
        self.createText((o, h+2), 'Delay 1 Mod')
        self.mgam1 = self.createSlider((o+1, h+2), (0,63))
        self.createText((o, h+3), 'Delay 2 Mod')
        self.mgam2 = self.createSlider((o+1, h+3), (0,63))
        o += 3

        self.createTitle((o, h), 'MG B', columnspan = 2)
        self.createText((o, h+1), 'Frequency')
        self.mgbf  = self.createSlider((o+1, h+1), (0,63))
        self.createText((o, h+2), 'Delay 1 Mod')
        self.mgbm1 = self.createSlider((o+1, h+2), (0,63))
        self.createText((o, h+3), 'Delay 2 Mod')
        self.mgbm2 = self.createSlider((o+1, h+3), (0,63))

    #Velocity Sensitive
        o = 1
        h = 22

        self.minSizeY(h-1, 50)

        self.createTitle((o, h), 'Velocity Sensitive', columnspan = 8)

        self.createText((o, h+1), 'Autobend Int ')
        self.vela = self.createSlider((o+1, h+1), (0,63))
        self.createText((o, h+2), 'X-mod')
        self.oscx = self.createSlider((o+1, h+2), (0,31))

        self.createText((o+3, h+1), 'Filter Cutoff')
        self.velfc = self.createSlider((o+4, h+1), (0,63))
        self.createText((o+3, h+2), 'Filter EG Attack')
        self.velfa = self.createSlider((o+4, h+2), (0,63))
        self.createText((o+3, h+3), 'Filter EG Decay')
        self.velfd = self.createSlider((o+4, h+3), (0,63))
        self.createText((o+3, h+4), 'Filter EG Slope')
        self.velfs = self.createSlider((o+4, h+4), (0,63))

        self.createText((o+6, h+1), 'VCA Level')
        self.velvl = self.createSlider((o+7, h+1), (0,63))
        self.createText((o+6, h+2), 'VCA EG Attack')
        self.velva = self.createSlider((o+7, h+2), (0,63))
        self.createText((o+6, h+3), 'VCA EG Decay')
        self.velvd = self.createSlider((o+7, h+3), (0,63))
        self.createText((o+6, h+4), 'VCA EG Slope')
        self.velvs = self.createSlider((o+7, h+4), (0,63))
        o += 7
        o += 6

    #Aftertouch
        self.createTitle((o, h), 'Aftertouch', columnspan = 6)
        self.createText((o, h+1), 'Osc MG Int', columnspan = 3)
        self.aftmgi= self.createSlider((o+3, h+1), (0,15), columnspan = 3)
        self.createText((o, h+2), 'Filter', columnspan = 3)
        self.aftf  = self.createSlider((o+3, h+2), (0,15), columnspan = 3)
        self.createText((o, h+3), 'Filter Mod', columnspan = 3)
        self.aftfm = self.createDropdown((o+3, h+3), ['MG Int', 'Cutoff'], start = 'MG Int', columnspan = 3)
        self.createText((o, h+4), 'VCA Level', columnspan = 3)
        self.aftvl = self.createSlider((o+3, h+4), (0,15), columnspan = 3)
        o += 7

    #Joystick
        self.createTitle((o, h), 'Joystick', columnspan = 6)
        self.createText((o, h+1), 'Range', columnspan = 3)
        self.joyr = self.createSlider((o+3, h+1), (0,12), columnspan = 3)
        self.createText((o, h+2), 'Filter Control', columnspan = 3)
        self.joyf = self.createCheckbutton((o+3, h+2), text = '', columnspan = 3)
        o += 7

    #Voice
        self.createTitle((o, h), 'Voice', columnspan = 2)
        self.createText((o, h+1), 'Assign Mode')
        self.assign = self.createDropdown((o+1, h+1), ['Poly 1', 'Poly 2', 'Unison'], start = 'Poly 1')
        self.createText((o, h+2), 'Uni Voices')
        self.unia = self.createDropdown((o+1, h+2), [1,2,4,8], start = 4)
        self.createText((o, h+3), 'Uni Detune')
        self.unid = self.createSlider((o+1, h+3), [0,7], start = 4)
