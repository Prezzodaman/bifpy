import tkinter
from tkinter import filedialog
from tkinter import messagebox
import bif
import time
from PIL import Image
from PIL import ImageTk

def original_algorithm_check():
    if mode.get()==4 or mode.get()==5:
        original_algorithm.set(0)
    if original_algorithm.get()==0:
        threshold_slider_label.set("Prebright:")
    else:
        threshold_slider_label.set("Threshold:")

def mode_button_check():
    if mode.get()==4 or mode.get()==5:
        original_algorithm.set(0)
        threshold_slider_label.set("Prebright:")
    else:
        if original_algorithm.get()==0:
            threshold_slider_label.set("Prebright:")
        else:
            threshold_slider_label.set("Threshold:")

def open_file():
    global image
    filename=filedialog.askopenfilename(title="Select a file for conversion...",filetypes=[("Image files","*.jpg *.jpeg *.png *.webp"),("BIF files","*.bif")])
    if filename!=None:
        filename_string.set(filename)
        filename_label_text.set(filename)
        filename_extension=".".join(filename_string.get().split(".")[-1:]).lower()
        if filename_extension=="bif":
            with open(filename_string.get()) as file:
                image=bif.decompress_bif(file.readline(),False)
            image_tk=ImageTk.PhotoImage(image["image"])
            image_label.configure(image=image_tk)
            image_label.image=image_tk
            preview_window.geometry(str(image["image"].size[0]) + "x" + str(image["image"].size[1]))
            converted.set(0)
            
            mode_string=""
            mode_string=bif.get_mode_description(image["mode"])
            compressed_string=""
            if image["compressed"]:
                compressed_string="Compression ratio: " + str(image["ratio"]) + "%"
            else:
                compressed_string="Uncompressed"
            
            status_label_text.set("BIF opened successfully! "+mode_string+", "+compressed_string)
            bif_opened.set(1)

def save_file():
    global image
    if bif_opened.get()==0:
        if converted.get()==1:
            if preview_compressed.get()!=compressed.get():
                image=bif.convert_to_bif(filename_string.get(),mode.get(),bool(original_algorithm.get()),threshold_actual.get(),bool(compressed.get()),prebright_actual.get(),float(scale.get()),False)
            filename=filedialog.asksaveasfile(title="Save the converted file...",filetypes=[("BIF files","*.bif")],defaultextension=".bif")
            if filename!=None:
                filename_actual=filename.name
                with open(filename_actual, "w") as file:
                    file.write(image["file"])
        else:
            messagebox.showerror("Error","Image not converted yet!")
    else:
        filename=filedialog.asksaveasfile(title="Save the converted file...",filetypes=[("PNG files","*.png")],defaultextension=".png")
        if filename!=None:
            image["image"].save(filename.name)

def preview():
    global image
    if filename_string.get()=="":
        messagebox.showerror("Error","File not specified!")
    else:
        filename_extension=".".join(filename_string.get().split(".")[-1:]).lower()
        if filename_extension!="bif":
            start_time=time.time()
            bif_opened.set(0)
            threshold_actual.set(0)
            prebright_actual.set(0)
            if original_algorithm.get()==0:
                prebright_actual.set(threshold.get())
            else:
                threshold_actual.set(threshold.get())
            image=bif.convert_to_bif(filename_string.get(),mode.get(),bool(original_algorithm.get()),threshold_actual.get(),bool(compressed.get()),prebright_actual.get(),float(scale.get()),False)
            image_tk=ImageTk.PhotoImage(image["image"])
            image_label.configure(image=image_tk)
            image_label.image=image_tk

            end_time=time.time()
            preview_window.geometry(str(image["image"].size[0]) + "x" + str(image["image"].size[1]))
            if image["file"].endswith("D:"):
                status_label_text.set("Conversion error!")
                messagebox.showerror("Error","For whatever reason, BIF was unable to convert this image. It likely has the incorrect file extension, or is in a format that isn't supported by the converter.")
                converted.set(0)
            else:
                status_label_text.set("Conversion completed in " + str(round(end_time-start_time,2)) + " seconds!")
                converted.set(1)
            preview_compressed.set(int(compressed.get()))
            preview_window.lift()

def about_show():
    def destroy():
        about.grab_release()
        about.destroy()
    about=tkinter.Toplevel(window)
    about.title("About!")
    about.geometry("360x560")
    about.configure(bg="black")
    about.resizable(width=False,height=False)

    logo2_image=tkinter.PhotoImage(file="gui/bifpy_small.gif")
    logo2_label=tkinter.Label(about,image=logo2_image,border=0)
    logo2_label.pack()
    
    tkinter.Label(about,text="BIF.py",fg="white",bg="black",font="Courier 20 bold").pack()
    tkinter.Label(about,text="A complete Python rewrite of the Best Image Format, complete with the BCA and original colour reduction algorithm, alongside some bonus new features!\n\nBest Image Format is an attempt at creating an image format, complete with lossless compression (via the Bloated Compression Algorithm) and various colour modes for extremely vibrant results! It's objectively better than PNG and JPG.\n\nBy Presley Peters, 2021-2022.",fg="white",bg="black",wraplength=360).pack(pady=10)
    tkinter.Button(about,text="okay cool thx",command=destroy).pack()
    about.wait_visibility()
    about.grab_set()
    about.mainloop()

image=None

window=tkinter.Tk(className="\Best Image Format")
window.resizable(width=False,height=False)
window.geometry("600x420")

tkinter.Button(text="?",command=about_show).pack(side="right",anchor="n",padx=(0,10),pady=10)
        
preview_window=tkinter.Toplevel(window)
preview_window.resizable(width=False,height=False)
preview_window.geometry("400x400+" + str(window.winfo_rootx()+600) + "+" + str(window.winfo_rooty()-20))
preview_window.title("Preview")
image_label=tkinter.Label(preview_window)
image_label.place(x=-2,y=-2)

logo_image=tkinter.PhotoImage(file="gui/logo.gif")
logo_label=tkinter.Label(window,image=logo_image)
logo_label.pack(pady=10)

mode_frame=tkinter.LabelFrame(text="Conversion properties")
mode_frame.pack(fill="x",expand=True,padx=20)

mode=tkinter.IntVar(value=1)
mode_buttons=[]
mode_buttons.append(tkinter.Radiobutton(mode_frame,text=bif.get_mode_description(1),variable=mode,value=1,command=mode_button_check))
mode_buttons.append(tkinter.Radiobutton(mode_frame,text=bif.get_mode_description(2),variable=mode,value=2,command=mode_button_check))
mode_buttons.append(tkinter.Radiobutton(mode_frame,text=bif.get_mode_description(3),variable=mode,value=3,command=mode_button_check))
mode_buttons.append(tkinter.Radiobutton(mode_frame,text=bif.get_mode_description(4),variable=mode,value=4,command=mode_button_check))
mode_buttons.append(tkinter.Radiobutton(mode_frame,text=bif.get_mode_description(5),variable=mode,value=5,command=mode_button_check))
for button in mode_buttons:
    button.pack(anchor="w")

original_algorithm=tkinter.IntVar(value=0)
original_algorithm_box=tkinter.Checkbutton(mode_frame,text="Original algorithm",variable=original_algorithm,command=original_algorithm_check)
original_algorithm_box.pack(side="right",anchor="e")

tkinter.Label(mode_frame,text="Scale:").pack(side="left",anchor="e",expand=True)
scale=tkinter.StringVar(value="1.00")
scale_slider_value=tkinter.Label(mode_frame,width=3,textvariable=scale).pack(side="left",anchor="w",expand=True)
scale_slider=tkinter.Scale(mode_frame,resolution=0.01,from_=0.25,to=1,variable=scale,orient="horizontal",showvalue=0)
scale_slider.pack(side="left")

threshold_slider_label=tkinter.StringVar(value="Prebright:")
tkinter.Label(mode_frame,textvariable=threshold_slider_label,width=8).pack(side="left",anchor="e",expand=True)
threshold=tkinter.IntVar(value=0)
threshold_slider_value=tkinter.Label(mode_frame,width=2,textvariable=threshold).pack(side="right",anchor="w",expand=True)
threshold_slider=tkinter.Scale(mode_frame,from_=-100,to=100,variable=threshold,orient="horizontal",showvalue=0)
threshold_slider.pack(side="right",anchor="w",expand=True)

compressed=tkinter.IntVar(value=0)
compressed_box=tkinter.Checkbutton(text="Enable BCA",variable=compressed)
compressed_box.pack()

status_label_text=tkinter.StringVar(value="Idle!")
status_label=tkinter.Label(textvariable=status_label_text).pack()
filename_string=tkinter.StringVar(value="")
filename_label_text=tkinter.StringVar(value="File not selected yet...")
filename_label=tkinter.Label(textvariable=filename_label_text).pack()
open_file_button=tkinter.Button(text="Open file",command=open_file)
open_file_button.pack(side="left",anchor="e",expand=True,padx=4,pady=(0,10))
save_file_button=tkinter.Button(text="Save file",command=save_file)
save_file_button.pack(side="right",anchor="w",expand=True,padx=4,pady=(0,10))
preview_button=tkinter.Button(text="Preview",command=preview)
preview_button.pack(pady=(0,10))

converted=tkinter.IntVar(value=0)
preview_compressed=tkinter.IntVar(value=0)
prebright_actual=tkinter.IntVar(value=0)
threshold_actual=tkinter.IntVar(value=0)
bif_opened=tkinter.IntVar(value=0)
    
window.focus_set()
window.mainloop()
