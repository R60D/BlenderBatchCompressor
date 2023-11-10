import os
import tkinter as tk
from tkinter import filedialog as fd
import tkinter.messagebox as mb
import pickle
import subprocess

FileName = "dirs.pkl"
CurrentDir = os.path.dirname(os.path.abspath(__file__))
PicklePath = os.path.join(CurrentDir, FileName)
def Save(a,b,c,d):
    dirs = {"source": a, "dest": b,"blend": c, "jpg": d} # add a key for jpg compression
    with open(PicklePath, "wb") as f:
        pickle.dump(dirs, f)
    print(f"saved {a},{b},{c},{d}") # print the jpg value as well

def Compress():
    SourceDir = SourceEntry.get()
    DestDir = DestEntry.get()
    BlenderPath = BlenderEntry.get() # get the blender path from the entry
    JpgValue = JpgVar.get() # get the jpg value from the variable
    if not os.path.isdir(SourceDir):
        mb.showerror("Error", "Invalid source directory")
        return
    if not os.path.isdir(DestDir):
        mb.showerror("Error", "Invalid destination directory")
        return
    if not os.path.isfile(BlenderPath): # check if the blender path is valid
        mb.showerror("Error", "Invalid blender path")
        return
    ScriptPath = os.path.join(CurrentDir, "BlenderHeadlessCompressor.py")
    try:
        process = subprocess.Popen([BlenderPath, "--background", "--python", ScriptPath, str(JpgValue)]) # pass the jpg value as an argument to the script
        process.wait () 
        ReturnCode = process.returncode 
        print (ReturnCode) 
    except Exception as e:
        mb.showerror("Error", str(e))
        return
    mb.showinfo("Compression complete", f"Check the console for data")

root = tk.Tk()
root.title("Batch blend file compressor") 
SourceLabel = tk.Label(root, text="Source directory:")
SourceLabel.grid(row=0, column=0, padx=5, pady=5)
SourceEntry = tk.Entry(root, width=40)
SourceEntry.grid(row=0, column=1, padx=5, pady=5)
DestLabel = tk.Label(root, text="Destination directory:")
DestLabel.grid(row=1, column=0, padx=5, pady=5)
DestEntry = tk.Entry(root, width=40)
DestEntry.grid(row=1, column=1, padx=5, pady=5)
BlenderLabel = tk.Label(root, text="Blender.exe path:") # add a label for the blender path
BlenderLabel.grid(row=2, column=0, padx=5, pady=5)
BlenderEntry = tk.Entry(root, width=40) # add an entry for the blender path
BlenderEntry.grid(row=2, column=1, padx=5, pady=5)
JpgLabel = tk.Label(root, text="Convert Packed Images to jpg compression:") # add a label for the jpg compression
JpgLabel.grid(row=3, column=0, padx=5, pady=5)
JpgVar = tk.BooleanVar() # create a boolean variable for the jpg compression
JpgCheck = tk.Checkbutton(root, text="Enable", variable=JpgVar) # create a checkbutton for the jpg compression
JpgCheck.grid(row=3, column=1, padx=5, pady=5)
BrowseSourceButton = tk.Button(root, text="Browse", command=lambda: [SourceEntry.delete(0, tk.END), SourceEntry.insert(0, fd.askdirectory()),Save(SourceEntry.get(),DestEntry.get(),BlenderEntry.get(),JpgVar.get())]) # save the jpg value as well
BrowseSourceButton.grid(row=0, column=2, padx=5, pady=5)
BrowseDestButton = tk.Button(root, text="Browse", command=lambda: [DestEntry.delete(0, tk.END), DestEntry.insert(0, fd.askdirectory()),Save(SourceEntry.get(),DestEntry.get(),BlenderEntry.get(),JpgVar.get())]) # save the jpg value as well
BrowseDestButton.grid(row=1, column=2, padx=5, pady=5)
BrowseBlenderButton = tk.Button(root, text="Browse", command=lambda: [BlenderEntry.delete(0, tk.END), BlenderEntry.insert(0, fd.askopenfilename()),Save(SourceEntry.get(),DestEntry.get(),BlenderEntry.get(),JpgVar.get())]) # save the jpg value as well
BrowseBlenderButton.grid(row=2, column=2, padx=5, pady=5)
CompressButton = tk.Button(root, text="Compress", command=Compress) 
CompressButton.grid(row=4, column=1, padx=5, pady=5) # change the row to 4
try:
    with open(PicklePath, "rb") as f:
        dirs = pickle.load(f)
    SourceDir = dirs["source"]
    DestDir = dirs["dest"]
    BlendDir = dirs["blend"]
    JpgDir = dirs["jpg"] # load the jpg value from the pickle file
    SourceEntry.insert(0, SourceDir)
    DestEntry.insert(0, DestDir)
    BlenderEntry.insert(0, BlendDir)
    JpgVar.set(JpgDir) # set the checkbutton according to the jpg value
except Exception as e:
    print(e)
root.mainloop()
