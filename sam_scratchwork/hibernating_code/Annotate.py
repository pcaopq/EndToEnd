'''
For TKinter Image-loading help,
thanks to http://stackoverflow.com/questions/4066202
'''

from tkinter import *
from random import randrange, shuffle
from PIL import Image, ImageTk

from Box import Box
from Segments import Segment, Segmentation

hexy = lambda i: hex(i)[2:].rjust(2,'0').upper()
mycolors = ['#'+hexy(i)+hexy(j)+hexy(k) for i in range(0,256,32) for j in range(0,256,32) for k in range(0,256,32)][1:]
shuffle(mycolors)
whichcolor = 0
def randcolor(spacing=32):
    global mycolors, whichcolor
    whichcolor += 1
    return mycolors[whichcolor]
    #return '#'+''.join(hex(randrange(0,256,spacing))[2:].rjust(2,'0').upper() for i in range(3))

class Annotater:
    def __init__(self, filename):
        self.annotate(filename)
    def annotate(self, filename):
        self.setup_gui()
        self.filename = filename
        self.refresh_canvas()
        self.load_image()
        self.canvas.pack()
        mainloop()
    def setup_gui(self):
        self.master = Tk()
        self.cvsh, self.cvsw = 768, 480
        self.canvas = Canvas(self.master, height=self.cvsh, width=self.cvsw)

        self.canvas.bind('<Button-1>', lambda e: self.start_box(e))
        self.canvas.bind('<B1-Motion>', lambda e: self.stretch_box(e))
        self.canvas.bind('<ButtonRelease-1>', lambda e: self.end_box(e))
        self.canvas.bind('<Button-3>', lambda e: self.del_box(e))
        self.master.bind('<Key>', lambda e: self.change_colors(e))
        self.master.bind('<Return>', lambda e: self.write())
    def start_box(self,event):
        self.start = [event.x,event.y]; self.end = self.start[:]
        print('clicked at', self.start)
        self.boxids[self.curr_colkey].append(
           self.canvas.create_rectangle(self.start[0],self.start[1],self.end[0],self.end[1],
                                        fill=self.colors[self.curr_colkey], stipple='gray75')
        )
    def stretch_box(self,event):
        if not self.boxids[self.curr_colkey]: return
        self.end = [event.x,event.y]
        self.canvas.coords(self.boxids[self.curr_colkey][-1],self.start[0],self.start[1],self.end[0],self.end[1])
    def end_box(self,event):
        print(self.boxids)
        print('created rectangle at', '(',self.canvas.coords(self.boxids[self.curr_colkey][-1]) ,')')
    def del_box(self,event):
        print('click3 at', event.x, event.y)
        for c in list(self.colors.keys()): #current color is first to be searched [so we have shallow history]
            for mb in self.boxids[c][::-1]:
                x0,y0,x1,y1 = self.canvas.coords(mb)
                if x0 <= event.x < x1 and\
                   y0 <= event.y < y1:
                   self.canvas.delete(mb)
                   self.boxids[c].remove(mb)
                   return
    def change_colors(self,event):
        c = event.char; print('pressed',c)
        if not c.isalnum(): return
        if c not in self.colors.keys():
            self.colors[c] = randcolor()
            self.boxids[c] = []
        self.curr_colkey = c
    def write(self):
        print('saving to %s...', self.filename+'.txt')
        splice = lambda coor4: (coor4[1::2],coor4[::2])
        from_id = lambda bid: self.canvas.coords(bid)
        S = Segmentation([Segment([Box(*splice(from_id(bid))) for bid in self.boxids[c]]) for c in self.colors.keys()])
        with open(self.filename+'.txt','w') as f:
            f.write(str(S))
    def refresh_canvas(self):
        self.canvas.delete('all')
        self.curr_colkey = 'q'
        self.colors = {self.curr_colkey:'#000000'}
        self.boxids = {self.curr_colkey:[]}
        self.start, self.end = None, None

        image = Image.open(self.filename)
        image = image.resize((self.cvsw-5, self.cvsh-5), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.cvsw/2,self.cvsh/2, image=image)
    def load_image(self):
        self.image = Image.open(self.filename)
        self.image = self.image.resize((self.cvsw-5, self.cvsh-5), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.cvsw/2,self.cvsh/2, image=self.image)

Annotater('Data\\0005.jpg')
#Annotater('Data\\0006.jpg')
