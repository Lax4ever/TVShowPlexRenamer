import os
import tkinter as tk 
from tkinter import ttk, filedialog, simpledialog
import TVShowRenamerv2_Lists as tvls # Houses the lists of supported video and subtitle formats as well as the blank dictionaries
import platform

class Renamer_GUI:

    def __init__(self):
        
        self.source_var = tk.StringVar() # file path in string format
        self.showname_var = tk.StringVar() # show name in string format
        self.season_var = tk.StringVar() # season number in string format

    def create_gui(self, window):
        # Season Details panel, and associated text boxes, frames, and buttons

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
        self.text_panel = ttk.LabelFrame(window, relief=tk.RIDGE, text="Comparison Panel")
        self.text_panel.grid(row=3, column=1, sticky=tk.S + tk.E + tk.W + tk.N)

    def pathSet(self, path_string):
    # Set the working directory path in the file path Entry box
        self.source_var.set(path_string)
        print("pathSet = " + self.source_var.get())

    def pathGet(self):
    # Get the working directory as shown in the file path Entry box
        file_path = self.source_var.get()
        return file_path

    def showSet(self, show_name):
    # Set the name of the Show in the show name Entry box
        self.showname_var.set(show_name)
        print("showSet = " + self.showname_var.get())
    
    def showGet(self):
    # Get the name of the Show as shown in the show name Entry box
        show_name = self.showname_var.get()
        return show_name

    def seasonSet(self, season_number):
    # Allows the Season Number to be set programmatically if not entered in the Season Number box
        self.showname_var.set(season_number)
        print("seasonSet = " + self.season_var.get())

    def seasonGet(self):
    # Gets the Season Number as shown in the Season Number box
        season = self.season_var.get()
        return season

    def getSourceDir(self):
    # Get source directory through filedialog    
        dir_path_source = filedialog.askdirectory(title="Please select a folder")
        dir_path = dir_path_source + self.platformCheck() # Needed to make complete path, filedialogue value does not return the final slash
        self.pathSet(dir_path)

    def sourceCheck(self):
    # Allows for checking of the file path and dictionaries        
        source_check = self.pathGet()
        print("Source Var = " + source_check)
        print(f"episodes: {tvls.episodes}")
        print(f"subtitles: {tvls.subtitles}")

    def clearText(self):
    # Clear contents of the comparison panel    
        for eps in tvls.episodes:
            tvls.episodes[eps]["currentText"].destroy()
            tvls.episodes[eps]["newText"].destroy()
            tvls.episodes[eps]["toggle"].destroy()
        tvls.episodes.clear()
        tvls.subtitles.clear()
    
    def getSourceMaterial(self):
    # Read the directory and create the episode and subtitle dictionaries, displaying the episode changes in the comparison panel

        # Check for source directory either manually entered or through filedialog
        orig_path = self.pathGet()
        print("Path, check 1 = " + orig_path)
        if not orig_path:
            print("No Path in Entry box. Getting Path through filedialog")
            dir_path_source = filedialog.askdirectory(title="Please select a folder")
            dir_path = dir_path_source + self.platformCheck() # Needed to make complete path, filedialogue value does not return the final slash
            self.pathSet(dir_path)
            orig_path = self.pathGet()
            print("Path, check 2 = " + orig_path)

        # Check to make sure the Path is a valid path
        if not os.path.exists(orig_path):
            print("Invalid Path in Entry box, getting through filedialog")
            dir_path_source = filedialog.askdirectory(title="Please select a folder")
            dir_path = dir_path_source + self.platformCheck() # Needed to make complete path, filedialogue value does not return the final slash
            self.pathSet(dir_path)
            orig_path = self.pathGet()
            print("Path, check 3 = " + orig_path)
        
        # Passed both checks
        else:
            if orig_path[-1] != self.platformCheck():
                dir_path = orig_path + self.platformCheck()
                self.pathSet(dir_path)
                orig_path = self.pathGet()
                print(f"Path, final check = {orig_path}")
            else: 
                print("Path " + orig_path + " is good.")

        # Get show details already entered and request details that are missing
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

        # Create dictionaries for episodes and subtitle files. Creates one of the text boxes and the checkbox for the episodes in the comparison panel
        ep_num = tvls.start
        for file in os.listdir(orig_path):
            if os.path.isfile(orig_path + file):
                _, extension = os.path.splitext(file)
                if extension in tvls.videoFormats:
                    tvls.episodes[f"E{ep_num}"] = {"currentName": file}
                    tvls.episodes[f"E{ep_num}"].update({"currentText": tk.Text(self.text_panel, height=1, width=(len(tvls.episodes[f"E{ep_num}"]["currentName"])) + 8), "toggle": tk.Checkbutton(self.text_panel)})
                    tvls.episodes[f"E{ep_num}"]["currentText"].insert('end', f'{tvls.episodes[f"E{ep_num}"]["currentName"]}  --->')
                    tvls.episodes[f"E{ep_num}"]["currentText"].grid(row=(ep_num), column=1)
                    tvls.episodes[f"E{ep_num}"]["toggle"].grid(row=(ep_num), column=3)
                    ep_num += 1

        sub = tvls.start
        for file in os.listdir(orig_path):
            if os.path.isfile(orig_path + file):
                _, extension = os.path.splitext(file)
                if extension == ".idx":
                    tvls.subtitles[f"S{sub}"] = {"currentIDXName": file}
                # Check if supported subtitle format
                if extension in tvls.subFormats:
                    if f"S{sub}" in tvls.subtitles.keys():
                        tvls.subtitles[f"S{sub}"].update({"currentSubName": file})
                        sub += 1
                    else:
                        tvls.subtitles[f"S{sub}"] = {"currentSubName": file}
                        sub += 1


        # Check of initial dictionaries
        # print(f"Current Episodes: {tvls.episodes}")
        # print(f"Current Subs: {tvls.currentSubList}")

        # Update the episode and subtitle dictionaries with the new name format, adding the final text box to the comparison panel
        a = tvls.start
        ep_num = tvls.start
        for eps in tvls.episodes:
            if a < 10:
                episode_number = "0" + str(a)
            else: 
                episode_number = a
            # Need to make sure the extension is carried over
            _, extension = os.path.splitext(tvls.episodes[eps]["currentName"])
            new_name = show_name + " S" + season_number + "E" + str(episode_number) + extension
            tvls.episodes[f"E{ep_num}"].update({"newName": new_name}) 
            tvls.episodes[f"E{ep_num}"].update({"newText": tk.Text(self.text_panel, height=1, width=(len(tvls.episodes[f"E{ep_num}"]["newName"]) + 2))})
            tvls.episodes[f"E{ep_num}"]["newText"].insert('end', tvls.episodes[f"E{ep_num}"]["newName"])
            tvls.episodes[f"E{ep_num}"]["newText"].grid(row=(ep_num), column=2)
            a += 1
            ep_num += 1  

        b = tvls.start
        sub = tvls.start
        for subs in tvls.subtitles:
            if b < 10:
                episode_number = "0" + str(b)
            else: 
                episode_number = b
            # Create new IDX file name, if current exists
            if "currentIDXName" in tvls.subtitles[f"S{sub}"]:
                # Need to make sure the extension is carried over
                _, extension = os.path.splitext(tvls.subtitles[subs]["currentIDXName"])
                new_name = show_name + " S" + season_number + "E" + str(episode_number) + extension
                tvls.subtitles[f"S{sub}"].update({"newIDXName": new_name})
            # Creating new file names for all other supported subtitle files
            # Need to make sure the extension is carried over
            _, extension = os.path.splitext(tvls.subtitles[subs]["currentSubName"])
            new_name = show_name + " S" + season_number + "E" + str(episode_number) + extension
            tvls.subtitles[f"S{sub}"].update({"newSubName": new_name})
            b += 1
            sub += 1

        # Check of dictionaries with new episode/sub names
        # print(f"New Episodes: {tvls.episodes}")
        # print(f"New Subs {tvls.newSubList}")

    def renameFiles(self):
    # Rename the supported video and subtitle files using the new names in the appropriate dictionaries

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

        # Rename files
        for eps in tvls.episodes:
            src = orig_path + tvls.episodes[eps]["currentName"]
            dst = orig_path + tvls.episodes[eps]["newName"]
            os.rename(src, dst)
        for subs in tvls.subtitles:
            if "currentIDXName" in tvls.subtitles[subs]:
                idx_src = str(orig_path) + tvls.subtitles[subs]["currentIDXName"]
                idx_dst = str(orig_path) + tvls.subtitles[subs]["newIDXName"]
                os.rename(idx_src, idx_dst)
            src = str(orig_path) + tvls.subtitles[subs]["currentSubName"]
            dst = str(orig_path) + tvls.subtitles[subs]["newSubName"]
            os.rename(src, dst)

        # Clear the comparison panel
        self.clearText()
    
    def platformCheck(self):
        # Checks the OS to return the correct slash type for file paths
        if platform.system() == "Linux":
            return "/"
        elif platform.system() == "Darwin":
            return "/"
        else:
            return "\\"