import cv2 as cv

#empty function
def doNothing(x):
    pass

#creating a resizable window named Track Bars
cv.namedWindow('Track Bars', cv.WINDOW_NORMAL)

#creating track bars for gathering threshold values of red green and blue
cv.createTrackbar('min_blue', 'Track Bars', 0, 255, doNothing)
cv.createTrackbar('min_green', 'Track Bars', 0, 255, doNothing)
cv.createTrackbar('min_red', 'Track Bars', 0, 255, doNothing)

cv.createTrackbar('max_blue', 'Track Bars', 0, 255, doNothing)
cv.createTrackbar('max_green', 'Track Bars', 0, 255, doNothing)
cv.createTrackbar('max_red', 'Track Bars', 0, 255, doNothing)

cv.setTrackbarPos('min_blue', 'Track Bars', 0)
cv.setTrackbarPos('min_green', 'Track Bars', 48)
cv.setTrackbarPos('min_red', 'Track Bars', 80)


cv.setTrackbarPos('max_blue', 'Track Bars', 20)
cv.setTrackbarPos('max_green', 'Track Bars', 255)
cv.setTrackbarPos('max_red', 'Track Bars', 255)

# reading the image
camera = cv.VideoCapture(0)
_, frame = camera.read()
frame = cv.flip(frame, 1)

# reading the image
#frame = cv.imread('anti_racism.jpg')

#resizing the image for viewing purposes
resized_image = cv.resize(frame,(400, 312))

#converting into HSV color model
hsv_image = cv.cvtColor(resized_image, cv.COLOR_BGR2HSV)

#showing both resized and hsv image in named windows
cv.imshow('Base Image', resized_image)
cv.imshow('HSV Image', hsv_image)

#creating a loop to get the feedback of the changes in trackbars
while True:
    #reading the trackbar values for thresholds
    min_blue = cv.getTrackbarPos('min_blue', 'Track Bars')
    min_green = cv.getTrackbarPos('min_green', 'Track Bars')
    min_red = cv.getTrackbarPos('min_red', 'Track Bars')
    
    max_blue = cv.getTrackbarPos('max_blue', 'Track Bars')
    max_green = cv.getTrackbarPos('max_green', 'Track Bars')
    max_red = cv.getTrackbarPos('max_red', 'Track Bars')
    
    #using inrange function to turn on the image pixels where object threshold is matched
    mask = cv.inRange(hsv_image, (min_blue, min_green, min_red), (max_blue, max_green, max_red))
    #showing the mask image
    cv.imshow('Mask Image', mask)
    # checking if q key is pressed to break out of loop
    key = cv.waitKey(25)
    if key == ord('q'):
        break

#printing the threshold values for usage in detection application
print(f'min_blue {min_blue}  min_green {min_green} min_red {min_red}')
print(f'max_blue {max_blue}  max_green {max_green} max_red {max_red}')
#destroying all windows
cv.destroyAllWindows()