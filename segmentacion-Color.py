# Este programa en Python utiliza OpenCV para segmentar una imagen de frutas 
# por colores específicos (rojo, amarillo, verde, azul y naranja). 
# A través del modelo de color HSV, se generan máscaras para cada color, lo que permite aislar 
# visualmente diferentes tipos de frutas u objetos en la imagen según su color.


import cv2 as cv

img = cv.imread('frutass.jpg', 1)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

red=(10, 255, 255)
red1=(0, 40 ,40)
red2=(180, 255, 255)
red3=(170, 40,40)
mask_red1 = cv.inRange(hsv, red1, red)
mask_red2 = cv.inRange(hsv, red3, red2)
mask_red = mask_red1+mask_red2
res = cv.bitwise_and(img, img, mask=mask_red)

yellow1 = (20, 100, 100)
yellow2 = (30, 255, 255)
yellow3 = (35, 100, 100)
mask_yellow1 = cv.inRange(hsv, yellow1, yellow2)
mask_yellow2 = cv.inRange(hsv, yellow3, yellow2)
mask_yellow = mask_yellow1 + mask_yellow2
res_yellow = cv.bitwise_and(img, img, mask=mask_yellow)

green1 = (40, 100, 100)
green2 = (60, 255, 255)
green3 = (55, 175, 175)
mask_green1 = cv.inRange(hsv, green1, green2)
mask_green2 = cv.inRange(hsv, green3, green2)
mask_green = mask_green1 + mask_green2
res_green = cv.bitwise_and(img, img, mask=mask_green)

blue1 = (90, 75, 75)
blue2 = (110, 150, 200)
blue3 = (130, 250, 100)
blue4 = (120, 240, 240)
mask_blue1 = cv.inRange(hsv, blue1, blue2)
mask_blue2 = cv.inRange(hsv, blue3, blue2)
mask_blue3 = cv.inRange(hsv, blue3, blue4)
mask_blue = mask_blue1 + mask_blue2 + mask_blue3
res_blue = cv.bitwise_and(img, img, mask=mask_blue)

orange1 = (15, 150, 150)
orange2 = (20, 255, 255)
mask_orange = cv.inRange(hsv, orange1, orange2)
res_orange = cv.bitwise_and(img, img, mask=mask_orange)

cv.imshow('ROJO', res)
cv.imshow('AMARILLO', res_yellow)
cv.imshow('VERDE', res_green)
cv.imshow('AZUL', res_blue)
cv.imshow('NARANJA', res_orange)
cv.waitKey(0)
cv.destroyAllWindows