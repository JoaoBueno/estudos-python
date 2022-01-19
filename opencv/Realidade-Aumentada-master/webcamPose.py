import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import glob

cap = cv.VideoCapture(0)
img1 = cv.imread('fotos/box1.jpg',cv.IMREAD_GRAYSCALE)          # queryImage

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)


# Load previously saved data
# with np.load('B.npz') as X:
#     mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)


def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img



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

    # create BFMatcher object
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    # Draw first 10 matches.
    img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:40],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # plt.imshow(img3),plt.show()
    cv.imwrite('abc.png', img3)

    for fname in glob.glob('fotos/box1.jpg'):
        img2 = cv.imread(fname)
        gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (7,6),None)

        if ret == True:
            corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

            # Find the rotation and translation vectors.
            rvecs, tvecs, inliers = cv.solvePnPRansac(objp, corners2, mtx, dist)

            # project 3D points to image plane
            imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)

            img2 = draw(img2,corners2,imgpts)
            cv.imshow('frame',img2)
            k = cv.waitKey(0) & 0xff
            if k == 's':
                cv.imwrite(fname[:6]+'.png', img2)

    cv.destroyAllWindows()


    cv.imshow('frame',img2)



# When everything done, release the capture
cap.release()
cv.destroyAllWindows()