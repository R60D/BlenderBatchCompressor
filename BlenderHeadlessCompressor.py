import os
import sys
import bpy
import pickle

FileName = "dirs.pkl"
CurrentDir = os.path.dirname(os.path.abspath(__file__))
PicklePath = os.path.join(CurrentDir, FileName)

LoadedBytes = 0
LoadedFiles = 0
SavedBytes = 0
SavedFiles = 0
FailedSaves = []

def CheckAndRemove(FileName):
    if os.path.exists(FileName):
        os.remove(FileName)
        print(f"{FileName} removed")

with open(PicklePath, "rb") as f:
    dirs = pickle.load(f)

SourceDir = dirs["source"]
DestDir = dirs["dest"]

def HasBlend(folder):
    # Loop through the folder and its subfolders
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".blend"):
                print(folder)
                print(file)
                return True
    return False

def CopyFolderStructure(source, target):
    global LoadedFiles
    global SavedFiles
    global SavedBytes
    global LoadedBytes
    global FailedSaves
    # Create the target folder if it does not exist
    # Check if the source folder has a file ending in ".blend"
    HasBlendFile = HasBlend(source)
    # If the source folder has a blend file, create the target folder if it does not exist
    if HasBlendFile:
        if not os.path.exists(target):
            os.mkdir(target)
    # Loop through the files and subfolders in the source folder
    for file in os.listdir(source):
        # Get the full path of the file or subfolder
        SourcePath = os.path.join(source, file)
        TargetPath = os.path.join(target, file)
        # If the source path is a folder, call the function recursively
        print(HasBlendFile)
        print(SourcePath)
        if os.path.isdir(SourcePath) and HasBlendFile:
            CopyFolderStructure(SourcePath,TargetPath)
        # If the source path is a file, copy it to the target path
        elif file.lower().endswith(".blend"):
            
            try:
                bpy.ops.wm.open_mainfile(filepath=os.path.join(SourcePath))
                LoadedFiles += 1
                LoadedBytes += os.path.getsize(SourcePath)
            except RuntimeError as error:
                print(error)
                FailedSaves.append(TargetPath)
                continue
            try:
                
                # Save the destination file with compression
                CheckAndRemove(TargetPath)
                bpy.ops.wm.save_as_mainfile(filepath=TargetPath, compress=True)
                SavedBytes += os.path.getsize(TargetPath)
                SavedFiles += 1            
            except RuntimeError as error:
                print(error)
                try:
                    SavedBytes += os.path.getsize(TargetPath)
                    SavedFiles += 1            
                except:
                    FailedSaves.append(TargetPath)

CopyFolderStructure(SourceDir,DestDir)



print("\n\n\n\n\n\n")
print("-------------------------")

if len(FailedSaves) != 0:
    print("Below Mentioned files failed to compress/load")
    for fail in FailedSaves:
        print(fail)
    print("Above mentioned files failed to compress/load")

SaveMB = round(SavedBytes/(1000*1000),1)
LoadMB = round(LoadedBytes/(1000*1000),1)

print(f'Source folder {LoadMB} MB -> Destination folder {SaveMB} MB')
print(f'Loaded Source files : {LoadedFiles} Compressed files : {SavedFiles}')
print("-------------------------")
os._exit(1)