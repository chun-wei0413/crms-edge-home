import cv2


def extract_first_frame(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()  # Read the first frame
    if ret:  # Check if a frame was returned
        cv2.imwrite(output_path, frame)
    else:
        print("No frame could be read from the video.")
    cap.release()

