import cv2 
import pytesseract

img = cv2.imread('Format-2/9037_0255.jpg')

# Adding custom options
custom_config = r'--oem 3 --psm 6'
pytesseract.image_to_string(img, config=custom_config)