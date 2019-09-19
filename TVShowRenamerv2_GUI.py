import os
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import TVShowRenamerv2_Lists as tvls

class Renamer_GUI:

    def __init__(self):
        
        self.source_var = tk.StringVar()
        self.showname_var = tk.StringVar()
        self.season_var = tk.StringVar()

    def create_gui(self, window):
        
        # Season Details panel, and associated text boxes and buttons
        show_frame = ttk.LabelFrame(window, text="Show Details", relief=tk.RIDGE)
        show_frame.grid(row=1, column=1, sticky=tk.S + tk.E + tk.W + tk.N)

        file_path_label = ttk.Label(show_frame, text="Season File Path")
        file_path_label.grid(row=1, column=1)
        file_path_entry = ttk.Entry(show_frame, width=75, textvariable=self.source_var)
        file_path_entry.grid(row=2, column=1, columnspan=2)

        show_name_label = ttk.Label(show_frame, text="Show Name")
        show_name_label.grid(row=3, column=1)
        show_name_entry = ttk.Entry(show_frame, width=50, textvariable=self.showname_var)
        show_name_entry.grid(row=4, column=1)

        season_number_label = ttk.Label(show_frame, text="Season Number")
        season_number_label.grid(row=3, column=2)
        self.season_var.set('1')
        season_number_spinbox = ttk.Spinbox(show_frame, text='1', from_=1, to=100, width=5, textvariable=self.season_var)
        season_number_spinbox.grid(row=4, column=2)

        test_source_button = ttk.Button(show_frame, text="Browse")
        test_source_button.grid(row=2, column=3)
        test_source_button['command'] = self.getSourceDir

        # Action Panel, and associated buttons
        action_panel = ttk.LabelFrame(window, text="Actions", relief=tk.RIDGE)
        action_panel.grid(row=2, column=1, sticky=tk.S + tk.E + tk.W + tk.N)

        start_label = ttk.Label(action_panel, text="Get Episode List")
        start_label.grid(row=1, column=1)
        start_button = ttk.Button(action_panel, text="Get")
        start_button.grid(row=1, column=2, sticky=tk.E + tk.W)
        start_button['command'] = self.getSourceMaterial

        start_label = ttk.Label(action_panel, text="Rename Episodes")
        start_label.grid(row=1, column=3)
        start_button = ttk.Button(action_panel, text="Start")
        start_button.grid(row=1, column=4, sticky=tk.E + tk.W)
        start_button['command'] = self.renameFiles

        clear_label = ttk.Label(action_panel, text="Clear Comparison")
        clear_label.grid(row=1, column=5)
        clear_button = ttk.Button(action_panel, text="Clear")
        clear_button.grid(row=1, column=6, sticky=tk.E + tk.W)
        clear_button['command'] = self.clearText

        quit_label = ttk.Label(action_panel, text="Exit Renamer")
        quit_label.grid(row=2, column=1)
        quit_button = ttk.Button(action_panel, text="Exit")
        quit_button.grid(row=2, column=2)
        quit_button['command'] = window.destroy

        test_button_label = ttk.Label(action_panel, text="Path and List Check")
        test_button_label.grid(row=2, column=3)
        test_source_button = ttk.Button(action_panel, text="Test")
        test_source_button.grid(row=2, column=4)
        test_source_button['command'] = self.sourceCheck

        # Text panel, and associated text box
        text_panel = ttk.LabelFrame(window, relief=tk.RIDGE, text="Comparison Panel")
        text_panel.grid(row=3, column=1, sticky=tk.S + tk.E + tk.W + tk.N)

        self.text_box_left = tk.Text(text_panel, height=15, width=60)
        self.text_box_left.grid(row=1, column=1)

        # Removed text box, printed comparisons in same box
        # text_box_right = tk.Text(text_panel, height=15, width=30)
        # text_box_right.grid(row=1, column=2)

    def pathSet(self, path_string):
        self.source_var.set(path_string)
        print("pathSet = " + self.source_var.get())

    def pathGet(self):
        file_path = self.source_var.get()
        return file_path

    def showSet(self, show_name):
        self.showname_var.set(show_name)
        print("showSet = " + self.showname_var.get())
    
    def showGet(self):
        show_name = self.showname_var.get()
        return show_name

    def seasonSet(self, season_number):
        self.showname_var.set(season_number)
        print("seasonSet = " + self.season_var.get())

    def seasonGet(self):
        season = self.season_var.get()
        return season

    # Get source directory through filedialog
    def getSourceDir(self):
        dir_path_source = filedialog.askdirectory(title="Please select a folder")
        dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
        self.pathSet(dir_path)

    def textBoxClear(self):
        self.text_box_left.delete(1,'end')

    def insertTextStart(self, current, new):
        self.text_box_left.insert("end", current + " -> " + new)
    
    def insertText(self, current, new):
        self.text_box_left.insert("end", "\n" + current + " -> " + new)

    def sourceCheck(self):    
        source_check = self.pathGet()
        print("Source Var = " + source_check)
        print(tvls.currentEpisodeList)
        print(tvls.currentSubList)
        print(tvls.newEpisodeList)
        print(tvls.newSubList)

    # Clear contents of the comparison panel
    def clearText(self):
        self.textBoxClear()
        tvls.currentEpisodeList.clear()
        tvls.currentSubList.clear()
        tvls.newEpisodeList.clear()
        tvls.newSubList.clear()
    
    # Read the directory and create the current and new episode lists, displaying them in the comparison panel
    def getSourceMaterial(self):

        # Check for source directory either manually entered or through filedialog
        orig_path = self.pathGet()
        print("Path, check 1 = " + orig_path)
        if not orig_path:
            print("No Path in Entry box. Getting Path through filedialog")
            dir_path_source = filedialog.askdirectory(title="Please select a folder")
            dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
            self.pathSet(dir_path)
            orig_path = self.pathGet()
            print("Path, check 2 = " + orig_path)

        # Check to make sure the Path is a valid path
        if not os.path.exists(orig_path):
            print("Invalid Path in Entry box, getting through filedialog")
            dir_path_source = filedialog.askdirectory(title="Please select a folder")
            dir_path = dir_path_source + "/" # Needed to make complete path, filedialogue value does not return the final slash
            self.pathSet(dir_path)
            orig_path = self.pathGet()
            print("Path, check 3 = " + orig_path)
        
        # Passed both checks
        else:
            print("Path " + orig_path + " is good.")

        # Show details
        # Also checks if entries are blank
        show_name = self.showGet()
        print("Show Name, check 1 = " + show_name)
        if not show_name:
            name = simpledialog.askstring("Name", "What is the TV Show name?")
            self.showSet(name)
            show_name = self.showGet()
            print("Show Name, check 2 = " + show_name)

        season_number = self.seasonGet()
        print("Season Number, check 1 = " + season_number)
        if not season_number:
            number = simpledialog.askstring("Season", "What is the Season number?") 
            self.seasonSet(number)
            season_number = self.seasonGet()
            print("Season Number, check 2 = " + season_number)

        if int(season_number) < 10:
            season_number = "0" + season_number

        # Filter anything but file types from the creation of the original lists, and sort between subs and video files
        for file in os.listdir(orig_path):
            if os.path.isfile(orig_path + file):
                file_orig, extension = os.path.splitext(file)
                print(extension)
                if extension in tvls.videoFormats:
                    tvls.currentEpisodeList.append(file)
                if extension in tvls.subFormats:
                    tvls.currentSubList.append(file)
                # else:
                #     currentEpisodeList.append(file)

        # Check of initial lists
        print(tvls.currentEpisodeList)
        print(tvls.currentSubList)

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
        a = tvls.start
        b = tvls.start
        for item in tvls.currentEpisodeList:
            if a < 10:
                episode_number = "0" + str(a)
            else: 
                episode_number = a
            # Need to make sure the extension is carried over
            file_orig, extension = os.path.splitext(item)
            tvls.newEpisodeList.append(show_name + " S" + season_number + "E" + str(episode_number) + extension)
            if a == 1:
                self.insertTextStart(tvls.currentEpisodeList[a-1], tvls.newEpisodeList[a-1])
            else: 
                self.insertText(tvls.currentEpisodeList[a-1], tvls.newEpisodeList[a-1])
            a += 1

        for item in tvls.currentSubList:
            if b < 10:
                episode_number = "0" + str(b)
            else: 
                episode_number = b
            # Need to make sure the extension is carried over
            file_orig, extension = os.path.splitext(item)
            tvls.newSubList.append(show_name + " S" + season_number + "E" + str(episode_number) + extension)
            b += 1

        print(tvls.newEpisodeList)
        print(tvls.newSubList)

    def renameFiles(self):

        # Check for source directory either manually entered or through filedialog
        orig_path = self.pathGet()
        if not orig_path:
            print("Get Path from Entry box")
            orig_path = self.pathGet()
            # Check to make sure the path is, at the very least, valid
            if not os.path.exists(orig_path):
                print("Invalid Path in Entry box, getting through filedialog")
                orig_path = self.pathGet()
                print(orig_path)

        i = tvls.start
        j = tvls.start
        x = 0
        y = 0
        for oldEpisodeName in tvls.currentEpisodeList:
            dst = str("".join(tvls.newEpisodeList[x]))
            src = str(orig_path) + oldEpisodeName
            dst = str(orig_path) + dst
            os.rename(src, dst)
            i += 1
            x += 1
        for oldSubName in tvls.currentSubList:
            dst = str("".join(tvls.newSubList[y]))
            src = str(orig_path) + oldSubName
            dst = str(orig_path) + dst
            os.rename(src, dst)
            j += 1
            y += 1

        self.clearText()