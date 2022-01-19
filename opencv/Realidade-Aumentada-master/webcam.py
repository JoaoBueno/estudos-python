import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


cap = cv.VideoCapture(0)
# img1 = cv.imread('fotos/box1.jpg',cv.IMREAD_GRAYSCALE)          # queryImage
img1 = cv.imread('fotos/eu.jpg',cv.IMREAD_GRAYSCALE)          # queryImage

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Display the resulting frame
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


    
    
    img2 = gray

    
    # Initiate ORB detector
    orb = cv.ORB_create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)
    pts = cv.KeyPoint_convert(kp1)
    pts3d = np.insert(pts, 2, 1, axis=1)
    print("kp1.x")
    print(pts3d)
    
    # print("kp1.y")
    # print(kp1.y)
    # print("des1")
    # print(des1)

    # create BFMatcher object
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    # Draw first 10 matches.
    img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:200000],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # plt.imshow(img3),plt.show()

    cv.imshow('frame',img3)



# When everything done, release the capture
cap.release()
cv.destroyAllWindows()