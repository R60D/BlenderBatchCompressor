import os
import sys
import bpy
import pickle

file_name = "dirs.pkl"
current_dir = os.path.dirname(os.path.abspath(__file__))
pickle_path = os.path.join(current_dir, file_name)

def check_and_remove(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"{file_name} removed")



with open(pickle_path, "rb") as f:
    dirs = pickle.load(f)

source_dir = dirs["source"]
dest_dir = dirs["dest"]

print("--------------------")
print(source_dir)
print(dest_dir)
print("--------------------")
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

for file in os.listdir(source_dir):
    if file.endswith(".blend"):
        compressed_file = file
        bpy.ops.wm.open_mainfile(filepath=os.path.join(source_dir, file))
        newfilepath = os.path.join(dest_dir, compressed_file)
        check_and_remove(newfilepath)
        try:
            bpy.ops.wm.save_as_mainfile(filepath=newfilepath, compress=True)
        except RuntimeError as error:
            print(error)
        print(f"Compressed {file} to {compressed_file}")
os._exit(1)
