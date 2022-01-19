import numpy as np
import cv2 as cv
import time
# import matplotlib.pyplot as plt

# Load previously saved data
with np.load('R1.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]



def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img
def draw2(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
    return img

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
axis = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],[0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])


cap = cv.VideoCapture(0)
img1 = cv.imread('fotos/box1.jpg',cv.IMREAD_GRAYSCALE)          # queryImage

#limitando fps de leitura
frame_rate = 60
prev = 0

while(True):

    time_elapsed = time.time() - prev
    # Capture frame-by-frame
    ret, img2 = cap.read()

    if time_elapsed > 1./frame_rate:
        prev = time.time()

        img2Gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)


        # Display the resulting frame
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
        
    
    # Initiate ORB detector
        orb = cv.ORB_create()
        # find the keypoints and descriptors with ORB
        kp1, des1 = orb.detectAndCompute(img1,None)
        kp2, des2 = orb.detectAndCompute(img2Gray,None)
        pts = cv.KeyPoint_convert(kp1)
        pts3d = np.insert(pts, 2, 1, axis=1)
        # print("kp1.x")
        # print(len(pts))

        pts2d = cv.KeyPoint_convert(kp2)


        # create BFMatcher object
        bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
        # Match descriptors.
        matches = bf.match(des1,des2)
        # Sort them in the order of their distance.
        matches = sorted(matches, key = lambda x:x.distance)
        # for m,n in matches:
        #     if m.distance < 0.7*n.distance:
        #         good.append(m)


        
        limite = 0
        distanciaMaxima = 40
        a = []
        b = []
        for i in range(len(matches)):
            a.append(matches[i].trainIdx)
            b.append(matches[i].queryIdx)
            # print(matches[i].distance)
            if(matches[i].distance < distanciaMaxima):
                limite = i-1

        # print("b:")
        # print(b)

        pts2dd = np.asarray(pts2d) 
        pts3dd = np.asarray(pts3d) 

        pts2dd = pts2dd[a]
        pts3dd = pts3dd[b]


        # Draw first 10 matches.
        img3 = cv.drawMatches(img1,kp1,img2Gray,kp2,matches[:20000],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        print(limite)
        if limite > 5:
            print("RA")
            ret,rvecs, tvecs = cv.solvePnP(pts3dd[:limite], pts2dd[:limite], mtx, dist)
            width = img1.shape[0]
            heigth = img1.shape[1]
            axis1 = np.float32([[0,0,1],[0,width,1],[heigth,0,1],[heigth,width,1]])
            # axis1 = np.float32([[0,0,1],[0,img1.width,1]])
            imgpts, jac = cv.projectPoints(axis1, rvecs, tvecs, mtx, dist)
            # print(imgpts[1][0][1])
            # print(imgpts[0][0][1])
            largura = int(imgpts[1][0][1] - imgpts[0][0][1])
            altura = int(imgpts[3][0][1] - imgpts[2][0][1])
            # print(largura)
            # print(altura)
            # cv.rectangle(img3,(imgpts[0][0][0],imgpts[0][0][1]),(imgpts[3][0][0],imgpts[3][0][1]),(0,255,0),3)
            if(int(imgpts[0][0][1]) > -10 and int(imgpts[0][0][1]) < 1000):
                print(int(imgpts[0][0][1]))
                # cv.rectangle(img2,(imgpts[0][0][0],imgpts[0][0][1]),(imgpts[3][0][0],imgpts[3][0][1]),(0,255,0),3)
            # project 3D points to image plane
            imgpts, jac = cv.projectPoints(10*axis, rvecs, tvecs, mtx, dist)       
            img2 = draw2(img2,pts2d,imgpts)
        cv.imwrite('frame.png',img2)
        cv.imwrite('frameSaida.png',img3)
        print("frame")
        cv.imshow('frame',img2)

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

