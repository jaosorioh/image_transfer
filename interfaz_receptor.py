from receptor import Listener

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog 
from PIL import Image
import numpy as np
import time
#--------End of imports

root = Tk()

figure = Figure(figsize=(4, 4))
plot = figure.add_subplot(1, 1, 1)
plot.set_yticklabels([])
plot.set_xticklabels([])

data = np.random.randn(16, 16).astype('uint8')*255

im = plot.imshow(data, cmap="gray")

canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().grid(row=0, column=3, rowspan=7)

lbl1 = Label(root, text="Duration")
lbl1.grid(row=0, column=0)
t1=Entry()
t1.grid(row=0, column=1)

lbl2 = Label(root, text="0-Freq")
lbl2.grid(row=1, column=0)
t2=Entry()
t2.grid(row=1, column=1)

lbl3 = Label(root, text="1-Freq")
lbl3.grid(row=2, column=0)
t3=Entry()
t3.grid(row=2, column=1)

lbl4 = Label(root, text="Start-Freq")
lbl4.grid(row=3, column=0)
t4=Entry()
t4.grid(row=3, column=1)

lbl5 = Label(root, text="Stop-Freq")
lbl5.grid(row=4, column=0)
t5=Entry()
t5.grid(row=4, column=1)


def plotter():
    global running
    i = 0
    data = np.zeros((N, N))    
    while(running and i<(N**2)):
        val = recep.listen()
        if(abs(val-stopFreq)<20):
            running = False
        else:
            data[int(i/N), i%N] = int((recep.listen()-minFreq)/(maxFreq-minFreq))
            im.set_data(data.astype('uint8')*255)
            figure.canvas.draw()
            figure.canvas.flush_events() 
            i+=1
    recep.stop()


def start():
    global running, recep, minFreq, maxFreq, stopFreq, im, fig, N
    duration = float(t1.get())
    minFreq = float(t2.get())
    maxFreq = float(t3.get())
    startFreq = float(t4.get())
    stopFreq = float(t5.get())
    N = 32#int(t6.get())
    recep = Listener(duration = duration/4)
    while(abs(recep.listen()-startFreq)>20):
        print("Espere...")
    running = True
    start_time = time.time()
    plotter()
    print("--- %s seconds ---" % (time.time() - start_time))

def stop():
    global running
    running = False

btn1=Button(root,text="Start", command=start)
btn1.grid(row=5,column=0)

btn2=Button(root,text="Stop", command=stop)
btn2.grid(row=5,column=2)

root.mainloop()

    


