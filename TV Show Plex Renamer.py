import os
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, ttk

# Function to test button
def buttonTest():
    print("Button Works!")
    
def sourceCheck():    
    print(source_path)
    print(type(source_path))

# Get source directory through filedialog
def getSourceDir():
    dir_path_source = filedialog.askdirectory(title="Please select a folder")
    dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
    file_path.insert(0, dir_path)
    print(dir_path)
    return dir_path
    # print(type(source_path))

def assignSourceDir():
    global source_path
    source_path = getSourceDir()

def renameFiles():

    # Pulling global values from entry boxes
    global source_path
    global source_var
    global showname_var
    global season_var

    # Get source directory, replaced by getSourceDir function
    # dir_path_source = filedialog.askdirectory(title="Please select a folder")
    # dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash

    # Check for source directory either manually entered or through filedialog
    orig_path = source_path
    if orig_path:
        print("All Good")
    if not orig_path:
        print("Not Good. Needs Change")
        orig_path = source_var.get()
    print(orig_path)

    # Show details
    # OLD    
    # show_name =  simpledialog.askstring("Name", "What is the TV Show name?")
    # season_number = simpledialog.askstring("Season", "What is the Season number?")
    # dirs = os.listdir(dir_path) # Get contents of the selected directory, not currently being used
    
    # NEW
    # Also checks if entries are blank
    show_name = showname_var.get()
    if not show_name:
        show_name = simpledialog.askstring("Name", "What is the TV Show name?")
    season_number = season_var.get()
    if not season_number:
        season_number = simpledialog.askstring("Season", "What is the Season number?") 

    if int(season_number) < 10:
        season_number = "0" + season_number

    # Filter anything but file types from the creation of the original lists, and sort between subs and video files
    for file in os.listdir(orig_path):
        if os.path.isfile(orig_path + file):
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
    ok_to_sort = messagebox.askyesno("Sort Needed?", "Does this need to be sorted?")
    if ok_to_sort:
        currentEpisodeList.sort(key=str.lower)
        currentSubList.sort(key=str.lower)
        # General lists check, post sort
        print (currentEpisodeList)
        print (currentSubList)

    # Type Check, not really needed except for testing
    # x = 0
    # for name in currentEpisodeList:
    #     print (type(currentEpisodeList[x]))
    #     x += 1

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
    ok_to_proceed = messagebox.askyesno("Proceed?", "Ok to proceed?")

    # Rename
    if ok_to_proceed:
        i = start
        j = start
        x = 0
        y = 0
        for oldEpisodeName in currentEpisodeList:
            dst = str("".join(newEpisodeList[x]))
            src = str(orig_path) + oldEpisodeName
            dst = str(orig_path) + dst
            os.rename(src, dst)
            i += 1
            x += 1
        for oldSubName in currentSubList:
            dst = str("".join(newSubList[y]))
            src = str(orig_path) + oldSubName
            dst = str(orig_path) + dst
            os.rename(src, dst)
            j += 1
            y += 1
    else:
        quit()


window = tk.Tk()
# window.title("TV Show Plex Renamer")
window.geometry("800x200")

currentEpisodeList = []
currentSubList = []
newEpisodeList = []
newSubList = []
start = 1
source_path = ""
source_var = tk.StringVar()
season_var = tk.StringVar()
showname_var = tk.StringVar()

my_label = tk.Label(window, text="Season File Path")
my_label.grid(row=1, column=1)

file_path = tk.Entry(window, width=100, textvariable=source_var)
file_path.grid(row=2, column=1, columnspan=2)

show_name_label = tk.Label(window, text="Show Name")
show_name_label.grid(row=3, column=1)
show_name_entry = tk.Entry(window, width=50, textvariable=showname_var)
show_name_entry.grid(row=4, column=1)

season_number_label = tk.Label(window, text="Season Number")
season_number_label.grid(row=3, column=2)
season_number_entry = tk.Entry(window, width=10, textvariable=season_var)
season_number_entry.grid(row=4, column=2)

test_source_button = tk.Button(window, text="Browse")
test_source_button.grid(row=2, column=3)
test_source_button['command'] = assignSourceDir

start_button = tk.Button(window, text="Start")
start_button.grid(row=5, column=1)
start_button['command'] = renameFiles

quit_button = tk.Button(window, text="Quit")
quit_button.grid(row=5, column=2)
quit_button['command'] = window.destroy

test_source_button = tk.Button(window, text="Test")
test_source_button.grid(row=5, column=3)
test_source_button['command'] = sourceCheck

window.mainloop()