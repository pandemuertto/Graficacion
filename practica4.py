import numpy as np 
import cv2 as cv

img = np.ones((500, 500), dtype=np.uint8) * 240

for i in range(500):
    for j in range(500):
        if i % 25 == 0 & j % 25 == 0:
            img[i, j] = 1 
            img[j, i] = 1

for i in range(50):
    for j in range(275):
        if i > 25:
            if j > 225:
                img[i, j] = 30
  
for i in range(100):
    for j in range(225):
        if i > 50:
            if j > 200:
                img[i, j] = 30
                
for i in range(100):
    for j in range(300):
        if i > 50:
            if j > 275:
                img[i, j] = 30
                
for i in range(150):
    for j in range(200):
        if i > 100:
            if j > 175:
                img[i, j] = 30                
         
for i in range(150):
    for j in range(325):
        if i > 100:
            if j > 300:
                img[i, j] = 30
                
for i in range(150):
     for j in range(200):
         if i > 125:
             if j > 50:
                 img[i, j] = 30                        

for i in range(150):
     for j in range(450):
         if i > 125:
             if j > 300:
                 img[i, j] = 30
         
cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()
