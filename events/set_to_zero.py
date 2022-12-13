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
import time
import math
from utils import orientation_of_2_points, in_zooming_treshold
####

def task(stop_event, media_player, event_queue):

    #### put your variables here
    mov_detected_flag = False
    zoom_started_flag = False
    start_time = 0

    ####

    while not stop_event.is_set() :
        try :
            nb_fingers, center, fingertips, concavities, circle_gesture = event_queue.get(timeout = 2)

            #### put your code here

            if not mov_detected_flag :

                # if the hand has 4 fingers raised, and they form a circle shape
                if nb_fingers == 4 and circle_gesture :
                    mov_detected_flag = True
                    start_time = time.time()
            
            # if the hand has 4 fingers raised, and they form a circle shape
            else :
                if nb_fingers != 4 or not circle_gesture:
                        mov_detected_flag = False

                else:
                    if time.time() - start_time > 0.5:
                        media_player.seekVideo(0)
                        time.sleep(0.1)
                        media_player.pauseVideo()

            ####

            event_queue.task_done()
        except queue.Empty : pass
