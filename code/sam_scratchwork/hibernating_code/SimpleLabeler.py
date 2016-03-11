from tkinter import *
from random import randrange
from PIL import Image, ImageTk

'''Thanks to http://stackoverflow.com/questions/4066202'''
master = Tk()
w = Canvas(master, width=400, height=640)
image = Image.open('Data\\0005.jpg')
image = image.resize((390, 630), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
w.create_image(400/2,640/2, image=img)

#TODO: don't change colors when mouse is down!

from Box import Box
from Segments import Segment, Segmentation
def write_to(filename):
    print('saving..')
    def get_coors(mbid):
        mbcoors = w.coords(mbid)
        return (mbcoors[1::2],mbcoors[::2])
    S = Segmentation([Segment([Box(*get_coors(b)) for b in myboxes[c]]) for c in mycolors.keys()])
    with open(filename,'w') as f:
        f.write(str(S))

def randcolor():
    return '#'+''.join(hex(randrange(0,256,16))[2:].rjust(0) for i in range(3))
def key_callback(event):
    global mycolors, curr_colkey
    c = event.char; print('pressed',c)
    if not c.isalnum(): return
    if c not in mycolors.keys():
        mycolors[c] = randcolor()
        myboxes[c] = []
    curr_colkey = c

def click_callback(event):
    global start,end, curr_colkey
    start = [event.x,event.y]
    end = start[:]
    print('clicked at', start)
    myboxes[curr_colkey].append(w.create_rectangle(start[0],start[1],end[0],end[1],
                               fill=mycolors[curr_colkey], stipple='gray75'))
def move_callback(event):
    global start,end, myboxes
    end = [event.x,event.y]
    print('move at', end)
    w.coords(myboxes[curr_colkey][-1],start[0],start[1],end[0],end[1])
def release_callback(event):
    global start,end
    print('created rectangle from', start, 'to', end, '(',w.coords(myboxes[curr_colkey][-1]) ,')')
def click3_callback(event): #TODO: optimize with kd trees
    global myboxes
    print('click3 at', event.x, event.y)
    for c in list(mycolors.keys()): #current color is first to be searched [so we have shallow history]
        for mb in myboxes[c][::-1]:
            x0,y0,x1,y1 = w.coords(mb)
            if x0 <= event.x < x1 and\
               y0 <= event.y < y1:
               w.delete(mb)
               myboxes[c].remove(mb)
               return
def return_callback(event):
    write_to('save.txt')

w.bind('<Button-1>', click_callback)
w.bind('<B1-Motion>', move_callback)
w.bind('<ButtonRelease-1>', release_callback)
w.bind('<Button-3>', click3_callback)
master.bind('<Key>', key_callback)
master.bind('<Return>', return_callback)
w.pack()

mainloop()
