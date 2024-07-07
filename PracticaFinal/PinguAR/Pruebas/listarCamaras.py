import cv2

# List of device nodes to check
device_nodes = ['/dev/video0', '/dev/video1', '/dev/video2', '/dev/video3']

for device in device_nodes:
    print(f"Trying {device}...")
    cap = cv2.VideoCapture(device) 
    
    if not cap.isOpened():
        print(f"Error: Could not open video stream from {device}")
        continue

    ret, frame = cap.read()
    if ret:
        cv2.imshow(f'Camera {device}', frame)
        print(f"Displaying feed from {device}")
        # Wait for a key press to move to the next device
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"Error: Failed to capture image from {device}")
    
    cap.release()

