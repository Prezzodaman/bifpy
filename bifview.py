import argparse
import os
import time
import bif
from PIL import Image
from PIL import ImageTk
import tkinter
from tkinter import filedialog

def save_image():
    global image
    filename=filedialog.asksaveasfile(title="Save the converted file...",filetypes=[("PNG files","*.png")],defaultextension=".png")
    if filename!=None:
        image["image"].save(filename.name)

parser = argparse.ArgumentParser(description="Views a BIF image.")
parser.add_argument("input_file", type=argparse.FileType("r"), help="The name of the file to be converted.")

args=parser.parse_args()

input_extension=".".join(args.input_file.name.split(".")[-1:]).lower()
if input_extension=="bif":
    start_time=time.time()
    print("Opening...")
    with open(args.input_file.name) as file:
        image=bif.decompress_bif(file.readline(),False)
    end_time=time.time()
    window=tkinter.Tk(className="\BIF Viewer")
    image_tk=ImageTk.PhotoImage(image["image"])
    image_label=tkinter.Label(image=image_tk).place(x=-2,y=-2)
    tkinter.Button(text="Save as PNG",command=save_image).pack(side="right",anchor="s",padx=8,pady=8)
    tkinter.Label(anchor="w",text="Displayed in " + str(round(end_time-start_time,2)) + " seconds!").pack(side=tkinter.BOTTOM,fill="x")
    if image["compressed"]:
        tkinter.Label(anchor="w",text="Compression ratio: " + str(image["ratio"]) + "%").pack(side=tkinter.BOTTOM,fill="x")
    else:
        tkinter.Label(anchor="w",text="Uncompressed").pack(side=tkinter.BOTTOM,fill="x")

    tkinter.Label(anchor="w",text=bif.get_mode_description(image["mode"])).pack(side=tkinter.BOTTOM,fill="x")
    window.geometry(str(image["image"].size[0]) + "x" + str(image["image"].size[1]+65))
    window.resizable(width=False,height=False)
    window.mainloop()
else:
    raise argparse.ArgumentTypeError("Input file not a BIF!")
