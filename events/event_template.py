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



####

def task(stop_event, media_player, event_queue):

    #### put your variables here



    ####

    while not stop_event.is_set() :
        try :
            nb_fingers, center, fingertips, concavities, circle_gesture = event_queue.get(timeout = 2)
            #print(nb_fingers, center, fingertips, concavities)

            #### put your code here


            #media_player.pause()
            ####

            event_queue.task_done()
        except queue.Empty : pass
