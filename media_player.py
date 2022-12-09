from tkinter import *
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo

from threading import Thread
import time
import os


class MediaPlayer(Thread) :    
    def run(self) : 
        # Le site de TKvideoPlayer : https://pypi.org/project/tkvideoplayer/
        # Pour installer théoriquement c'est : pip install tkvideoplayer
        # De la doc sur le player : https://github.com/PaulleDemon/tkVideoPlayer/blob/master/Documentation.md

        self.window = Tk()
        self.window.title("Media Player for Hand Detection")
        self.window.geometry("720x480")
        self.window.configure(bg="white")

        self.interface = Frame(self.window) #, width=1900, height=200)
        self.interface.configure(bg="white")
        self.interface.pack(side=TOP, pady=2)


        self.filename = None
        self.videoplayer = None
        self.affiche = None
        self.duree = None
        self.zooming = None
        
        self.setup_buttons()

        self.window.mainloop()

    def __init__(self, verbose=False):
        Thread.__init__(self)
        self.is_stopped = False
        self.verbose=False
        self.start()
    def callback(self) :
        self.is_stopped = True
        self.window.quit()

    ## -----------------------------------------------------------------
    ## ----------------- Ouverture Fichier -----------------------------
    ## -----------------------------------------------------------------

    def open_preset(self):  # Ouvrir un fichier déjà défini
        if self.videoplayer is not None :
            self.videoplayer.destroy()
            self.duree.destroy()

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'avatar.mp4')  
        self.videoplayer = TkinterVideo(master=self.window, scaled=True)
        self.videoplayer.load(filename) 
        self.filename=filename
        self.videoplayer.pack(expand=True, fill="both")
        self.videoplayer.play()
        self.videoplayer.bind('<<SecondChanged>>', self.actualiseTps)

        self.duree = Frame(self.window, width=1000, height=30)
        self.duree.configure(bg="red")
        self.duree.pack(side=BOTTOM, pady=2)
        
        self.affiche = Button(self.duree, text=str(int(self.videoplayer.current_duration())))
        self.affiche.pack(side=BOTTOM, padx=5)

        self.zooming=1

    def open_file(self): # Demander à l'utilisateur de choisir son fichier video
        file = askopenfile(mode='r', filetypes=[('Video Files', ["*.mp4"])])
        if file is not None:
            if self.videoplayer is not None :
                self.videoplayer.destroy()
                self.duree.destroy()

            self.filename = file.name
            self.videoplayer = TkinterVideo(master=self.window, scaled=True)#, pre_load=False)
            self.videoplayer.load(r"{}".format(self.filename))
            self.videoplayer.pack(expand=True, fill="both")
            self.videoplayer.play()
            self.videoplayer.bind('<<SecondChanged>>',self.actualiseTps)

            self.duree = Frame(self.window, width=1000, height=30)
            self.duree.configure(bg="red")
            self.duree.pack(side=BOTTOM, pady=2)
        
            self.affiche = Button(self.duree, text=str(int(self.videoplayer.current_duration())))
            self.affiche.pack(side=BOTTOM, padx=5)

            self.zooming=1

    ## -------------------------------------------------------------
    ## ----------------- Les Fonctions -----------------------------
    ## -------------------------------------------------------------

    def actualiseTps(self, eventObject): # Affiche le temps de la video 01:23sec par exemple
        tps_sec=int(self.videoplayer.current_duration())
        disp_min=tps_sec//60
        disp_sec=tps_sec%60
        self.affiche.config(text=("%d : %d" % (disp_min,disp_sec)))

    def actualiseTps2(self): # Même fonction mais version sans eventObject
        tps_sec=int(self.videoplayer.current_duration())
        disp_min=tps_sec//60
        disp_sec=tps_sec%60
        self.affiche.config(text=("%d : %d" % (disp_min,disp_sec)))

    def playAgain(self):
        if self.verbose: print(self.filename)
        self.videoplayer.play()
    
    def stopVideo(self): # Ferme la video
        if self.verbose: print(self.filename)
        self.videoplayer.stop()
        self.videoplayer.destroy()
        self.affiche.destroy()
        self.duree.destroy()

    def pauseVideo(self):
        if self.verbose: print(self.filename)
        self.videoplayer.pause()
        self.actualiseTps2()

    def seekVideo(self, tps): # Aller à un instant tps de la video
        if self.verbose: print(self.filename)
        self.videoplayer.seek(int(tps))

    def forward(self, tps): #Avancer de tps dans la video
        if self.verbose: print(self.filename)
        moment=self.videoplayer.current_duration()
        if self.videoplayer.is_paused() : #On relance la video pour voir le changement
            self.videoplayer.play()
            self.videoplayer.seek(int(moment+tps))
            time.sleep(0.1)
            self.videoplayer.pause()
        else :
            self.videoplayer.seek(int(moment+tps))
        self.actualiseTps2()

    def originale(self): # Revenir à la taille originale
        if self.verbose: print(self.filename)
        self.zooming=1
        informations=self.videoplayer.video_info()
        a=informations['framesize']
        if self.videoplayer.is_paused() : #On relance la video pour voir le changement
            self.videoplayer.play()
            self.videoplayer.set_size(a)
            time.sleep(0.1)
            self.videoplayer.pause()
        else :
            self.videoplayer.set_size(a)

    def sizeVideo(self, a): # Changer la taille de la vidéo pour une valeur fixe (640,520) par exemple
        if self.verbose: print(self.filename)
        if self.videoplayer.is_paused() : #On relance la video pour voir le changement
            self.videoplayer.play()
            self.videoplayer.set_size(a)
            # time.sleep(2) j'arrive pas à faire marcher ça
            self.videoplayer.pause()
        else :
            self.videoplayer.set_size(a)

    def zoom(self, x, relative=True): # Zoomer dans la vidéo pour multiplier la taille originale
        if self.verbose: print(self.filename)
        self.zooming = self.zooming * x if relative else x
        informations = self.videoplayer.video_info()
        framesize=informations['framesize']
        new_X=int(self.zooming*framesize[0])
        new_Y=int(self.zooming*framesize[1])
        self.videoplayer.set_size((new_X,new_Y))

    def get_zoom(self):
        return self.zooming

    ## -----------------------------------------------------------
    ## ----------------- Les Boutons -----------------------------
    ## -----------------------------------------------------------

    def setup_buttons(self):
        lbl1 = Label(self.interface, text="Video Player", bg="white", fg="black", font="none 24 bold")
        lbl1.config(anchor=CENTER)
        lbl1.pack()

        openbtn = Button(self.interface, text='Choose Video', command=lambda: self.open_file())
        openbtn.pack(side=LEFT, padx=1)

        openpresetbtn = Button(self.interface, text='Preset Video', command=lambda: self.open_preset())
        openpresetbtn.pack(side=LEFT, padx=1)
        
        stopbtn = Button(self.interface, text='Close', command=lambda: self.stopVideo())
        stopbtn.pack(side=LEFT, padx=14)

        playbtn = Button(self.interface, text='Play Video', command=lambda: self.playAgain())
        playbtn.pack(side=LEFT, padx=1)
        
        pausebtn = Button(self.interface, text='Pause Video', command=lambda: self.pauseVideo())
        pausebtn.pack(side=LEFT, padx=1)

        backbtn = Button(self.interface, text='- 10sec', command=lambda: self.forward(-10))
        backbtn.pack(side=LEFT, padx=1)

        forw1btn = Button(self.interface, text='+ 10sec', command=lambda: self.forward(10))
        forw1btn.pack(side=LEFT, padx=1)
        
        size2btn = Button(self.interface, text='Zoom x1/2', command=lambda: self.zoom(1/2))
        size2btn.pack(side=LEFT, padx=1)

        size1btn = Button(self.interface, text='Taille Original', command=lambda: self.originale())
        size1btn.pack(side=LEFT, padx=1)

        size2btn = Button(self.interface, text='Zoom x2', command=lambda: self.zoom(2))
        size2btn.pack(side=LEFT, padx=1)
    pass

if __name__ == "__main__":
    media_player = MediaPlayer()