#########################################################
#### Les differentes fonctions du Player utilisables ####
#########################################################
## playAgain() 
## stopVideo()    / Ferme la video
## pauseVideo()
## seekVideo(tps) / Aller à un instant tps de la video
## forward(tps)   / Avancer de tps dans la video
## originale()    / Revenir a la taille originale de la video
## sizeVideo(a)   / Changer la taille de la vidéo pour une valeur fixe (640,520) par exemple
## zoom(x)        / Zoomer dans la vidéo pour multiplier la taille originale
#########################################################
#########################################################
#########################################################

import queue

#### put your imports
from time import time

####

def task(stop_event, media_player, event_queue):

    #### put your variables here
    open_hand_time = -999 # the last time 5 fingers were seen (initially : never). Reset when pause/play
    is_playing = True
    ####

    while not stop_event.is_set() :
        try :
            nb_fingers, center, fingertips, concavities = event_queue.get(timeout = 2)

            #### put your code here
            
            if nb_fingers == 5:
                open_hand_time = time()

            if nb_fingers == 0 and time() - open_hand_time < 0.5:
                if is_playing:
                    media_player.pauseVideo()
                    is_playing = False
                else:
                    media_player.playAgain()
                    is_playing = True
                open_hand_time = -999 
            ####

            event_queue.task_done()
        except queue.Empty : pass
