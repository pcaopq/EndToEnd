from tkinter import *

master = Tk()
w = Canvas(master, width=640, height=480)
start, end = None, None
def click_callback(event):
    global start,end
    start = [event.x,event.y]
    print('clicked at', start)
def release_callback(event):
    global start,end
    end = [event.x,event.y]
    print('released at', end)
    w.delete('all')
    w.create_rectangle(start[0], start[1], end[0], end[1], fill="blue")


w.bind('<Button-1>', click_callback)
w.bind('<ButtonRelease-1>', release_callback)
w.pack()

mainloop()
