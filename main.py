from queue import Queue
from threading import Thread, Event

from media_player import MediaPlayer
from hand_detection import HandDetection

from events import pause_play, event_template03, set_to_zero, event_skip #, ...

#### EVENTS ####
ALL_EVENTS = [
    pause_play.task,
    event_template03.task,
    set_to_zero.task,
    event_skip.task,
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
hand_detection = HandDetection(event_queues, debug=True)

# stop everything if media_player is stopped
media_player.join()
hand_detection.callback()
for stop_event in stop_events : stop_event.set()