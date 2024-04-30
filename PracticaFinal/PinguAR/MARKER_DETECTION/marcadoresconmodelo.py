import cv2 as cv
from cv2 import aruco
import numpy as np

 # pip install PyOpenGL PyOpenGL_accelerate
 #    1. Detect the ArUco marker using OpenCV as you're already doing in your code.
 #    2. Once the marker is detected, calculate its pose (position and orientation) in the camera frame.
 #    3. Use OpenGL to render the 3D model at the calculated pose.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pywavefront

# Function to initialize OpenGL
def init_opengl():
    glutInit()
    glutInitWindowSize(800, 600)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(b"OpenGL Window")
    glEnable(GL_DEPTH_TEST)

# Function to draw 3D model
def draw_model(model, marker_pose):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw the 3D model
    glPushMatrix()
    glTranslatef(marker_pose[0], marker_pose[1], marker_pose[2])
    glRotatef(marker_pose[3], 1, 0, 0)
    glRotatef(marker_pose[4], 0, 1, 0)
    glRotatef(marker_pose[5], 0, 0, 1)
     # Render the model
    for mesh in model.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                vertex = model.vertices[vertex_i[0]]
                normal = model.normals[vertex_i[2]]
                glNormal3f(*normal)
                glVertex3f(*vertex)
        glEnd()

    glPopMatrix()

    glutSwapBuffers()
    glPopMatrix()

    glutSwapBuffers()

# Load 3D model
def load_model(model_path):
    try:
        return pywavefront.Wavefront(model_path)
    except Exception as e:
        print("Error loading model:", e)
        return None


####

# Get the Aruco dictionary
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters()
cap = cv.VideoCapture(0)



# Initialize OpenGL window
init_opengl()

# Load 3D model
model_path = r"/Users/juanl/Documents/GitHub/Practicas_CUIA/PracticaFinal/PinguAR/Models/pingui2.obj"
model = load_model(model_path)


if model is None:
    print("Error: Unable to load 3D model.")
    exit()
else:
    print("3D model loaded successfully.")


while True:
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read the frame")
        break

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    marker_corners, marker_ids, rejected_candidates = aruco.detectMarkers(gray_frame, marker_dict, parameters = param_markers)

    if marker_ids is not None and 1 in marker_ids:
        index = np.where(marker_ids == 1)[0][0]
        marker_corners = np.array(marker_corners)
        corners = marker_corners[index].reshape(4, 2)
        corners = corners.astype(int)
        top_right = corners[0]
        marker_pose = [top_right[0], top_right[1], 10, 0, 0, 0]  # Placeholder pose
        draw_model(model, marker_pose)

    # print(marker_ids)
    
    # Display the frame
    cv.imshow("frame", frame)

    # Exit on pressing 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Exit camera
cap.release()
cv.destroyAllWindows()