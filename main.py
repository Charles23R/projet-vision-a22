from queue import Queue
from threading import Thread, Event

from media_player import MediaPlayer
from hand_detection import HandDetection

from events import event_template01, event_template02, event_template03 #, ...

#### EVENTS ####
ALL_EVENTS = [
    event_template01.task,
    event_template02.task,
    event_template03.task,
    # ...
]
################
def create_all_events(event_functions, media_player):
    events = []
    for event_function in event_functions :
        stop_event = Event()
        queue = Queue()
        thread = Thread(target = event_function, args = (stop_event, media_player, queue))
        events.append((stop_event, queue, thread))
    return events
################

# set and start media_player
media_player = MediaPlayer()

# set and start all events
events = create_all_events(ALL_EVENTS, media_player)
stop_events, event_queues, event_threads = list(zip(*events))
for event_thread in event_threads : event_thread.start()

# set and start hand_detection
hand_detection = HandDetection(event_queues)

# stop everything if media_player is stopped
media_player.join()
hand_detection.callback()
for stop_event in stop_events : stop_event.set()