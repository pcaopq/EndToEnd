import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

img = cv2.imread("0003_medium.jpg")
img  = cv2.medianBlur(img,5)
kernel = np.ones((20,2),np.uint8)
img  = cv2.erode(img,kernel)
img  = cv2.medianBlur(img,9)

plt.imshow(img)
plt.show()
