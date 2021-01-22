import os
import split
from soundControl import Sound
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import cv2
import ImageTk

cap = None

sound = Sound(5)

def startAction():
    try:
        selectedsong = songs.get(songs.curselection())
    except:
        messagebox.showwarning("No Song","please pick a song")
        return
    sound.startCallback(selectedsong,acc.get()/100,voc.get()/100)
    global cap
    cap = cv2.VideoCapture(f"./songs/{selectedsong}/video.mp4")
    video_stream()
    

def stopAction():
    global cap
    cap = None
    sound.stopCallback()
    video_stream()

def importAction():
    split.importAll()
    sngs = os.listdir("./songs")
    sn = tk.StringVar()
    sn.set([s for s in sngs])
    songs.config(listvariable=sn)
    messagebox.showinfo("finished","import done")

def video_stream():
    if cap != None:
        _, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(int(1000//fps), video_stream) 


window = Tk()

window.title("Karaoke")
window.geometry('800x800')
window.configure(background="grey")

start = Button(window, text="START", command=startAction)
start.grid(column=0,row=4)

stop = Button(window, text="STOP", command=stopAction)
stop.grid(column=1,row=4)

imp = Button(window, text="IMPORT", command=importAction)
imp.grid(column=2,row=4)

sngs = os.listdir("./songs")
sn = tk.StringVar()
sn.set([s for s in sngs])
songs = Listbox(window,listvariable=sn)
songs.grid(row=1,columnspan=3,  sticky = tk.W+tk.E)


video = Frame(window, bg='#000000')
video.grid(column=0,row=0,columnspan=3,sticky = tk.W+tk.E)
lmain = Label(video)
lmain.grid()

acc = Scale(window,from_=0,to=300,orient=HORIZONTAL)
acc.set(100)
acc.grid(columnspan=3,row=2,sticky = tk.W+tk.E)


voc = Scale(window,from_=0,to=100,orient=HORIZONTAL)
voc.set(0)
voc.grid(columnspan=3,row=3,sticky = tk.W+tk.E)

window.mainloop()