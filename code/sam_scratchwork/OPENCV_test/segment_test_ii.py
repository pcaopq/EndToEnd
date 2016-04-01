import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

in_img = cv2.imread("0003_medium.jpg")
kernel = np.ones((5,2),np.uint8)
kernel1 = np.ones((5,1),np.uint8)/5
for i in range(1):
    print(i)
    in_img = cv2.erode(in_img,kernel)
    #in_img = cv2.filter2D(in_img,-1,kernel1)
    in_img = cv2.dilate(in_img,kernel)
gray = cv2.cvtColor(in_img,cv2.COLOR_BGR2GRAY)
gauss = cv2.GaussianBlur(gray,(9,9),0)
edges = cv2.Canny(gauss,10  ,100)
LSD = cv2.createLineSegmentDetector()
lines, width, prec, nfa = LSD.detect(edges)
color = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
for i in range(len(lines)):
    for x1,y1,x2,y2 in lines[i] :
        cv2.line(color,(x1,y1),(x2,y2),(0,0,255),1)
disp_in_img  = cv2.cvtColor(color,  cv2.COLOR_BGR2RGB)

plt.imshow(disp_in_img)
plt.show()
