import math

def orientation_of_2_points(pt1, pt2):
    dy = pt2[1] - pt1[1]
    dx = pt2[0] - pt1[0]
    return math.degrees(math.atan2(dy, dx))

def in_zooming_treshold(angle):
    return (angle < -30 and angle > -60) or (angle > 120 and angle < 160)