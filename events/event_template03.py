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

                # if the hand has 2 fingers raised, and they are in the right orientation, start a timer
                if nb_fingers == 2 :
                    if in_zooming_treshold(orientation_of_2_points(fingertips[0], fingertips[1])):
                        mov_detected_flag = True
                        start_time = time()
            
            # if the hand has 2 fingers raised, and they are in the right orientation
            else :
                if nb_fingers != 2:
                        mov_detected_flag = False
                        zoom_started_flag = False

                else:
                    if not in_zooming_treshold(orientation_of_2_points(fingertips[0], fingertips[1])):
                        mov_detected_flag = False
                        zoom_started_flag = False
                    
                    else:
                        if not zoom_started_flag:
                            # if the fingers were raised for 0.3 seconds, start the zooming process
                            if time() - start_time > 0.3 :
                                zoom_started_flag = True
                                distance_0 = math.dist(fingertips[0], fingertips[1])
                                zoom_0 = media_player.get_zoom()
                                start_time = time()
                        
                        else:
                            # apply a zoom proportionnal to distance of fingers now vs at time 0
                            if time() - start_time > 0.05:
                                distance = math.dist(fingertips[0], fingertips[1])
                                zoom = distance / distance_0
                                media_player.zoom(zoom * zoom_0, relative=False)
                                start_time = time()

            ####

            event_queue.task_done()
        except queue.Empty : pass
