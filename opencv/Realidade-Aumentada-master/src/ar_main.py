import argparse
import cv2
import numpy as np
import math
import os
from objloader_simple import *
import time
import copy
# Minimum number of matches that have to be found
# to consider the recognition valid
MIN_MATCHES = 10  

def main():
    """
    This functions loads the target surface image,
    """
    homography = None 
    # matrix of camera parameters (made up but works quite well for me) 
    camera_parameters = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
    # create ORB keypoint detector
    orb = cv2.ORB_create()
    # create BFMatcher object based on hamming distance  
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # load the reference surface that will be searched in the video stream
    dir_name = os.getcwd()
    model = cv2.imread(os.path.join(dir_name, '../reference/box1.jpg'), 0)
    # model = cv2.blur(model,(3,3))
    # Compute model keypoints and its descriptors
    kp_model, des_model = orb.detectAndCompute(model, None)
    # Load 3D model from OBJ file
    obj = OBJ(os.path.join(dir_name, "../models/fox.obj"), swapyz=True)  
    # obj = OBJ(os.path.join(dir_name, "../models/muscular_amazon.obj"), swapyz=True)  
    # obj = OBJ(os.path.join(dir_name, "../obj_models/zangief.obj"), swapyz=True)  
    # obj = OBJ(os.path.join(dir_name, "../obj_models/uv_sphere.obj"), swapyz=True)  

    
    # init video capture
    cap = cv2.VideoCapture(0)
    start = time.time()

    dst_old = np.array([[0,0],[0,0],[0,0],[0,0]])
    projection_old = np.array([])
    projection = np.array([])
    zeroo = np.array([[0,0],[0,0],[0,0],[0,0]])
    while True:
        mudou = False
        
        # print(time.time() - start)
        if(time.time() - start > 0.000001):
            start = time.time()
            # print("hello")
            # end = time.time()
            # print(end - start)

            # read the current frame
            ret, frame = cap.read()
            # frame = cv2.blur(frame,(3,3))
            if not ret:
                print("Unable to capture video")
                return 
            # find and draw the keypoints of the frame
            kp_frame, des_frame = orb.detectAndCompute(frame, None)
            # match frame descriptors with model descriptors
            matches = bf.match(des_model, des_frame)
            # sort them in the order of their distance
            # the lower the distance, the better the match
            matches = sorted(matches, key=lambda x: x.distance)

            limite = 0
            distanciaMaxima = 50
            
            for i in range(len(matches)):
                # print(matches[i].distance)
                if(matches[i].distance < distanciaMaxima):
                    limite = i-1

            # compute Homography if enough matches are found
            if len(matches) > MIN_MATCHES:
                # differenciate between source points and destination points
                
                src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
                
                # src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches[:30]]).reshape(-1, 1, 2)
                # dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches[:30]]).reshape(-1, 1, 2)
                
                # compute Homography

                homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                
                
                if True:
                    
                    # Draw a rectangle that marks the found model in the frame
                    h, w = model.shape
                    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                    # project corners into frame
                    dst = cv2.perspectiveTransform(pts, homography)
                    a = dst-dst_old
                    
                    for ponto in a:
                        if(abs(ponto[0][0])>30 or abs(ponto[0][1])>30):
                            print("mudou")
                            mudou = True
                    print(dst_old)
                    
                    if(mudou):
                        frame = cv2.polylines(frame, [np.int32(dst)], True, 255, 2, cv2.LINE_AA)  
                        dst_old = copy.deepcopy(dst)
                        projection_old = copy.deepcopy(projection)
                    else:
                        frame = cv2.polylines(frame, [np.int32(dst_old)], True, 255, 2, cv2.LINE_AA)  
                    # connect them with lines  
                    # frame = cv2.polylines(frame, [np.int32(dst_old)], True, 255, 2, cv2.LINE_AA)  
                # if a valid homography matrix was found render cube on model plane
                if homography is not None:
                    try:
                        # obtain 3D projection matrix from homography matrix and camera parameters
                        projection = projection_matrix(camera_parameters, homography)  
                        if(mudou):
                            frame = render(frame, obj, projection, model,False)
                        else:
                            frame = render(frame, obj, projection_old, model,False)
                        #frame = render(frame, model, projection)
                    except:
                        pass
                # draw first 10 matches.
                if args.matches:
                    frame = cv2.drawMatches(model, kp_model, frame, kp_frame, matches[:2000000],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                    # img3 = cv.drawMatches(img1,kp1,img2Gray,kp2,matches[:20],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                # show result
                # frame = cv2.drawMatches(model, kp_model, frame, kp_frame, matches[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                print( "Not enough matches found - %d/%d" % (len(matches), MIN_MATCHES))

    cap.release()
    cv2.destroyAllWindows()
    return 0

def render(img, obj, projection, model ,color=False):
    """
    Render a loaded obj model into the current video frame
    """

    vertices = obj.vertices
    scale_matrix = np.eye(3) * 2
    h, w = model.shape
    # print(color)
    # print("qtd de faces:",len(obj.faces) )
    
    for face in obj.faces:
        # print("aaaaaa")
        face_vertices = face[0]
        points = np.array([vertices[vertex - 1] for vertex in face_vertices])
        points = np.dot(points, scale_matrix)
        # render model in the middle of the reference surface. To do so,
        # model points must be displaced
        points = np.array([[p[0] + w / 2, p[1] + h / 2, p[2]] for p in points])
        # points = np.array([[p[0], p[1], p[2]] for p in points])
        dst = cv2.perspectiveTransform(points.reshape(-1, 1, 3), projection)
        imgpts = np.int32(dst)
        if color is False:
            cv2.fillConvexPoly(img, imgpts, (137, 0, 0))
        else:
            # print("face[-1]: ",face[-1])
            # color = hex_to_rgb(face[-1])
            # color = color[::-1]  # reverse
            # print("color",color)
            cv2.fillConvexPoly(img, imgpts, tuple([face[-1][0],face[-1][1],face[-1][2]]))
            # cv2.fillConvexPoly(img, imgpts, tuple([1,50,64]))
    return img

def projection_matrix(camera_parameters, homography):
    """
    From the camera calibration matrix and the estimated homography
    compute the 3D projection matrix
    """
    # Compute rotation along the x and y axis as well as the translation
    homography = homography * (-1)
    rot_and_transl = np.dot(np.linalg.inv(camera_parameters), homography)
    col_1 = rot_and_transl[:, 0]
    col_2 = rot_and_transl[:, 1]
    col_3 = rot_and_transl[:, 2]
    # normalise vectors
    l = math.sqrt(np.linalg.norm(col_1, 2) * np.linalg.norm(col_2, 2))
    rot_1 = col_1 / l
    rot_2 = col_2 / l
    translation = col_3 / l
    # compute the orthonormal basis
    c = rot_1 + rot_2
    p = np.cross(rot_1, rot_2)
    d = np.cross(c, p)
    rot_1 = np.dot(c / np.linalg.norm(c, 2) + d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_2 = np.dot(c / np.linalg.norm(c, 2) - d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_3 = np.cross(rot_1, rot_2)
    # finally, compute the 3D projection matrix from the model to the current frame
    projection = np.stack((rot_1 , rot_2, rot_3, translation)).T
    return np.dot(camera_parameters, projection)

def hex_to_rgb(hex_color):
    print(tuple([int(hex(hex_color[2]).split('x')[-1]),int(hex(hex_color[1]).split('x')[-1]),int(hex(hex_color[0]).split('x')[-1])]))
    return tuple([int(hex(hex_color[2]).split('x')[-1]),int(hex(hex_color[1]).split('x')[-1]),int(hex(hex_color[0]).split('x')[-1])])
    # return tuple([hex(hex_color[2]).split('x')[-1],hex(hex_color[1]).split('x')[-1],hex(hex_color[0]).split('x')[-1])])
    


# Command line argument parsing
# NOT ALL OF THEM ARE SUPPORTED YET
parser = argparse.ArgumentParser(description='Augmented reality application')

parser.add_argument('-r','--rectangle', help = 'draw rectangle delimiting target surface on frame', action = 'store_true')
parser.add_argument('-mk','--model_keypoints', help = 'draw model keypoints', action = 'store_true')
parser.add_argument('-fk','--frame_keypoints', help = 'draw frame keypoints', action = 'store_true')
parser.add_argument('-ma','--matches', help = 'draw matches between keypoints', action = 'store_true')
# TODO jgallostraa -> add support for model specification
#parser.add_argument('-mo','--model', help = 'Specify model to be projected', action = 'store_true')

args = parser.parse_args()

if __name__ == '__main__':
    main()
