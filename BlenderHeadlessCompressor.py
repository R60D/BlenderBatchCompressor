import os
import sys
import bpy
import pickle

def check_and_remove(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"{file_name} removed")

file_name = "dirs.pkl"

with open(file_name, "rb") as f:
    dirs = pickle.load(f)

source_dir = dirs["source"]
dest_dir = dirs["dest"]

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

for file in os.listdir(source_dir):
    if file.endswith(".blend"):
        compressed_file = file
        bpy.ops.wm.open_mainfile(filepath=os.path.join(source_dir, file))
        newfilepath = os.path.join(dest_dir, compressed_file)
        check_and_remove(newfilepath)
        bpy.ops.wm.save_as_mainfile(filepath=newfilepath, compress=True)
        print(f"Compressed {file} to {compressed_file}")
os._exit(1)
