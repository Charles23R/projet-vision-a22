
import numpy as np
import cv2 as cv
import operator

from threading import Thread

class HandDetection(Thread):
    def run(self):
        self.camera = cv.VideoCapture(0, cv.CAP_DSHOW)

        # Set width and height of camera
        self.width, self.height = 640, 480
        self.camera.set(3,self.width)
        self.camera.set(4,self.height)

        # Define region of interest (ROI) coordinates
        self.top, self.right, self.bottom, self.left = 120, 320, 480, 640

        # initialize mask threshold
        self.min_hue, self.min_saturation, self.min_value = 0, 48, 80
        self.max_hue, self.max_saturation, self.max_value = 20, 255, 255
        self.init_trackbars()

        # useful for circle gesture
        self.circle_buffer = [0] * 20
        self.circle_index = 0

        # define a variable to stop the mainloop
        self.__stop = False

        print("Place your hand inside the green box.")
        self.mainloop()

    def __init__(self, event_queues, debug=True):
        Thread.__init__(self)
        self.event_queues = event_queues
        #debug mode draws the contour, hull, fingertips and concavities
        self.debug = debug
        self.start()
    def callback(self) :
        self.__stop = True

    def mainloop(self):
        while self.camera.isOpened():

            # Read and mirror frame
            _, frame = self.camera.read()
            frame = cv.flip(frame, 1)

            # Create region of interest (ROI) highlighted in green in the frame
            roi = frame[self.top:self.bottom, self.right:self.left]

            # Get HSV based skin mask
            self.update_mask_values()
            lower = [self.min_hue, self.min_saturation, self.min_value]
            upper = [self.max_hue, self.max_saturation, self.max_value]
            mask = self.get_skin_mask(roi, lower=lower, upper=upper)

            try:
                # Get contour based on mask
                contour = self.get_contour(mask)
                # Get center
                center = self.get_center(contour)
                # Get convex hull
                hull = cv.convexHull(contour)
                hull_hollow = cv.convexHull(contour, returnPoints=False)

                #Get convexity defects (space between fingers)
                defects = cv.convexityDefects(contour, hull_hollow)

                #count number of fingers
                count, fingertip_list, concavities_list = self.detect_fingers(defects, contour)

                minDist = 15
                param1 = 30 #500
                param2 = 16 #200 #smaller value-> more false circles
                minRadius = 15
                maxRadius = 100 #10

                circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
                # If some circle is found
                n_circles = 0
                if circles is not None:
                    # Get the (x, y, r) as integers
                    circles = np.round(circles[0, :]).astype("int")
                    n_circles = len(circles)

                i = self.circle_index
                self.circle_buffer[i] = 1 if n_circles == 1 else 0
                self.circle_index = 0 if i == len(self.circle_buffer)-1 else i + 1
                
                circle_gesture = False
                if self.circle_buffer.count(1) > 10:
                    circle_gesture = True
                
                #### SEND ALL DATA to event threads
                data = count, center, list(fingertip_list), list(concavities_list), circle_gesture
                for event_queue in self.event_queues :
                        event_queue.put(data)
                
                # Draw bunch of stuff
                if self.debug:

                    cv.drawContours(roi, [contour], 0, (255,255,0), 2)
                    cv.drawContours(roi, [hull], 0, (0, 255, 255), 2)
                    cv.circle(roi, center, 7, (0, 0, 255), -1)
                    self.draw_circles(frame, fingertip_list, (0, 255, 0))
                    self.draw_circles(frame, concavities_list, (0, 255, 255))
                    cv.putText(frame, str(count), (0, 50), cv.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0) , 2, cv.LINE_AA)
                    
                    if circles is not None :
                        # loop over the circles
                        for (x, y, r) in circles:
                            img_coord = tuple(map(operator.add, (x, y), (self.right, self.top)))
                            if self.debug :
                                cv.circle(frame, img_coord, r, (0, 255, 0), 2)

            except ValueError:
                # If the mask is 100% black, no contours will be found and get_contour will throw a ValueError
                pass

            # draw ROI
            cv.rectangle(frame, (self.left, self.top), (self.right, self.bottom), (0,255,0), 2)


            cv.imshow('frame', frame)
            cv.imshow('mask', mask)

            cv.waitKey(1)

            # stop the loop
            if self.__stop :
                self.camera.release()
                cv.destroyAllWindows()
                print("Bye bye!")

    def get_skin_mask(self, img, lower=[0, 48, 80], upper=[20, 255, 255]):
        hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        skinRegionHSV = cv.inRange(hsvim, np.array(lower), np.array(upper))
        kernel = np.ones((5,5), np.uint8)
        mask = cv.dilate(skinRegionHSV, kernel, iterations=1)
        return mask

    def get_contour(self, mask):
        contours,_ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key=cv.contourArea)
        return contour

    def get_center(self, contour):
        M = cv.moments(contour)
        center = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        return center

    def detect_fingers(self, defects, contour):
        concavity_list = set()
        fingertip_list = set()
        end_list = set()

        cnt = 0
        if defects is not None:

            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])
                a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  #      cosine theorem
                if angle <= np.pi / 2 and (a, b) > (40, 40):  # angle less than 90 degree, and fingers are more than 40 pixels of lenght, treat as fingers
                    cnt += 1
                    concavity_list.add(far)
                    fingertip_list.add(start)
                    end_list.add(end)

            # since we only add the starting point of the defects, we will be missing one fingertip
            # the end point which is far from fingertips is the one
            outsider_list = set()
            for end_pt in end_list:
                outsider = True
                for tip_pt in fingertip_list:
                    if np.linalg.norm(tuple(map(operator.sub, end_pt, tip_pt))) < 30:
                        outsider = False
                if outsider:
                    outsider_list.add(end_pt)

            # add the outsider end point to fingertip list
            for out in outsider_list:
                fingertip_list.add(out)

            if cnt > 0:
                cnt += 1
        return cnt, fingertip_list, concavity_list


    def draw_circles(self, frame, coords, color = (0, 255, 0), top = 120, right = 320):
        for coord in coords:
            img_coord = tuple(map(operator.add, coord, (right, top)))
            cv.circle(frame, img_coord, 4, color, -1)

    def update_mask_values(self):
        self.min_hue = cv.getTrackbarPos('min_hue', 'Track Bars')
        self.min_saturation = cv.getTrackbarPos('min_sat', 'Track Bars')
        self.min_value = cv.getTrackbarPos('min_value', 'Track Bars')
        
        self.max_hue = cv.getTrackbarPos('max_hue', 'Track Bars')
        self.max_saturation = cv.getTrackbarPos('max_sat', 'Track Bars')
        self.max_value = cv.getTrackbarPos('max_value', 'Track Bars')

    def init_trackbars(self):
        #empty function
        def doNothing(x):
            pass

        #creating a resizable window named Track Bars
        cv.namedWindow('Track Bars', cv.WINDOW_NORMAL)

        #creating track bars for gathering threshold values of red green and blue
        cv.createTrackbar('min_hue', 'Track Bars', 0, 255, doNothing)
        cv.createTrackbar('min_sat', 'Track Bars', 0, 255, doNothing)
        cv.createTrackbar('min_value', 'Track Bars', 0, 255, doNothing)

        cv.createTrackbar('max_hue', 'Track Bars', 0, 255, doNothing)
        cv.createTrackbar('max_sat', 'Track Bars', 0, 255, doNothing)
        cv.createTrackbar('max_value', 'Track Bars', 0, 255, doNothing)

        cv.setTrackbarPos('min_hue', 'Track Bars', 0)
        cv.setTrackbarPos('min_sat', 'Track Bars', 48)
        cv.setTrackbarPos('min_value', 'Track Bars', 80)


        cv.setTrackbarPos('max_hue', 'Track Bars', 20)
        cv.setTrackbarPos('max_sat', 'Track Bars', 255)
        cv.setTrackbarPos('max_value', 'Track Bars', 255)

    pass


if __name__ == '__main__': 

    hand_detection = HandDetection([])

    import time
    time.sleep(10)

    hand_detection.callback()

