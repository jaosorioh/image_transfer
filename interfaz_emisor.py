from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog 

from emisor import Sender 

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import numpy as np
import threading  

root = Tk()
var = StringVar(root)

figure = Figure(figsize=(4, 4))
plot = figure.add_subplot(1, 1, 1)
plot.set_yticklabels([])
plot.set_xticklabels([])

canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().grid(row=0, column=3, rowspan=7)
running = True
bw = []
def removealpha(image):
 # image.convert("RGBA") # Convert this to RGBA if possible
  pixel_data = image.load()

  if image.mode == "RGBA":
    # If the image has an alpha channel, convert it to white
    # Otherwise we'll get weird pixels
    for y in range(image.size[1]): # For each row ...
      for x in range(image.size[0]): # Iterate through each column ...
        # Check if it's opaque
        if pixel_data[x, y][3] < 255:
          # Replace the pixel data with the colour white
          pixel_data[x, y] = (255, 255, 255, 255)
  return image

def load():
    var.set(tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*"))))
    root.update_idletasks() 
    global bw
    bw = removealpha(Image.open(var.get()).convert("RGBA")).convert('1')
    plot.imshow(bw)
    canvas.draw()

def send():
    duration = float(t1.get())
    start_f = float(t4.get())
    stop_f = float(t5.get())
    freqs = np.array([t2.get(), t3.get()]).astype("float")
    emit = Sender(duration = duration)
    emit.send(start_f)
    array = np.array(bw).astype("int")
    global running
    running = True
    def run():
        for row in array:
            for col in row:
                if(running == False):
                    emit.stop()
                    break
                else:
                    emit.send(freqs[col])
            if(running == False):
                break
        emit.send(stop_f)
    thread = threading.Thread(target=run)  
    thread.start() 
    
def stop():
    global running
    running = False
    
lbl0 = Label(root, text="Image")
lbl0.grid(row=0, column=0)
t0=Entry(textvariable=var)
t0.grid(row=0, column=1)

btn1=Button(root,text="Load", command=load)
btn1.grid(row=0,column=2)

lbl1 = Label(root, text="Duration")
lbl1.grid(row=1, column=0)
t1=Entry()
t1.grid(row=1, column=1)

lbl2 = Label(root, text="0-Freq")
lbl2.grid(row=2, column=0)
t2=Entry()
t2.grid(row=2, column=1)

lbl3 = Label(root, text="1-Freq")
lbl3.grid(row=3, column=0)
t3=Entry()
t3.grid(row=3, column=1)

lbl4 = Label(root, text="Start-Freq")
lbl4.grid(row=4, column=0)
t4=Entry()
t4.grid(row=4, column=1)

lbl5 = Label(root, text="Stop-Freq")
lbl5.grid(row=5, column=0)
t5=Entry()
t5.grid(row=5, column=1)

btn2=Button(root,text="Send", command=send)
btn2.grid(row=6,column=0)

btn3=Button(root,text="Stop", command=stop)
btn3.grid(row=6,column=2)

root.mainloop()