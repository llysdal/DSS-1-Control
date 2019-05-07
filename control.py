from tkinter import *
import os

curDir = os.path.dirname(os.path.abspath(__file__))

class Application(Frame):
    def init(self, titlefont, textfont, numberfont):
        Frame.__init__(self, None)
        self.grid(sticky=N+S+E+W)

        #Resizeability
        self.top = self.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        self.black = "#212121"
        self.grey  = '#2e2e2e'
        self.white = '#e2e2e2'
        self.blue  = '#336ece'

        self.titlefont = titlefont
        self.textfont = textfont
        self.numberfont = numberfont

        self.configure(background = self.grey)

    def createCanvas(self, gridpos, columnspan = 1, rowspan = 1, size = (100,100)):
        canvas = Canvas(self, width = size[0], height = size[1], bg = 'black')
        canvas.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, rowspan = rowspan, sticky = N+S+E+W)

        return canvas
    
    def createSlider(self, gridpos, val, res = 1, start = 0, length = 100, width = 15, orient = 0, span = (1,1), showvalue = True, stick = E+S):
        slider = Scale(self, from_ = val[0], to = val[1], resolution = res,\
                       orient = (HORIZONTAL, VERTICAL)[orient], length = length, showvalue = showvalue, width = width)
        slider.configure(background = self.black, foreground = self.white, highlightthickness = 0, troughcolor = self.grey, activebackground = self.white, font = self.numberfont)
        slider.grid(row = gridpos[0], column = gridpos[1], rowspan = span[0], columnspan = span[1], sticky = stick)
        
        slider.set(start)

        return slider
        
    def createDropdown(self, gridpos, values = [1,2,3], start = 1, columnspan = 1):
        string = StringVar()
        string.set(start)
    
        dropdown = OptionMenu(self, string, *values)
        dropdown.configure(background = self.black, foreground = self.white, highlightthickness = 0, borderwidth = 2, activebackground = self.blue)
        dropdown.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, sticky = E+S)
        
        return string
        
    def createButton(self, gridpos, text, function):
        button = Button(self, text = text, command = function)
        button.configure(background = self.black, foreground = self.white)
        button.grid(row = gridpos[0], column = gridpos[1], stick = N+S+E+W)
    
    def createText(self, gridpos, text, columnspan = 1, stick = W+S):
        label = Label(self, text = text, font = self.textfont, justify = 'left')
        label.configure(background = self.black, foreground = self.white)
        label.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, sticky = stick)
        
        return label

    def createTitle(self, gridpos, text, columnspan = 1):
        label = Label(self, text = text, font = self.titlefont, justify = 'left')
        label.configure(background = self.black, foreground = self.white)
        label.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, sticky = E+W)
        
        return label
        
    def createDynText(self, gridpos, stick = 0, size = 12, columnspan = 1):
        stringvar = StringVar()
        
        label = Label(self, textvariable = stringvar, font = ('Helvetica', size), justify = 'left')
        label.configure(background = self.black, foreground = self.white)
        label.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, sticky = (E, W)[stick])

        return stringvar

    def createCheckbutton(self, gridpos, text, columnspan = 1):
        intvar = IntVar()

        button = Checkbutton(self, text = text, variable = intvar, onvalue = 1, offvalue = 0)
        button.configure(background = self.black, activebackground = self.blue)
        button.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, sticky = E+S)

        return intvar

    def createMenu(self):
        menubar = Menu(self)
        self.top.config(menu=menubar)

        return menubar

    def minSizeH(self, pos, width):
        self.columnconfigure(pos, minsize = width)
        
    def minSizeV(self, pos, width):
        self.rowconfigure(pos, minsize = width)
       
class DSS1gui(Application):
    def __init__(self, titlefont, textfont, numberfont):
        self.init(titlefont, textfont, numberfont)
        self.menu = self.createMenu()
        self.setup()

        self.execcommand = 0


    def egCanvas(self, canvas, egpar):
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
        self.osc1w.set(values[58]+1)
        self.osc2w.set(values[59]+1)
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
                int(self.osc1w.get())-1,
                int(self.osc2w.get())-1,
                12,                     #?
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

#Gui
    #Gui setup, this is gonna be long
    #Dont touch anything here please
    def setup(self):
        self.master.title('DSS-1 Main Control')

        self.menu.add_command(label='Get Parameters', command = lambda: self.execCom('getparameters'))
        self.menu.add_command(label='Set Parameters', command = lambda: self.execCom('setparameters'))
        self.menu.add_command(label='Save Program', command = lambda: self.execCom('saveprogram'))

        #Background
        backimage = PhotoImage(file = curDir + '/background.png')
        backlabel = Label(self, image=backimage, bd = 0)
        backlabel.place(x=0, y=0)
        backlabel.image = backimage


        self.minSizeH((0,0), 5)
        self.minSizeH((0,33), 5)
        self.minSizeV((28,0), 5)

    #Program management
        self.createText((0,1), 'Program', stick = W+N)
        self.prog = Spinbox(self, from_=1, to=32, width = 2, command = lambda: self.execCom('updatename'))
        self.prog.grid(row = 0, column = 2, sticky = E+N)

        self.progname = Entry(self, width = 10)
        self.progname.grid(row = 0, column = 3, sticky = W+N)

        o = 1
    #Autobend
        self.createTitle((10,o), 'Autobend', columnspan = 2)
        self.createText((11,o), 'Mode')
        self.autom = self.createDropdown((11,o+1), ['Off', 'Osc1', 'Osc2', 'Both'], start = 'Both')
        self.createText((12,o), 'Polarity')
        self.autop = self.createDropdown((12,o+1), ['Down', 'Up'], start = 'Up')
        self.createText((13,o), 'Intensity')
        self.autoi = self.createSlider((13,o+1), (0,127), start = 0)
        self.createText((14,o), 'Time')
        self.autot = self.createSlider((14,o+1), (0,31), start = 0)
        self.minSizeH((0,o+1), 80)
        o += 2

        #Gap
        self.minSizeH((0,o), 30)
        o += 1

    #Oscillator 1
        self.createTitle((10,o), 'Oscillator 1', columnspan = 2)
        self.createText((11,o), 'Multisound')
        self.osc1w  = self.createDropdown((11,o+1), range(1,16), start = 1)
        self.createText((12,o), 'Octave')
        self.osc1o  = self.createDropdown((12,o+1), [4,8,16], start = 8)
        self.createText((14,o), 'D/A Resolution')
        self.oscres = self.createDropdown((14,o+1), ['6 bits', '7 bits', '8 bits', '10 bits', '12 bits'], start = '12 bits')
        self.minSizeH((0,o+1), 80)
        o += 2

        #Gap
        self.minSizeH((0,o), 20)
        o += 1

    #Oscillator 2
        self.createTitle((10,o), 'Oscillator 2', columnspan = 2)
        self.createText((11,o), 'Multisound')
        self.osc2w = self.createDropdown((11,o+1), range(1,17), start = 1)
        self.createText((12,o), 'Octave')
        self.osc2o = self.createDropdown((12,o+1), [4,8,16], start = 8)
        self.createText((13,o), 'Interval')
        self.osc2i = self.createSlider((13,o+1), (0,11), start = 0)
        self.createText((14,o), 'Detune')
        self.osc2d = self.createSlider((14,o+1), (0,63), start = 0)
        self.createText((15,o), 'Sync')
        self.osc2s = self.createCheckbutton((15,o+1), text = '')
        o += 2

        #Gap
        self.minSizeH((0,o), 30)
        o += 1

    #Mixer
        self.createTitle((10,o), 'Mixer', columnspan = 3)
        self.createText((14,o), '1', stick = E+S)
        self.osc1v = self.createSlider((11,o), (100,0), start = 100, orient = 1, span = (3,1))
        self.createText((14,o+1), '2', stick = E+S)
        self.osc2v = self.createSlider((11,o+1), (100,0), start = 0, orient = 1, span = (3,1))
        self.createText((14,o+2), 'Noise', stick = E+S)
        self.noise = self.createSlider((11,o+2), (63,0), start = 0, orient = 1, span = (3,1))
        o += 3

        #Gap
        self.minSizeH((0,o), 30)
        o += 1

    #Filter
        self.createTitle((10,o), 'Filter', columnspan = 6)
        self.createText((11,o), 'Mode', columnspan = 3)
        self.filterm = self.createDropdown((11,o+3), ['12dB', '24dB'], start = '24dB', columnspan = 3)
        self.createText((12,o), 'Cutoff', columnspan = 3)
        self.filterc = self.createSlider((12,o+3), (0,127), start = 127, span=(1,3))
        self.createText((13,o), 'Resonance', columnspan = 3)
        self.filterr = self.createSlider((13,o+3), (0,63), start = 0, span=(1,3))
        self.createText((14,o), 'KBD Track', columnspan = 3)
        self.filterk = self.createSlider((14,o+3), (0,63), start = 0, span=(1,3))
        self.createText((15, o), 'Filter EG', columnspan = 3)
        self.filtereg = self.createSlider((15,o+3), (0,63), start = 0, span=(1,3))
        self.createText((16, o), 'EG Invert', columnspan = 3)
        self.filterinv = self.createCheckbutton((16,o+3), text = '', columnspan = 3)

    #Filter EG
        self.egfc = self.createCanvas((17,o), columnspan = 6, rowspan = 2, size=(225,100))
        self.egfa = self.createSlider((19,o),   (63,0), start = 0, orient = 1, span=(2,1))
        self.egfd = self.createSlider((19,o+1), (63,0), start = 0, orient = 1, span=(2,1))
        self.egfb = self.createSlider((19,o+2), (63,0), start = 0, orient = 1, span=(2,1))
        self.egfsl= self.createSlider((19,o+3), (63,0), start = 0, orient = 1, span=(2,1))
        self.egfs = self.createSlider((19,o+4), (63,0), start = 0, orient = 1, span=(2,1))
        self.egfr = self.createSlider((19,o+5), (63,0), start = 0, orient = 1, span=(2,1))
        o += 6

        #Gap
        self.minSizeH((0,o), 30)
        o += 1

    #VCA
        self.createTitle((10,o), 'VCA', columnspan = 6)
        self.createText((11,o), 'Level', columnspan = 3)
        self.vcal = self.createSlider((11,o+3), (0,63), start = 63, span=(1,3))
        self.createText((12,o), 'KBD Decay', columnspan = 3)
        self.vcad = self.createSlider((12, o+3), (-63,63), start = 0, span=(1,3))
        self.createText((13,o), 'Treble', columnspan = 3)
        self.treb = self.createSlider((13, o+3), (-4,8), start = 0, span=(1,3))
        self.createText((14,o), 'Bass', columnspan = 3)
        self.bass = self.createSlider((14, o+3), (-4,8), start = 0, span=(1,3))
  
    #VCA EG
        self.egvc = self.createCanvas((17,o), columnspan = 6, rowspan = 2, size=(225,100))
        self.egva = self.createSlider((19,o),   (63,0), start = 0, orient = 1, span=(2,1))
        self.egvd = self.createSlider((19,o+1), (63,0), start = 0, orient = 1, span=(2,1))
        self.egvb = self.createSlider((19,o+2), (63,0), start = 0, orient = 1, span=(2,1))
        self.egvsl= self.createSlider((19,o+3), (63,0), start = 0, orient = 1, span=(2,1))
        self.egvs = self.createSlider((19,o+4), (63,0), start = 0, orient = 1, span=(2,1))
        self.egvr = self.createSlider((19,o+5), (63,0), start = 0, orient = 1, span=(2,1))
        o += 6

        #Gap
        self.minSizeH((0,o), 30)
        o += 1

    #Delay 1
        self.createTitle((10,o), 'Delay 1', columnspan = 2)
        self.createText((11,o), 'Time')
        self.d1t = self.createSlider((11,o+1), (0,500), start = 200)
        self.createText((12,o), 'Feedback')
        self.d1f = self.createSlider((12,o+1), (0,15), start = 0)
        self.createText((13,o), 'Effect Level')
        self.d1e = self.createSlider((13,o+1), (0,15), start = 0)
        o += 2

        #Gap
        self.minSizeH((0,o), 20)
        o += 1

    #Delay 2
        self.createTitle((10,o), 'Delay 2', columnspan = 2)
        self.createText((11,o), 'Time')
        self.d2t = self.createSlider((11,o+1), (0,500), start = 200)
        self.createText((12,o), 'Feedback')
        self.d2f = self.createSlider((12,o+1), (0,15), start = 0)
        self.createText((13,o), 'Effect Level')
        self.d2e = self.createSlider((13,o+1), (0,15), start = 0)
        self.createText((14,o), 'Source')
        self.d2s = self.createDropdown((14,o+1), ['Direct', 'Delay 1'], start = 'Direct')
        self.createText((15,o), 'Mod Invert')
        self.d2mi = self.createCheckbutton((15,o+1), text = '')

    #MOD Section
        o = 4
        h = 16

    #MG
        self.createTitle((h,o), 'Osc MG', columnspan = 2)
        self.createText((h+1,o), 'Frequency')
        self.omgf = self.createSlider((h+1,o+1), (0,31), start = 0)
        self.createText((h+2,o), 'Intensity')
        self.omgi = self.createSlider((h+2,o+1), (0,15), start = 0)
        self.createText((h+3,o), 'Delay')
        self.omgd = self.createSlider((h+3,o+1), (0,15), start = 0)
        self.createText((h+4,o), 'Mode')
        self.omgm = self.createDropdown((h+4,o+1), ['Off', 'Osc1', 'Osc2', 'Both'], start = 'Both')
       
        o += 3

        self.createTitle((h,o), 'Filter MG', columnspan = 2)
        self.createText((h+1,o), 'Frequency')
        self.fmgf = self.createSlider((h+1,o+1), (0,63), start = 0)
        self.createText((h+2,o), 'Intensity')
        self.fmgi = self.createSlider((h+2,o+1), (0,63), start = 0)
        self.createText((h+3,o), 'Delay')
        self.fmgd = self.createSlider((h+3,o+1), (0,63), start = 0)

        o += 21

    #DDL MG
        self.createTitle((h,o), 'MG A', columnspan = 2)
        self.createText((h+1,o), 'Frequency')
        self.mgaf = self.createSlider((h+1,o+1), (0,63), start = 20)
        self.createText((h+2,o), 'Delay 1 Mod')
        self.mgam1 = self.createSlider((h+2,o+1), (0,63), start = 0)
        self.createText((h+3,o), 'Delay 2 Mod')
        self.mgam2 = self.createSlider((h+3,o+1), (0,63), start = 0)
        o += 3

        self.createTitle((h,o), 'MG B', columnspan = 2)
        self.createText((h+1,o), 'Frequency')
        self.mgbf = self.createSlider((h+1,o+1), (0,63), start = 20)
        self.createText((h+2,o), 'Delay 1 Mod')
        self.mgbm1 = self.createSlider((h+2,o+1), (0,63), start = 0)
        self.createText((h+3,o), 'Delay 2 Mod')
        self.mgbm2 = self.createSlider((h+3,o+1), (0,63), start = 0)

    #Velocity Sensitive
        o = 1
        h = 22

        self.minSizeV((h-1,0), 50)

        self.createTitle((h,o), 'Velocity Sensitive', columnspan = 8)

        self.createText((h+1,o), 'Autobend Int ')
        self.vela = self.createSlider((h+1,o+1), (0,63), start = 0)
        self.createText((h+2,o), 'X-mod')
        self.oscx = self.createSlider((h+2,o+1), (0,31), start = 0)

        self.createText((h+1, o+3), 'Filter Cutoff')
        self.velfc = self.createSlider((h+1,o+4), (0,63), start = 0)
        self.createText((h+2, o+3), 'Filter EG Attack')
        self.velfa = self.createSlider((h+2,o+4), (0,63), start = 0)
        self.createText((h+3, o+3), 'Filter EG Decay')
        self.velfd = self.createSlider((h+3,o+4), (0,63), start = 0)
        self.createText((h+4, o+3), 'Filter EG Slope')
        self.velfs = self.createSlider((h+4,o+4), (0,63), start = 0)

        self.createText((h+1, o+6), 'VCA Level')
        self.velvl = self.createSlider((h+1,o+7), (0,63), start = 0)
        self.createText((h+2, o+6), 'VCA EG Attack')
        self.velva = self.createSlider((h+2,o+7), (0,63), start = 0)
        self.createText((h+3, o+6), 'VCA EG Decay')
        self.velvd = self.createSlider((h+3,o+7), (0,63), start = 0)
        self.createText((h+4, o+6), 'VCA EG Slope')
        self.velvs = self.createSlider((h+4,o+7), (0,63), start = 0)
        o += 7
        o += 6

    #Aftertouch 
        self.createTitle((h,o), 'Aftertouch', columnspan = 6)
        self.createText((h+1,o), 'Osc MG Int', columnspan = 3)
        self.aftmgi = self.createSlider((h+1,o+3), (0,15), start = 0, span = (1,3))
        self.createText((h+2,o), 'Filter', columnspan = 3)
        self.aftf = self.createSlider((h+2,o+3), (0,15), start = 0, span = (1,3))
        self.createText((h+3,o), 'Filter Mod', columnspan = 3)
        self.aftfm = self.createDropdown((h+3,o+3), ['MG Int', 'Cutoff'], start = 'MG Int', columnspan = 3)
        self.createText((h+4,o), 'VCA Level', columnspan = 3)
        self.aftvl = self.createSlider((h+4,o+3), (0,15), start = 0, span = (1,3))
        o += 7

    #Joystick
        self.createTitle((h,o), 'Joystick', columnspan = 6)
        self.createText((h+1,o), 'Range', columnspan = 3)
        self.joyr = self.createSlider((h+1,o+3), (0,12), start = 2, span=(1,3))
        self.createText((h+2,o), 'Filter Control', columnspan = 3)
        self.joyf = self.createCheckbutton((h+2,o+3), text = '', columnspan = 3)
        o += 7

    #Voice
        self.createTitle((h,o), 'Voice', columnspan = 2)
        self.createText((h+1,o), 'Assign Mode')
        self.assign = self.createDropdown((h+1,o+1), ['Poly 1', 'Poly 2', 'Unison'], start = 'Poly 1')
        self.createText((h+2,o), 'Uni Voices')
        self.unia = self.createDropdown((h+2,o+1), [1,2,4,8], start = 4)
        self.createText((h+3,o), 'Uni Detune')
        self.unid = self.createSlider((h+3,o+1), [0,7], start = 4)
