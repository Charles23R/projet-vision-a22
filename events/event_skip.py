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

    first_finger_x = None
    first_timer = 0
    first_nb_fingers = 0
    first_flag = False

    second_timer = 0
    second_flag = False


    ####

    while not stop_event.is_set() :
        try :
            nb_fingers, center, fingertips, concavities, circle_gesture = event_queue.get(timeout = 2)
            #print(nb_fingers, center, fingertips, concavities)

            #### put your code here
            if not(first_flag) :
                if 2 <= nb_fingers <= 5 :
                    # get the x coordinate of the finger at the left of the hand
                    first_finger_x = sorted(list(zip(*fingertips))[0])[0]
                    first_timer = time()
                    first_nb_fingers = nb_fingers
                    first_flag = True

                    block_time = 1
                    difference = 150
            
            # if a skip or a backwards has occured
            elif second_flag :
                # block skip and backwards after a skip or a backwards for Ns
                if time() - second_timer >= block_time :
                    first_flag = False
                    second_flag = False
                    print('unblock skip and backwards')
                    print()

            else :
                if time() - first_timer >= 0.2 :
                    if nb_fingers != first_nb_fingers : first_flag = False
                    else :
                        current_finger_x = sorted(list(zip(*fingertips))[0])[0]
                        time_skip = (first_nb_fingers - 1) * 5
                        
                        # skip if difference between start_center and current center is below 100 pixels
                        if current_finger_x - first_finger_x >= difference :
                            media_player.forward(time_skip)
                            print('skip', str(time_skip) + 's')

                            print('block skip and backwards for 2s')
                            second_timer = time()
                            second_flag = True
                        
                        # backwards if difference between start_center and current center is below 100 pixels
                        elif first_finger_x - current_finger_x >= difference :
                            media_player.forward(- time_skip)
                            print('backwards', str(- time_skip) + 's')

                            print('block skip and backwards for ' + str(block_time) + 's')
                            second_timer = time()
                            second_flag = True
                        
                        first_flag = False

                        
                        

            ####

            event_queue.task_done()
        except queue.Empty : pass
