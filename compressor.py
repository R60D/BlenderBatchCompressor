import os
import tkinter as tk
from tkinter import filedialog as fd
import tkinter.messagebox as mb
import pickle
import subprocess

file_name = "dirs.pkl"

def save(a,b):
    dirs = {"source": a, "dest": b}
    with open(file_name, "wb") as f:
        pickle.dump(dirs, f)
    print(f"saved {a},{b}")

def compress():
    source_dir = source_entry.get()
    dest_dir = dest_entry.get()
    if not os.path.isdir(source_dir):
        mb.showerror("Error", "Invalid source directory")
        return
    if not os.path.isdir(dest_dir):
        mb.showerror("Error", "Invalid destination directory")
        return
    save(source_entry.get(),dest_entry.get())
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "BlenderHeadlessCompressor.py")
    try:
        process = subprocess.Popen(["blender", "--background", "--python", script_path])
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
browse_source_button = tk.Button(root, text="Browse", command=lambda: [source_entry.delete(0, tk.END), source_entry.insert(0, fd.askdirectory()),save(source_entry.get(),dest_entry.get())]) 
browse_source_button.grid(row=0, column=2, padx=5, pady=5)
browse_dest_button = tk.Button(root, text="Browse", command=lambda: [dest_entry.delete(0, tk.END), dest_entry.insert(0, fd.askdirectory()),save(source_entry.get(),dest_entry.get())]) 
browse_dest_button.grid(row=1, column=2, padx=5, pady=5)
compress_button = tk.Button(root, text="Compress", command=compress) 
compress_button.grid(row=2, column=1, padx=5, pady=5)
try:
    with open(file_name, "rb") as f:
        dirs = pickle.load(f)
    source_dir = dirs["source"]
    dest_dir = dirs["dest"]
    source_entry.insert(0, source_dir)
    dest_entry.insert(0, dest_dir)
except Exception as e:
    print(e)
root.mainloop()
