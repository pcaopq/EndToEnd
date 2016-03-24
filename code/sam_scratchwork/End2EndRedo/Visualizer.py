'''@author Samuel Tenka
'''

from tkinter import *

from random import random as rn
from math import sqrt, pi
tri=.8660
dist = lambda rgb,RGB: sum((c-C)**2 for c,C in zip(rgb,RGB))
def generate_colors():
    '''Generator of RGB values, with no two colors unnecessarily close.
       Highly inefficient (consider the redundant computation due to
       bad flow control and lack of memory-use!),
       but not called from any time-critical functions.
    '''
    past_colors = []
    while True:
        max_distance = sqrt(tri/(len(past_colors)+1) / pi)
        rgb = rn(),rn(),rn()
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

class Visualizer:
    def __init__(self,image_name):
        self.setup_gui()
        h,w = size_of_image(image_name)
        self.hs,self.ws = 640.0/h,480.0/w
    def setup_gui(self):
        self.master = Tk()
        self.canvas = Canvas(self.master, height=640+20, width=480+20)
        self.canvas.pack()
    def refresh_canvas(self):
        self.canvas.delete('all')
    def draw_box(self, box, color, content_class, activewidth=3):
        (y,x),(Y,X) = box.coors
        st,ast = ('gray75','gray50') if content_class=='title' else ('gray25','gray12')
        self.canvas.create_rectangle(x*self.ws+10,y*self.hs+10,X*self.ws+10,Y*self.hs+10, fill=color, stipple=st, activestipple=ast, activewidth=activewidth)
    def display(self, segmentation):
        self.refresh_canvas()
        self.load_background('0003.jpg')
        for a,col in zip(segmentation.articles,generate_colors()):
            for content_class, p in a.polygons_by_type.items():
                for b in p.boxes:
                    self.draw_box(b, col, content_class)
        mainloop()
    def load_background(self, image_name):
        self.image = Image.open(image_name)
        self.image = self.image.resize((480, 640), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(480/2 + 10,640/2 + 10, image=self.image)

from Segmentation import Segmentation
S = Segmentation('0003.json')
V = Visualizer('0003.jpg')
V.display(S)
