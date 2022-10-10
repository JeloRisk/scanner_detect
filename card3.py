# library
from tkinter import BaseWidget
from weakref import WeakSet
import cv2
import numpy as np
from PIL import Image
import math
import datetime


def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.01 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest
src ='scanner_detect/input/water2.jpg'
img1 = Image.open(src)
img2 = cv2.imread(src)

# start of resize
width, height = img1.size
print(str(height) +" : "+ str(width))
print(str(math.floor(height/2)) + " " + str(math.floor(width/2)))
baseheight = 500
wpercent = (baseheight / img1.size[1])
wsize = int((float(img1.size[0]) * float(wpercent)))
print("img: " + str(wsize) + " " + str(baseheight))
img  = cv2.resize(img2, (math.floor(wsize), math.floor(baseheight)))
# end of resize

img_original = img.copy()

# start of contouring

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 20, 30, 30)
edged = cv2.Canny(gray, 20, 100)


contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

biggest = biggest_contour(contours)

cv2.drawContours(img, [biggest], -1, (0, 255, 0), 3)


points = biggest.reshape(4, 2)
input_points = np.zeros((4, 2), dtype="float32")

points_sum = points.sum(axis=1)
input_points[0] = points[np.argmin(points_sum)]
input_points[3] = points[np.argmax(points_sum)]

points_diff = np.diff(points, axis=1)
input_points[1] = points[np.argmin(points_diff)]
input_points[2] = points[np.argmax(points_diff)]

(top_left, top_right, bottom_right, bottom_left) = input_points
bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
# end of contouring

max_width = max(int(bottom_width), int(top_width))
# max_height = max(int(right_height), int(left_height))
max_height = int(max_width * 1.414)  # for A4


converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])


matrix = cv2.getPerspectiveTransform(input_points, converted_points)
img_output = cv2.warpPerspective(img_original, matrix, (max_width, max_height))


gray = np.stack((gray,) * 3, axis=-1)
edged = np.stack((edged,) * 3, axis=-1)

# start of showing output
img_hor = np.hstack((img_original, gray, edged, img))
cv2.imshow("Contour detection", img_hor)
cv2.imshow("Warped perspective", img_output)

cv2.imwrite('scanner_detect/output/document.jpg', img_output)
# end of showing output

# to open the program that detect the color
exec(open('scanner_detect/detect_color.py').read())
##

# line of codes where some data will store in csv
# need to modify
import csv
fields=[datetime.datetime.now(),src,baseheight,wsize]
print(datetime.datetime.now())
with open(r'scanner_detect/result.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

cv2.waitKey(0)