'''@author Samuel Tenka.
   Thanks to
   http://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
'''

from tkinter import *

from random import random, seed
from math import sqrt, pi
tri=.8660
dist = lambda rgb,RGB: sum((c-C)**2 for c,C in zip(rgb,RGB))
def generate_colors():
    '''Generator of RGB values, with no two colors unnecessarily close.
       Highly inefficient (consider the redundant computation due to
       bad flow control and lack of memory-use!),
       but not called from any time-critical functions.
    '''
    seed(0)
    past_colors = []
    while True:
        max_distance = sqrt(tri/(len(past_colors)+1) / pi)
        rgb = random(),random(),random()
        rgb=tuple(c/sum(rgb) for c in rgb)
        for pc in past_colors:
            if dist(rgb,pc)<max_distance: break
        else:
            past_colors.append(tuple(int(c*256) for c in rgb))
            yield '#%02x%02x%02x' % past_colors[-1]

from PIL import Image, ImageTk
def size_of_image(image_name):
    im=Image.open(image_name)
    return im.size[::-1] #[height,width]

from random import random
class ResizingCanvas(Canvas):
    ''' A subclass of Canvas for dealing with resizing of windows
        Thanks to
        http://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
    '''
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        scale_h = float(event.height)/self.height
        scale_w = float(event.width)/self.width
        self.height = event.height
        self.width = event.width
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,scale_w,scale_h)

from Segmentation import Segmentation
class Visualizer:
    def __init__(self, image_name, json_name):
        self.imagedims = None
        self.setup_gui(image_name, json_name)
    def setup_gui(self, image_name, json_name):
        self.master = Tk()
        self.canvas = ResizingCanvas(self.master, height=800+2, width=600+2)
        self.canvas.pack(fill=BOTH,expand=YES)
        b = Button(self.master, text="display", command=self.display); b.pack()
        self.image_name_entry = Entry(self.master); self.image_name_entry.pack()
        self.image_name_entry.insert(0,image_name)
        self.json_name_entry = Entry(self.master); self.json_name_entry.pack()
        self.json_name_entry.insert(0,json_name)

    def refresh_canvas(self):
        self.canvas.delete('boxes')
    def draw_box(self, box, color, content_class, activewidth=3):
        (y,x),(Y,X) = box.coors; hs,ws = self.scale_h, self.scale_w
        st,ast = ('@.\\title.xbm','@.\\clear.xbm') if content_class=='title' else ('@.\\article.xbm','@.\\clear.xbm')
        self.canvas.create_rectangle(x*ws+1,y*hs+1,X*ws+1,Y*hs+1, tag='boxes',
                                     outline=color, fill=color, width=2, stipple=st, activestipple=ast, activewidth=activewidth)
    def display(self):
        self.refresh_canvas()
        h,w = size_of_image(self.image_name_entry.get())
        self.scale_h, self.scale_w = self.canvas.height/h, self.canvas.width/w
        self.load_background()

        seg = Segmentation(self.json_name_entry.get())
        for a,col in zip(seg.articles,generate_colors()):
            for content_class, p in a.polygons_by_type.items():
                if content_class not in ('title','article'):continue
                for b in p.boxes:
                    self.draw_box(b, col, content_class)
        mainloop()
    def load_background(self):
        h,w = self.canvas.height,self.canvas.width#self.canvas.winfo_reqheight(), self.canvas.winfo_reqwidth()
        image_name=self.image_name_entry.get()
        if (h,w,image_name)==self.imagedims: return
        self.canvas.delete('image')
        self.image = Image.open(image_name)
        self.image = self.image.resize((w, h), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(w/2 + 1,h/2 + 1, image=self.image, tag='image')
        self.imagedims = (h,w,image_name)

import sys
if __name__=='__main__':
    image_name,json_name = sys.argv[1:3]
    V = Visualizer(image_name,json_name)
    V.display()
