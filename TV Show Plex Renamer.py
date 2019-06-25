import os
import tkinter as tk
from tkinter import simpledialog, filedialog

# window = tk.Tk()
# window.geometry("300x300")

dir_path_source = filedialog.askdirectory(title="Please select a folder")
dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
show_name =  input("What is the TV Show name?")
season_number = input("What is the Season number?")
dirs = os.listdir(dir_path) # Get contents of the selected directory
fileList = []
newList = []
start = 1

if int(season_number) < 10:
    season_number = "0" + season_number

# window = tkinter.Tk()  # Not needed with the initial window setup

# Filter anything but file types from the dirs list, creating working list

for file in os.listdir(dir_path):
    if os.path.isfile(dir_path + file):
        fileList.append(file)

# Check of initial list
print(fileList)

# Sort list
fileList.sort(key=str.lower)

# General list check, including to see if there were any changes to the order
print (fileList)
print (len(fileList))

x = 0
for name in fileList:
    print (type(fileList[x]))
    x += 1

# Create new list with new file names
z = start
for item in fileList:
    if z < 10:
        episode_number = "0" + str(z)
    else: 
        episode_number = z
    # Need to make sure the extension is carried over
    file_orig, extension = os.path.splitext(item)
    newList.append(show_name + " S" + season_number + "E" + str(episode_number) + extension)
    z += 1

# Comparison of the two lists to make sure order is correct
print (fileList)
print (newList) 

# Manual stop point to allow for comparison of the two lists
ok_to_proceed = input("Ok to proceed? Yes/No ")

# Rename
if ok_to_proceed == "Yes":
    i = start
    y = 0
    for oldName in fileList:
        dst = str("".join(newList[y]))
        src = str(dir_path) + oldName
        dst = str(dir_path) + dst
        os.rename(src, dst)
        i += 1
        y += 1