from tkinter import *
import time
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo

# Le site de TKvideoPlayer : https://pypi.org/project/tkvideoplayer/
# Pour installer théoriquement c'est : pip install tkvideoplayer
# De la doc sur le player : https://github.com/PaulleDemon/tkVideoPlayer/blob/master/Documentation.md

window = Tk()
window.title("Media Player for Hand Detection")
window.geometry("1280x720")
window.configure(bg="white")

interface = Frame(window)#, width=1900, height=200)
interface.configure(bg="white")
interface.pack(side=TOP, pady=2)

videoplayer=None

## -----------------------------------------------------------------
## ----------------- Ouverture Fichier -----------------------------
## -----------------------------------------------------------------

def open_preset():  # Ouvrir un fichier déjà défini
    global videoplayer
    global affiche
    global duree

    if videoplayer is not None :
        videoplayer.destroy()
        duree.destroy()

    videoplayer = TkinterVideo(master=window, scaled=True)
    videoplayer.load(r"/Users/joffreyliagre/Desktop/Projets/Avatar.mp4") #Il faut changer le path 
    global filename
    filename="/Users/joffreyliagre/Desktop/Projets/Avatar.mp4"
    videoplayer.pack(expand=True, fill="both")
    videoplayer.play()
    videoplayer.bind('<<SecondChanged>>',actualiseTps)

    duree = Frame(window, width=1000, height=30)
    duree.configure(bg="red")
    duree.pack(side=BOTTOM, pady=2)
    
    affiche = Button(duree, text=str(int(videoplayer.current_duration())))
    affiche.pack(side=BOTTOM, padx=5)

    global zooming
    zooming=1

def open_file(): # Demander à l'utilisateur de choisir son fichier video
    file = askopenfile(mode='r', filetypes=[('Video Files', ["*.mp4"])])
    if file is not None:
        global videoplayer
        global affiche
        global duree

        if videoplayer is not None :
            videoplayer.destroy()
            duree.destroy()

        global filename
        filename = file.name
        videoplayer = TkinterVideo(master=window, scaled=True)#, pre_load=False)
        videoplayer.load(r"{}".format(filename))
        videoplayer.pack(expand=True, fill="both")
        videoplayer.play()
        videoplayer.bind('<<SecondChanged>>',actualiseTps)

        duree = Frame(window, width=1000, height=30)
        duree.configure(bg="red")
        duree.pack(side=BOTTOM, pady=2)
    
        affiche = Button(duree, text=str(int(videoplayer.current_duration())))
        affiche.pack(side=BOTTOM, padx=5)

        global zooming
        zooming=1

## -------------------------------------------------------------
## ----------------- Les Fonctions -----------------------------
## -------------------------------------------------------------

def actualiseTps(eventObject): # Affiche le temps de la video 01:23sec par exemple
    tps_sec=int(videoplayer.current_duration())
    disp_min=tps_sec//60
    disp_sec=tps_sec%60
    affiche.config(text=("%d : %d" % (disp_min,disp_sec)))

def actualiseTps2(): # Même fonction mais version sans eventObject
    tps_sec=int(videoplayer.current_duration())
    disp_min=tps_sec//60
    disp_sec=tps_sec%60
    affiche.config(text=("%d : %d" % (disp_min,disp_sec)))

def playAgain():
    print(filename)
    videoplayer.play()
 
def StopVideo():    # Ferme la video
    print(filename)
    videoplayer.stop()
    videoplayer.destroy()
    affiche.destroy()
    duree.destroy()

def PauseVideo():
    print(filename)
    videoplayer.pause()
    actualiseTps2()

def SeekVideo(tps): # Aller à un instant tps de la video
    print(filename)
    videoplayer.seek(int(tps))

def forward(tps): #Avancer de tps dans la video
    print(filename)
    moment=videoplayer.current_duration()
    if videoplayer.is_paused() : #On relance la video pour voir le changement
        videoplayer.play()
        videoplayer.seek(int(moment+tps))
        time.sleep(0.1)
        videoplayer.pause()
    else :
        videoplayer.seek(int(moment+tps))
    actualiseTps2()

def Originale(): # Revenir à la taille originale
    print(filename)
    global zooming
    zooming=1
    informations=videoplayer.video_info()
    a=informations['framesize']
    if videoplayer.is_paused() : #On relance la video pour voir le changement
        videoplayer.play()
        videoplayer.set_size(a)
        time.sleep(0.1)
        videoplayer.pause()
    else :
        videoplayer.set_size(a)

def SizeVideo(a): # Changer la taille de la vidéo pour une valeur fixe (640,520) par exemple
    print(filename)
    if videoplayer.is_paused() : #On relance la video pour voir le changement
        videoplayer.play()
        videoplayer.set_size(a)
        # time.sleep(2) j'arrive pas à faire marcher ça
        videoplayer.pause()
    else :
        videoplayer.set_size(a)

def Zoom(x): # Zoomer dans la vidéo pour multiplier la taille originale
    print(filename)
    global zooming
    zooming*=x
    informations=videoplayer.video_info()
    framesize=informations['framesize']
    new_X=int(zooming*framesize[0])
    new_Y=int(zooming*framesize[1])
    videoplayer.set_size((new_X,new_Y))
    
## -----------------------------------------------------------
## ----------------- Les Boutons -----------------------------
## -----------------------------------------------------------

lbl1 = Label(interface, text="Video Player", bg="white", fg="black", font="none 24 bold")
lbl1.config(anchor=CENTER)
lbl1.pack()

openbtn = Button(interface, text='Choose Video', command=lambda: open_file())
openbtn.pack(side=LEFT, padx=1)

openpresetbtn = Button(interface, text='Preset Video', command=lambda: open_preset())
openpresetbtn.pack(side=LEFT, padx=1)
 
stopbtn = Button(interface, text='Close', command=lambda: StopVideo())
stopbtn.pack(side=LEFT, padx=14)

playbtn = Button(interface, text='Play Video', command=lambda: playAgain())
playbtn.pack(side=LEFT, padx=1)
 
pausebtn = Button(interface, text='Pause Video', command=lambda: PauseVideo())
pausebtn.pack(side=LEFT, padx=1)

backbtn = Button(interface, text='- 10sec', command=lambda: forward(-10))
backbtn.pack(side=LEFT, padx=1)

forw1btn = Button(interface, text='+ 10sec', command=lambda: forward(10))
forw1btn.pack(side=LEFT, padx=1)
 
size2btn = Button(interface, text='Zoom x1/2', command=lambda: Zoom(1/2))
size2btn.pack(side=LEFT, padx=1)

size1btn = Button(interface, text='Taille Original', command=lambda: Originale())
size1btn.pack(side=LEFT, padx=1)

size2btn = Button(interface, text='Zoom x2', command=lambda: Zoom(2))
size2btn.pack(side=LEFT, padx=1)

window.mainloop()