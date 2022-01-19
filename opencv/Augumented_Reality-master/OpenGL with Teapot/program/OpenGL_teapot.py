import numpy as np
import cv2
import cv2.aruco as aruco
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import pygame


texture_object = None
texture_background = None
camera_matrix = None
dist_coeff = None
cap = cv2.VideoCapture(0)
INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                           [-1.0,-1.0,-1.0,-1.0],
                           [-1.0,-1.0,-1.0,-1.0],
                           [ 1.0, 1.0, 1.0, 1.0]])

################## Define Utility Functions Here #######################
"""
Function Name : getCameraMatrix()
Input: None
Output: camera_matrix, dist_coeff
Purpose: Loads the camera calibration file provided and returns the camera and
         distortion matrix saved in the calibration file.
"""
def getCameraMatrix():
        global camera_matrix, dist_coeff
        with np.load('Camera.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]



########################################################################

############# Main Function and Initialisations ########################
"""
Function Name : main()
Input: None
Output: None
Purpose: Initialises OpenGL window and callback functions. Then starts the event
         processing loop.
"""        
def main():
        glutInit()
        getCameraMatrix()
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(625, 100)
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
        window_id = glutCreateWindow("OpenGL")
        init_gl()
        glutDisplayFunc(drawGLScene)
        glutIdleFunc(drawGLScene)
        glutReshapeFunc(resize)
        glutMainLoop()

"""
Function Name : init_gl()
Input: None
Output: None
Purpose: Initialises various parameters related to OpenGL scene.
"""  
def init_gl():
        global texture_object, texture_background
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0) 
        glDepthFunc(GL_ALWAYS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)   
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        texture_background = glGenTextures(1)
        texture_object = glGenTextures(1)
"""
Function Name : resize()
Input: None
Output: None
Purpose: Initialises the projection matrix of OpenGL scene
"""
def resize(w,h):
        ratio = 1.0* w / h
        glMatrixMode(GL_PROJECTION)
        glViewport(0,0,w,h)
        gluPerspective(50, ratio, 0.1, 100)

"""
Function Name : drawGLScene()
Input: None
Output: None
Purpose: It is the main callback function which is called again and
         again by the event processing loop. In this loop, the webcam frame
         is received and set as background for OpenGL scene. ArUco marker is
         detected in the webcam frame and 3D model is overlayed on the marker
         by calling the overlay() function.
"""
def drawGLScene():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ar_list = []
        ret, frame = cap.read()
        if ret == True:
                draw_background(frame)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                
                ar_list = detect_markers(frame)
                for i in ar_list:
                        if i[0] == 8:
                                overlay(frame, ar_list, i[0],"texture_1.png")
                        if i[0] == 2:
                                overlay(frame, ar_list, i[0],"texture_2.png")
                        if i[0] == 7:
                                overlay(frame, ar_list, i[0],"texture_3.png")
                        if i[0] == 6:
                                overlay(frame, ar_list, i[0],"texture_4.png")
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
        glutSwapBuffers()
        
########################################################################

######################## Aruco Detection Function ######################
"""
Function Name : detect_markers()
Input: img (numpy array)
Output: aruco list in the form [(aruco_id_1, centre_1, rvec_1, tvec_1),(aruco_id_2,
        centre_2, rvec_2, tvec_2), ()....]
Purpose: This function takes the image in form of a numpy array, camera_matrix and
         distortion matrix as input and detects ArUco markers in the image. For each
         ArUco marker detected in image, paramters such as ID, centre coord, rvec
         and tvec are calculated and stored in a list in a prescribed format. The list
         is returned as output for the function
"""
def detect_markers(img):
        markerLength = 100
        aruco_list = []
	######################## INSERT CODE HERE ########################
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
        parameters = aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
        rvec, tvec,_= aruco.estimatePoseSingleMarkers(corners, markerLength, camera_matrix, dist_coeff)
        centrecoord= []
        if ids is None:
                return aruco_list
        else:
                L=len(ids)
        
        for i in range(0,L):
                x=int(corners[i][0][0][0]+corners[i][0][1][0]+corners[i][0][3][0]+corners[i][0][2][0])/4
                y=int(corners[i][0][0][1]+corners[i][0][1][1]+corners[i][0][3][1]+corners[i][0][2][1])/4
                p=(x,y)
                centrecoord.append(p)
        for i in range(0,L):
                x=np.array(rvec[i],ndmin=3)
                y=np.array(tvec[i],ndmin=3)
                p=(ids[i][0],centrecoord[i],x,y)
                aruco_list.append(p)
        
	##################################################################
        return aruco_list
"""
Function Name : draw_background()
Input: img (numpy array)
Output: None
Purpose: Takes image as input and converts it into an OpenGL texture. That

         OpenGL texture is then set as background of the OpenGL scene
"""
def draw_background(img):
        
        image1 = Image.fromarray(img)
        width = image1.size[0]
        height = image1.size[1]
        imggedata1 = image1.tobytes("raw", "BGRX", 0, -1)
        
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB, width, height,0, GL_RGBA, GL_UNSIGNED_BYTE, imggedata1)

        
        width1=6.40
        height1=4.80
        glBindTexture(GL_TEXTURE_2D, texture_background)
        glPushMatrix()
        glTranslatef(0.0,0.0,-10.0)
        #########################
        glBegin (GL_QUADS);
        
        #########################
        glTexCoord2f(0.0, 0.0); glVertex3f( -width1, -height1, 0.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(width1, -height1, 0.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(width1, height1, 0.0);
        glTexCoord2f(0.0, 1.0); glVertex3f( -width1,height1, 0.0);
        glEnd();
        glPopMatrix()
        return None

"""
Function Name : init_object_texture()
Input: Image file path
Output: None
Purpose: Takes the filepath of a texture file as input and converts it into OpenGL
         texture. The texture is then applied to the next object rendered in the OpenGL
         scene.
"""
def init_object_texture(image_filepath):    
    textureSurface = pygame.image.load(image_filepath)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_object)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    return None

"""
Function Name : overlay()
Input: img (numpy array), aruco_list, aruco_id, texture_file (filepath of texture file)
Output: None
Purpose: Receives the ArUco information as input and overlays the 3D Model of a teapot
         on the ArUco marker. That ArUco information is used to
         calculate the rotation matrix and subsequently the view matrix. Then that view matrix
         is loaded as current matrix and the 3D model is rendered.

         Parts of this code are already completed, you just need to fill in the blanks. You may
         however add your own code in this function.
"""

def overlay(img, ar_list, ar_id, texture_file):
        for x in ar_list:
                if ar_id == x[0]:
                        centre, rvec, tvec = x[1], x[2], x[3]
        tvec=(tvec/100)
        rmtx = cv2.Rodrigues(rvec)[0]
        offsetX=0.1
        offsetY=0.5
        view_matrix =  np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvec[0][0][0]+0.1],
                            [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvec[0][0][1]-0.5],
                            [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvec[0][0][2]],
                            [0.0       ,0.0       , 0.0  ,  1.0 ]])
        
        view_matrix = view_matrix * INVERSE_MATRIX
        view_matrix = np.transpose(view_matrix)
        
        glBindTexture(GL_TEXTURE_2D,texture_object )
        init_object_texture(texture_file)
        glPushMatrix()
        glLoadMatrixd(view_matrix)
        glutSolidTeapot(0.6)
        glPopMatrix()
        
        ####################################
        
       

########################################################################

if __name__ == "__main__":
        main()
