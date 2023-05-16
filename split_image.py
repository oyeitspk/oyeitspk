# import cv2
# import sys

# SCALE = 4
# AREA_THRESHOLD = 427505.0 / 2

# def show_scaled(name, img):
#     try:
#         h, w  = img.shape
#     except ValueError:
#         h, w, _  = img.shape
#     cv2.imshow(name, cv2.resize(img, (w // SCALE, h // SCALE)))

# def main():
#     img = cv2.imread(r'Format-2/9037_0255.jpg')
#     print(img)
#     img = img[10:-10, 10:-10] # remove the border, it confuses contour detection
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     show_scaled("original", gray)

#     # black and white, and inverted, because
#     # white pixels are treated as objects in
#     # contour detection
#     thresholded = cv2.adaptiveThreshold(
#                 gray, 255,
#                 cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
#                 25,
#                 15
#             )
#     show_scaled('thresholded', thresholded)
#     # I use a kernel that is wide enough to connect characters
#     # but not text blocks, and tall enough to connect lines.
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 33))
#     closing = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

#     im2, contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     show_scaled("closing", closing)

#     for contour in contours:
#         convex_contour = cv2.convexHull(contour)
#         area = cv2.contourArea(convex_contour)
#         if area > AREA_THRESHOLD:
#             cv2.drawContours(img, [convex_contour], -1, (255,0,0), 3)

#     show_scaled("contours", img)
#     cv2.imwrite("/tmp/contours.png", img)
#     cv2.waitKey()

# main()


#####################################################################


import cv2
import numpy as np

# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread(r'Format-2/9037_0255.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Create rectangular structuring element and dilate
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(thresh, kernel, iterations=4)

# Find contours and draw rectangle
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
print(cnts)


# count = 1
# for c in cnts:
#     x,y,w,h = cv2.boundingRect(c)
#     print(x,y,w,h)
#     #cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
#     cropped = image[y:(y+h), x:(x+w)]
#     #cv2.imshow("cropped", cropped)
#     cv2.imwrite(f'Format-2/9037_0255_x{count}.jpg',cropped)
#     count += 1

# # cv2.imshow('thresh', thresh)
# # cv2.imshow('dilate', dilate)
# # cv2.imshow('image', image)
# # cv2.waitKey()


###################################################################


# import numpy as np
# import cv2

# img = cv2.imread('Format-2/9037_0255.jpg')

# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# #play with parameters that all I changed in answer
# _,thresh = cv2.threshold(gray,20,255,cv2.THRESH_BINARY)

# # and here are 3 value returned not 2 
# contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# count = 1
# print(contours)
# for cnt in contours:
#     x,y,w,h = cv2.boundingRect(cnt)
#     crop = img[y:y+h,x:x+w]
#     cv2.imwrite(f'Format-2/9037_0255_xx{count}.jpg',crop)
#     count += 1