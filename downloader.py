import requests
import re
import sys
import os
import time
import pipes
import pytube
from functools import partial
import tkinter as tk
from bs4 import BeautifulSoup
import re

class Downloader:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("YouTube Song Downloader")
        self.window.geometry("500x300")
        # Labels
        self.l1 = tk.Label(self.window, text="Enter Song URL", fg="black", font="Arial 10 bold")
        self.e1 = tk.Entry(self.window)
        self.b1 = tk.Button(self.window, text="CONVERT", font="Arial 8", fg="black", bg="gray", command=self.get_video_files)
        self.t1 = tk.Text(self.window, height=15, width=50)

    def get_playlist_info(self):
        index = self.url.find('list=')
        raw_html = requests.get('https://www.youtube.com/playlist?' + self.url[index:])
        html = BeautifulSoup(raw_html.content, 'html.parser')
        selection = html.findAll('a', href=True)
        video_links = []
        for link in selection:
            if(link['href'].endswith('t=0s')):
                video_links.append('https://www.youtube.com' + link['href'])
        video_links = list(set(video_links))
        return video_links

    def get_video_files(self):
        self.url = self.e1.get()
        self.t1.delete('1.0', tk.END)
        if 'watch?' in self.url:
            if 'list=' in self.url:
                links = self.get_playlist_info()
            else:
                links = [self.url]
        elif 'playlist' in self.url:
            links = self.get_playlist_info()
        else:
            exit(1)
        
        for video in links:
            self.t1.insert(tk.END, 'starting Download: \n')
            pytube.YouTube(video).streams.first().download('./')
            self.t1.insert(tk.END, 'Downloaded video...\n\n')
        self.conversion()
        for file in os.listdir('./'):
            if(file.endswith('.mp4')):
                os.remove(os.path.join('./', file))
        exit(1)

    def conversion(self):
        for file in os.listdir('./'):
            if(file.endswith('.mp4')):
                self.video_to_audio(file)
    

    def video_to_audio(self, fileName):
        self.t1.insert(tk.END, "Hang on Conversion is under way...")
        try:
            file, file_extension = os.path.splitext(fileName)
            if file_extension != '.mp4':
                print("Extension of file - " + file_extension + " invalid.")
                exit(1)
            file = pipes.quote(file)
            video_to_wav = 'ffmpeg -i ' + file + file_extension + ' ' + file + '.mp3'
            final_audio = 'lame '+ file + '.mp3'
            os.system(video_to_wav)
            os.system(final_audio)
            self.t1.insert(tk.END, "sucessfully converted " + fileName + " into audio!")
        except OSError as err:
            print(err.reason)
            exit(1)

    def DisplayWindow(self):
        self.l1.pack(fill=tk.X, pady=10)
        self.e1.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)
        self.b1.pack(side=tk.TOP)
        self.t1.pack(side=tk.TOP, pady=5)
        
        # Show the Window
        self.window.mainloop()

def main():
    obj = Downloader()
    obj.DisplayWindow()
    obj.get_video_files()



if __name__ == '__main__':
    main()