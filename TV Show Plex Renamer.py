import os
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, ttk

# Function to test button
def buttonTest():
    print("Button Works!")
    
# Button to quickly check source paths and episode lists
def sourceCheck():    
    print("Source Path = " + source_path)
    print("Source Var = " + source_var.get())
    print(currentEpisodeList)
    print(newEpisodeList)

# Clear contents of the comparison panel
def clearText():
    text_box_left.delete(1.0, 'end')
    currentEpisodeList.clear()
    currentSubList.clear()
    newEpisodeList.clear()
    newSubList.clear()

# Get source directory through filedialog
def getSourceDir():
    # Get source directory, replaced by getSourceDir function
    # dir_path_source = filedialog.askdirectory(title="Please select a folder")
    # dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash

    dir_path_source = filedialog.askdirectory(title="Please select a folder")
    dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
    file_path.delete(0, 'end')
    file_path.insert(0, dir_path)
    print(dir_path)
    return dir_path
    # print(type(source_path))

# Yes, it modifies the global source_path...
def assignSourceDir():
    global source_path
    source_path = ""
    source_path = getSourceDir()

# Read the directory and create the current and new episode lists, displaying them in the comparison panel
def getSourceMaterial():

    # Check for source directory either manually entered or through filedialog
    orig_path = source_path
    if orig_path == source_path:
        print("All Good Source")
        print(orig_path)
    if not orig_path:
        print("Not Good. Get manual path from Entry box")
        orig_path = source_var.get()
        # Check to make sure the path is, at the very least, valid
        if not os.path.exists(orig_path):
            print("Invalid text in Entry box, getting through filedialog")
            dir_path_source = filedialog.askdirectory(title="Please select a folder")
            orig_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
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
            if extension in videoFormats:
                currentEpisodeList.append(file)
            if extension in subFormats:
                currentSubList.append(file)
            # else:
            #     currentEpisodeList.append(file)
    
    # Check of initial lists
    print(currentEpisodeList)
    print(currentSubList)

    # Sort lists (NOT NEEDED AT THIS TIME)
    # ok_to_sort = messagebox.askyesno("Sort Needed?", "Does this need to be sorted?")
    # if ok_to_sort:
    #     currentEpisodeList.sort(key=str.lower)
    #     currentSubList.sort(key=str.lower)
    #     # General lists check, post sort
    #     print (currentEpisodeList)
    #     print (currentSubList)

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
        if a == 1:
            text_box_left.insert("end", currentEpisodeList[a-1] + " -> " + newEpisodeList[a-1])
        else: 
            text_box_left.insert("end", "\n" + currentEpisodeList[a-1] + " -> " + newEpisodeList[a-1])
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
    
    print(newEpisodeList)
    print(newSubList)

def renameFiles():

    # Check for source directory either manually entered or through filedialog
    orig_path = source_path
    if orig_path == source_path:
        print("All Good Rename")
        print(orig_path)
    if not orig_path:
        print("Not Good. Get manual path from Entry box")
        orig_path = source_var.get()
        # Check to make sure the path is, at the very least, valid
        if not os.path.exists(orig_path):
            print("Invalid text in Entry box, getting through filedialog")
            dir_path_source = filedialog.askdirectory(title="Please select a folder")
            orig_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
            print(orig_path)

    # OLD: Check to make sure that the lists appear correct. No longer needed due to inclusion of text boxes and seperation of get and rename functionality
    # Manual stop point to allow for comparison of the two lists
    # ok_to_proceed = messagebox.askyesno("Proceed?", "Ok to proceed?")
    # if ok_to_proceed:
    #     i = start
    #     j = start
    #     x = 0
    #     y = 0
    #     for oldEpisodeName in currentEpisodeList:
    #         dst = str("".join(newEpisodeList[x]))
    #         src = str(orig_path) + oldEpisodeName
    #         dst = str(orig_path) + dst
    #         os.rename(src, dst)
    #         i += 1
    #         x += 1
    #     for oldSubName in currentSubList:
    #         dst = str("".join(newSubList[y]))
    #         src = str(orig_path) + oldSubName
    #         dst = str(orig_path) + dst
    #         os.rename(src, dst)
    #         j += 1
    #         y += 1
    # else:
    #     quit()

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
    
    currentEpisodeList.clear()
    currentSubList.clear()
    newEpisodeList.clear()
    newSubList.clear()

window = tk.Tk()
window.title("TV Show Plex Renamer")
window.geometry("550x450")

currentEpisodeList = []
currentSubList = []
newEpisodeList = []
newSubList = []
videoFormats = [".mp4",".m4v",".flv",".mkv",".mov",".avi",".mts",".mpeg",".wmv",".mpg",".h264",".3g2",".3gp",".rm",".swf",".vob"]
subFormats = [".sub",".srt",".sbv"]
start = 1
source_path = ""
source_var = tk.StringVar()
season_var = tk.StringVar()
showname_var = tk.StringVar()

# Season Details panel, and associated text boxes and buttons
show_frame = ttk.LabelFrame(window, text="Show Details", relief=tk.RIDGE)
show_frame.grid(row=1, column=1, sticky=tk.S + tk.E + tk.W + tk.N)

my_label = tk.Label(show_frame, text="Season File Path")
my_label.grid(row=1, column=1)

file_path = tk.Entry(show_frame, width=75, textvariable=source_var)
file_path.grid(row=2, column=1, columnspan=2)

show_name_label = tk.Label(show_frame, text="Show Name")
show_name_label.grid(row=3, column=1)
show_name_entry = tk.Entry(show_frame, width=50, textvariable=showname_var)
show_name_entry.grid(row=4, column=1)

season_number_label = tk.Label(show_frame, text="Season Number")
season_number_label.grid(row=3, column=2)
season_number_spinbox = tk.Spinbox(show_frame, from_=1, to=100, width=5, textvariable=season_var)
season_number_spinbox.grid(row=4, column=2)

test_source_button = tk.Button(show_frame, text="Browse")
test_source_button.grid(row=2, column=3)
test_source_button['command'] = assignSourceDir

# Action Panel, and associated buttons
action_panel = ttk.LabelFrame(window, text="Actions", relief=tk.RIDGE)
action_panel.grid(row=2, column=1, sticky=tk.S + tk.E + tk.W + tk.N)

start_label = tk.Label(action_panel, text="Get Episode List")
start_label.grid(row=1, column=1)
start_button = tk.Button(action_panel, text="Get")
start_button.grid(row=1, column=2, sticky=tk.E + tk.W)
start_button['command'] = getSourceMaterial

start_label = tk.Label(action_panel, text="Rename Episodes")
start_label.grid(row=1, column=3)
start_button = tk.Button(action_panel, text="Start")
start_button.grid(row=1, column=4, sticky=tk.E + tk.W)
start_button['command'] = renameFiles

clear_label = tk.Label(action_panel, text="Clear Comparison")
clear_label.grid(row=1, column=5)
clear_button = tk.Button(action_panel, text="Clear")
clear_button.grid(row=1, column=6, sticky=tk.E + tk.W)
clear_button['command'] = clearText

quit_label = tk.Label(action_panel, text="Exit Renamer")
quit_label.grid(row=2, column=1)
quit_button = tk.Button(action_panel, text="Exit")
quit_button.grid(row=2, column=2)
quit_button['command'] = window.destroy

test_button_label = tk.Label(action_panel, text="Path and List Check")
test_button_label.grid(row=2, column=3)
test_source_button = tk.Button(action_panel, text="Test")
test_source_button.grid(row=2, column=4)
test_source_button['command'] = sourceCheck

# Text panel, and associated text box
text_panel = ttk.LabelFrame(window, relief=tk.RIDGE, text="Comparison Panel")
text_panel.grid(row=3, column=1, sticky=tk.S + tk.E + tk.W + tk.N)

text_box_left = tk.Text(text_panel, height=15, width=60)
text_box_left.grid(row=1, column=1)

# Removed text box, printed comparisons in same box
# text_box_right = tk.Text(text_panel, height=15, width=30)
# text_box_right.grid(row=1, column=2)

window.mainloop()