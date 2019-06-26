import os
import tkinter as tk
from tkinter import simpledialog, filedialog

# window = tk.Tk()
# window.geometry("300x300")

dir_path_source = filedialog.askdirectory(title="Please select a folder")
dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
show_name =  input("What is the TV Show name?")
season_number = input("What is the Season number?")
# dirs = os.listdir(dir_path) # Get contents of the selected directory, not currently being used
currentEpisodeList = []
currentSubList = []
newEpisodeList = []
newSubList = []
start = 1

if int(season_number) < 10:
    season_number = "0" + season_number

# window = tkinter.Tk()  # Not needed with the initial window setup

# Filter anything but file types from the creation of the original lists, and sort between subs and video files

for file in os.listdir(dir_path):
    if os.path.isfile(dir_path + file):
        file_orig, extension = os.path.splitext(file)
        print(extension)
        if extension == ".srt":
            currentSubList.append(file)
        elif extension == ".sub":
            currentSubList.append(file)
        else:
            currentEpisodeList.append(file)

# Check of initial lists
print(currentEpisodeList)
print(currentSubList)

# Sort lists
currentEpisodeList.sort(key=str.lower)
currentSubList.sort(key=str.lower)

# General lists check, post sort
print (currentEpisodeList)
print (currentSubList)

x = 0
for name in currentEpisodeList:
    print (type(currentEpisodeList[x]))
    x += 1

# Create new lists with new file names
a = start
b = start
for item in currentEpisodeList:
    if a < 10:
        episode_number = "0" + str(a)
    else: 
        episode_number = a
    # Need to make sure the extension is carried over
    file_orig, extension = os.path.splitext(item)
    newEpisodeList.append(show_name + " S" + season_number + "E" + str(episode_number) + extension)
    a += 1

for item in currentSubList:
    if b < 10:
        episode_number = "0" + str(b)
    else: 
        episode_number = b
    # Need to make sure the extension is carried over
    file_orig, extension = os.path.splitext(item)
    newSubList.append(show_name + " S" + season_number + "E" + str(episode_number) + extension)
    b += 1

# Comparison of the two lists to make sure order is correct
print (currentEpisodeList)
print (newEpisodeList) 
print (currentSubList)
print (newSubList)

# Manual stop point to allow for comparison of the two lists
ok_to_proceed = input("Ok to proceed? Yes/No ")

# Rename
if ok_to_proceed == "Yes":
    i = start
    j = start
    x = 0
    y = 0
    for oldEpisodeName in currentEpisodeList:
        dst = str("".join(newEpisodeList[x]))
        src = str(dir_path) + oldEpisodeName
        dst = str(dir_path) + dst
        os.rename(src, dst)
        i += 1
        x += 1
    for oldSubName in currentSubList:
        dst = str("".join(newSubList[y]))
        src = str(dir_path) + oldSubName
        dst = str(dir_path) + dst
        os.rename(src, dst)
        j += 1
        y += 1