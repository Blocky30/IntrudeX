import tkinter as tk
import pygame
import threading

pygame.mixer.init()
music_player_window = None

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("800x600")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="black")
        self.music_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.music_listbox.configure(bg="black", fg="lightgreen")
        self.music_listbox.pack()
        self.music_options = [
            "Music/HOME - Dream Head.mp3",
            "Music/HOME - Head First.mp3",
            "Music/HOME - Resonance.mp3",
            "Music/HOME - Twisted Light.mp3",
        ]
        for music in self.music_options:
            self.music_listbox.insert(tk.END, music)
        self.music_listbox.config(width=30)
        self.music_listbox.bind("<Double-1>", self.play_selected_music)
        self.volume_slider = tk.Scale(root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, label="Volume", command=self.update_volume)
        self.volume_slider.set(1)
        self.volume_slider.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.handle_close)
    def play_selected_music(self, event):
        selection = self.music_listbox.curselection()
        if selection:
            index = selection[0]
            music_file = self.music_options[index]
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self.volume_slider.get())
            pygame.mixer.music.play(loops=-1)
    def update_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))
    def handle_close(self):
        global music_player_window
        pygame.mixer.music.stop()
        self.root.destroy()
        music_player_window = None
def create_music_player():
    global music_player_window
    if music_player_window is None:
        root = tk.Tk()
        app = MusicPlayer(root)
        music_player_window = root
        root.mainloop()
    else:
        music_player_window.lift()
        music_player_window.attributes('-topmost', True)
        music_player_window.attributes('-topmost', False)
def handleTunes(args=None):
    create_music_player()