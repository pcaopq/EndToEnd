from tkinter import *

#from PIL import Image, ImageTk

master = Tk()
w = Canvas(master, width=336, height=543)
myboxes = []
start, end = None, None
def click_callback(event):
    global start,end
    start = [event.x,event.y]
    print('clicked at', start)
    for mb in myboxes: w.delete(mb)
    myboxes.append(w.create_rectangle(start[0], start[1], start[0], start[1], fill='blue', stipple='gray25'))
def move_callback(event):
    global start,end, myboxes
    end = [event.x,event.y]
    print('move at', end)
    w.coords(myboxes[-1], start[0],start[1],end[0],end[1])
'''def release_callback(event):
    global start,end, myboxes
    end = [event.x,event.y]
    print('released at', end)
    myboxes.append(w.create_rectangle(start[0], start[1], end[0], end[1], fill='blue', stipple='gray25'))
'''
w.bind('<Button-1>', click_callback)
w.bind('<B1-Motion>', move_callback)
'''w.bind('<ButtonRelease-1>', release_callback)'''
w.pack()

img = PhotoImage(file='zoom0.gif')
w.create_image(336/2,543/2, image=img)
#panel = Label(master, image = img)
#panel.pack()

mainloop()
