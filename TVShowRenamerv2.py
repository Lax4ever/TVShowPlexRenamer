import tkinter as tk
import TVShowRenamerv2_GUI as tvrg

window = tk.Tk()
window.title("TV Show Plex Renamer")
program = tvrg.Renamer_GUI()
program.create_gui(window)
window.mainloop()