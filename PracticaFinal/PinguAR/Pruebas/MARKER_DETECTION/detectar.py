import cv2 as cv
from cv2 import aruco
import numpy as np

# Get the Aruco dictionary
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

param_markers = aruco.DetectorParameters()

cap = cv.VideoCapture(0)

while True:
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read the frame")
        break

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    marker_corners, marker_ids, rejected_candidates = cv.aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)

    if marker_corners:
        for ids, corners in zip(marker_ids, marker_corners):
            cv.polylines(frame,[corners.astype(np.int32)], True, (0,255,255), 4,cv.LINE_AA)
            corners = corners.reshape(4,2)
            corners = corners.astype(int)
            top_right = corners.ravel()
            text_position = (top_right[0], top_right[1] - 10)
            cv.putText(frame, f"id: {ids[0]}", text_position, cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0), 2, cv.LINE_AA)
    # print(marker_ids)
    
    # Display the frame
    cv.imshow("frame", frame)

    # Exit on pressing 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Exit camera
cap.release()
cv.destroyAllWindows()