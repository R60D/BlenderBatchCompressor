import os
import tkinter as tk
from tkinter import filedialog as fd
import tkinter.messagebox as mb
import pickle
import subprocess

file_name = "dirs.pkl"

def save(a,b,c):
    dirs = {"source": a, "dest": b,"blend": c}
    with open(file_name, "wb") as f:
        pickle.dump(dirs, f)
    print(f"saved {a},{b},{c}")

def compress():
    source_dir = source_entry.get()
    dest_dir = dest_entry.get()
    blender_path = blender_entry.get() # get the blender path from the entry
    if not os.path.isdir(source_dir):
        mb.showerror("Error", "Invalid source directory")
        return
    if not os.path.isdir(dest_dir):
        mb.showerror("Error", "Invalid destination directory")
        return
    if not os.path.isfile(blender_path): # check if the blender path is valid
        mb.showerror("Error", "Invalid blender path")
        return
    save(source_entry.get(),dest_entry.get(),blender_entry.get())
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "BlenderHeadlessCompressor.py")
    try:
        process = subprocess.Popen([blender_path, "--background", "--python", script_path]) # use the blender path instead of "blender"
        process.wait () 
        return_code = process.returncode 
        print (return_code) 
    except Exception as e:
        mb.showerror("Error", str(e))
        return
    source_size = round(sum(os.path.getsize(os.path.join(source_dir, f)) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)))/(1000*1000),1)
    dest_size = round(sum(os.path.getsize(os.path.join(dest_dir, f)) for f in os.listdir(dest_dir) if os.path.isfile(os.path.join(dest_dir, f)))/(1000*1000),1)
    mb.showinfo("Compression complete", f"{source_size} -> {dest_size} MB")

root = tk.Tk()
root.title("Batch blend file compressor") 
source_label = tk.Label(root, text="Source directory:")
source_label.grid(row=0, column=0, padx=5, pady=5)
source_entry = tk.Entry(root, width=40)
source_entry.grid(row=0, column=1, padx=5, pady=5)
dest_label = tk.Label(root, text="Destination directory:")
dest_label.grid(row=1, column=0, padx=5, pady=5)
dest_entry = tk.Entry(root, width=40)
dest_entry.grid(row=1, column=1, padx=5, pady=5)
blender_label = tk.Label(root, text="Blender.exe path:") # add a label for the blender path
blender_label.grid(row=2, column=0, padx=5, pady=5)
blender_entry = tk.Entry(root, width=40) # add an entry for the blender path
blender_entry.grid(row=2, column=1, padx=5, pady=5)
browse_source_button = tk.Button(root, text="Browse", command=lambda: [source_entry.delete(0, tk.END), source_entry.insert(0, fd.askdirectory()),save(source_entry.get(),dest_entry.get(),blender_entry.get())]) 
browse_source_button.grid(row=0, column=2, padx=5, pady=5)
browse_dest_button = tk.Button(root, text="Browse", command=lambda: [dest_entry.delete(0, tk.END), dest_entry.insert(0, fd.askdirectory()),save(source_entry.get(),dest_entry.get(),blender_entry.get())]) 
browse_dest_button.grid(row=1, column=2, padx=5, pady=5)
browse_blender_button = tk.Button(root, text="Browse", command=lambda: [blender_entry.delete(0, tk.END), blender_entry.insert(0, fd.askopenfilename()),save(source_entry.get(),dest_entry.get(),blender_entry.get())]) # add a button to browse for the blender file
browse_blender_button.grid(row=2, column=2, padx=5, pady=5)
compress_button = tk.Button(root, text="Compress", command=compress) 
compress_button.grid(row=3, column=1, padx=5, pady=5)
try:
    with open(file_name, "rb") as f:
        dirs = pickle.load(f)
    source_dir = dirs["source"]
    dest_dir = dirs["dest"]
    blend_dir = dirs["blend"]
    source_entry.insert(0, source_dir)
    dest_entry.insert(0, dest_dir)
    blender_entry.insert(0, blend_dir)
except Exception as e:
    print(e)
root.mainloop()
