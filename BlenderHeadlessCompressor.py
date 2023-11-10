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
JpgCompression = dirs["jpg"]


def convert_packed_images_to_jpg():
    # loop through all images in the blend file
    for img in bpy.data.images:
        
        try:
            # check if the image is packed and not already jpg
            if img.packed_file:
                # save the image as jpg with the given quality
                img.unpack(method='USE_LOCAL')
                img.file_format = 'JPEG'
                img.save()
                # unpack the image
             
                # reload the image from the temporary file
 
                img.reload()
                # pack the image again
                img.pack()
        except:
            print(f"{img.name} image does not exist")



def pack_all_files():
    try:
        bpy.ops.file.pack_all()
    except:
        print("no external files!!")


def HasBlend(folder):
    # Loop through the folder and its subfolders
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".blend"):
                print(folder)
                print(file)
                return True
    return False
    
def BlendFileCount(folder):
    count = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".blend"):
                count += 1
    return count

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
            PreJpgCompression = True
            try:
                bpy.ops.wm.open_mainfile(filepath=os.path.join(SourcePath))
                pack_all_files()
                if JpgCompression:
                    convert_packed_images_to_jpg()
                
                LoadedFiles += 1
                LoadedBytes += os.path.getsize(SourcePath)
            except RuntimeError as error:
                print(error)
                FailedSaves.append(SourcePath)
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
                    FailedSaves.append(SourcePath)

CopyFolderStructure(SourceDir,DestDir)



print("\n\n\n\n\n\n")
print("-------------------------")

if len(FailedSaves) != 0:
    print("Below Mentioned files failed to compress/load")
    for fail in FailedSaves:
        print(fail)
    print("Above mentioned files failed to compress/load")
    print("-------------------------")

SaveMB = round(SavedBytes/(1000*1000),1)
LoadMB = round(LoadedBytes/(1000*1000),1)

print(f'{LoadMB} MB -> {SaveMB} MB')
print(f'Source Files : {BlendFileCount(SourceDir)}')
print(f'Loaded Source files : {LoadedFiles}')
print(f'Compressed files : {SavedFiles}')
print("-------------------------")
os._exit(1)