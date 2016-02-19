'''
For TKinter Image-loading help,
thanks to http://stackoverflow.com/questions/4066202
'''

'''
TODO: look up canvas tags
'''

from tkinter import *
from random import randrange, shuffle
from PIL import Image, ImageTk

from Box import Box
from Segments import Segment, Segmentation

hexy = lambda i: hex(i)[2:].rjust(2,'0').upper()
spacings = 'AA 00 55 FF'.split()
mycolors = ['#'+a+b+c for a in spacings for b in spacings for c in spacings]
myletters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-='
mycolors = {l:mycolors[i] for i,l in enumerate(myletters)}

class Annotater:
    def __init__(self, filename):
        self.boxmode=False
        self.annotate(filename)
    def annotate(self, filename):
        self.setup_gui()
        self.filename = filename
        self.refresh_canvas()
        self.load_image()
        self.load()
        self.canvas.pack()
        self.color_label.pack()
        mainloop()
    def setup_gui(self):
        self.master = Tk()
        self.cvsh, self.cvsw = 768, 480
        self.canvas = Canvas(self.master, height=self.cvsh, width=self.cvsw)
        self.color_label = Label(self.master, text='current color')

        self.canvas.bind('<Button-1>', lambda e: self.start_box(e))
        self.canvas.bind('<B1-Motion>', lambda e: self.stretch_box(e))
        self.canvas.bind('<ButtonRelease-1>', lambda e: self.end_box(e))
        self.canvas.bind('<Button-3>', lambda e: self.del_box(e))
        self.master.bind('<Key>', lambda e: self.change_colors(e))
        self.master.bind('<Return>', lambda e: self.write())
        self.master.bind('<Up>', lambda e: self.color_pick(e))
    def start_box(self,event):
        if self.title_box(event):
            return True
        self.boxmode=True
        self.start = [event.x,event.y]; self.end = self.start[:]
        self.boxids[self.curr_colkey].append(
           self.canvas.create_rectangle(self.start[0],self.start[1],self.end[0],self.end[1],
                                        fill=self.colors[self.curr_colkey], stipple='gray75',activewidth=3)
        )
        self.segtypes[self.boxids[self.curr_colkey][-1]]='text'
    def stretch_box(self,event):
        if not self.boxmode: return
        if not self.boxids[self.curr_colkey]: return
        self.end = [event.x,event.y]
        self.canvas.coords(self.boxids[self.curr_colkey][-1],self.start[0],self.start[1],self.end[0],self.end[1])
    def end_box(self,event):
        if not self.boxmode: return
        coords = self.canvas.coords(self.boxids[self.curr_colkey][-1])
        print('created rectangle at', '(', *coords ,')')
        if (coords[2]-coords[0])*(coords[3]-coords[1])<100.0:
           print('   ... but too small so deleted')
           self.canvas.delete(self.boxids[self.curr_colkey][-1])
           self.boxids[self.curr_colkey].pop()
        self.boxmode=False
    def del_box(self,event):
        for c in list(self.colors.keys()): #comment to right is false #current color is first to be searched [so we have shallow history]
            for mb in self.boxids[c][::-1]:
                x0,y0,x1,y1 = self.canvas.coords(mb)
                if x0 <= event.x < x1 and\
                   y0 <= event.y < y1:
                   print('deleted rectangle at', '(',x0,y0,x1,y1 ,')')
                   self.canvas.delete(mb)
                   self.boxids[c].remove(mb)
                   return
    def title_box(self,event):
        for c in list(self.colors.keys()):
            for mb in self.boxids[c][::-1]:
                x0,y0,x1,y1 = self.canvas.coords(mb)
                if x0 <= event.x < x1 and\
                   y0 <= event.y < y1:
                   print('toggled titling of rectangle at', '(',x0,y0,x1,y1 ,')')
                   psts = 'text title other'.split()
                   self.segtypes[mb] = psts[(psts.index(self.segtypes[mb])+1)%len(psts)]
                   #self.segtypes[mb] = 'title' if self.segtypes[mb]=='text' else 'text'
                   stipple = 'gray75' if self.segtypes[mb]=='text' else 'gray25' if self.segtypes[mb]=='title' else ''
                   self.canvas.itemconfig(mb, stipple=stipple)
                   return True
        return False
    def color_pick(self,event):
        for c in list(self.colors.keys()):
            for mb in self.boxids[c][::-1]:
                x0,y0,x1,y1 = self.canvas.coords(mb)
                if x0 <= event.x < x1 and\
                   y0 <= event.y < y1:
                   print('picking up color of rectangle at', '(',x0,y0,x1,y1 ,')')
                   self.curr_colkey = c
                   self.color_label.config(bg=self.colors[self.curr_colkey])
    def change_colors(self,event):
        c = event.char;
        if not c.isalnum(): return
        if c not in self.colors.keys():
            self.colors[c] = mycolors[c]
            self.boxids[c] = []
        self.curr_colkey = c
        self.color_label.config(bg=self.colors[self.curr_colkey])
    def write(self):
        splice = lambda coor4: ([coor4[1],coor4[0]],[coor4[3],coor4[2]])
        from_id = lambda bid: self.canvas.coords(bid)
        S = Segmentation([Segment([Box(*splice(from_id(bid))) for bid in self.boxids[c]],
                                  segtype=self.segtypes[self.boxids[c][0]]) for c in self.colors.keys() if self.boxids[c]])
        #S = Segmentation([Segment([Box(*splice(from_id(bid))) for bid in self.boxids[c]]) for c in self.colors.keys() if c in 'qwe'])
        #S2 = Segmentation([Segment([Box(*splice(from_id(bid))) for bid in self.boxids[c]]) for c in self.colors.keys() if c in 'iop'])
        #print('PPP=',S2.similarity_IU2(S))
        #print('APJ=',S2.similarity_jaccard(S))
        print('writing...')
        with open(self.filename+'.demo.txt','w') as f:
            f.write(str(S))
    def load(self):
        with open(self.filename+'.demo.txt','r') as f:
            S = Segmentation(string=f.read())
        i = 0; y ='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        for s in S.segments:
            stipple = 'gray75' if s.segtype=='text' else 'gray25' if s.segtype=='title' else ''
            for b in s.boxes:
                print('reading...', *b.coors)
                self.boxids[self.curr_colkey].append(
                   self.canvas.create_rectangle(b.coors[0][1],b.coors[0][0],b.coors[1][1],b.coors[1][0],
                                                fill=self.colors[self.curr_colkey], stipple=stipple, activewidth=3)
                )
                self.segtypes[self.boxids[self.curr_colkey][-1]]=s.segtype
            i += 1
            c = y[i]
            self.colors[c] = mycolors[c]
            self.boxids[c] = []
            self.curr_colkey = c
    def refresh_canvas(self):
        self.canvas.delete('all')
        self.curr_colkey = 'q'
        self.colors = {self.curr_colkey:mycolors[self.curr_colkey]}
        self.color_label.config(bg=self.colors[self.curr_colkey])
        self.boxids = {self.curr_colkey:[]}
        self.segtypes = {}
        self.start, self.end = None, None

        self.load_image()
    def load_image(self):
        self.image = Image.open(self.filename)
        self.image = self.image.resize((self.cvsw-5, self.cvsh-5), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.cvsw/2,self.cvsh/2, image=self.image)
