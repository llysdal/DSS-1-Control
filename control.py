from tkinter import *


def updateTask():
    app.after(10, updateTask)




#GUI
class Application(Frame):
    def __init__(self):
        Frame.__init__(self, None)
        self.grid(sticky=N+S+E+W)
        #Resizeability
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

    def createCanvas(self, gridpos, span = 1, size = (100,100)):
        canvas = Canvas(self, width = size[0], height = size[1], bg = 'black')
        canvas.grid(row = gridpos[0], column = gridpos[1], columnspan = span, sticky = N+S+E+W)

        return canvas
    
    def createSlider(self, gridpos, val, res = 1, start = 0, length = 100, width = 15, orient = 0, span = (1,1), showvalue = True):
        slider = Scale(self, from_ = val[0], to = val[1], resolution = res,\
                       orient = (HORIZONTAL, VERTICAL)[orient], length = length, showvalue = showvalue, width = width)
        slider.grid(row = gridpos[0], column = gridpos[1], rowspan = span[0], columnspan = span[1], sticky = W)
        
        slider.set(start)

        return slider
        
    def createDropdown(self, gridpos, values = [1,2,3], start = 1, columnspan = 1):
        string = StringVar()
        string.set(start)
    
        dropdown = OptionMenu(self, string, *values)
        dropdown.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, sticky = W)
        
        return string
        
    def createButton(self, gridpos, text, function):
        button = Button(self, text = text, command = function)
        button.grid(row = gridpos[0], column = gridpos[1], stick = N+S+E+W)
    
    def createText(self, gridpos, text, size = 12, columnspan = 1, stick = W):
        label = Label(self, text = text, font = ('Helvetica', size), justify = 'left')
        label.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, sticky = stick)
        
        return label
        
    def createDynText(self, gridpos, stick = 0, size = 12, columnspan = 1):
        stringvar = StringVar()
        
        label = Label(self, textvariable = stringvar, font = ('Helvetica', size), justify = 'left')
        label.grid(row = gridpos[0], column = gridpos[1], columnspan = columnspan, sticky = (E, W)[stick])

        return stringvar
       
app = Application()
app.master.title('DSS-1 Control')

#Oscillator 1
app.createText((0,0), 'Oscillator 1', columnspan = 2, stick = E+W)
app.createText((1,0), 'Multisound')
osc1w  = app.createDropdown((1,1), range(1,17), start = 1)
app.createText((2,0), 'Octave')
osc1o  = app.createDropdown((2,1), [4,8,16], start = 8)
app.createText((3,0), 'D/A Resolution')
oscres = app.createDropdown((3,1), ['6 bits', '7 bits', '8 bits', '10 bits', '12 bits'], start = '12 bits')

#Oscillator 2
app.createText((0,3), 'Oscillator 2', columnspan = 2, stick = E+W)
app.createText((1,3), 'Multisound')
osc2w  = app.createDropdown((1,4), range(1,17), start = 1)
app.createText((2,3), 'Octave')
osc2o  = app.createDropdown((2,4), [4,8,16], start = 8)
app.createText((3,3), 'Interval')
osc2i  = app.createSlider((3,4), (0,12), start = 0)
app.createText((4,3), 'Detune')
osc2d  = app.createSlider((4,4), (0,63), start = 0)




app.master.protocol("WM_DELETE_WINDOW", lambda: quit())
updateTask()
app.master.mainloop()
