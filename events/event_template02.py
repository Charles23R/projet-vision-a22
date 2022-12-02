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
    first_flag = False
    start_time = 0

    ####

    while not stop_event.is_set() :
        try :
            nb_fingers, center, fingertips, concavities = event_queue.get(timeout = 2)

            #### put your code here

            if not first_flag :

                # if the hand has 2 fingers raised, start a timer
                if nb_fingers == 2 :
                    first_flag = True
                    start_time = time()
            
            # if the hand has 2 fingers raised
            else :
                # if there is a change in the number of fingers raised, start over
                if nb_fingers != 2 : first_flag = False
                
                # if the hand keeps 3 fingers raised for 5 seconds, play the video
                if time() - start_time > 2 :
                    media_player.playAgain()
                    first_flag = False

            ####

            event_queue.task_done()
        except queue.Empty : pass
