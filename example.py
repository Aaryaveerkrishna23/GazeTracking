"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import dlib
import pandas as pd
from matplotlib import pyplot as plt
import cv2
from gaze_tracking import GazeTracking
import gaze_tracking
#from Visualization import Visualization

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1366)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

#image = cv2.imread(gaze_tracking.path)



while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()
    #out.write(frame)

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)


    frame = gaze.annotated_frame()
    #image=gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

#out.release()
class Visualization():
    df = pd.read_csv("data_csv.csv", names=['xleft','yleft','xright','yright','xrightyleft','xleftyright'])

    plt.plot(df.xleft, df.yleft)
    plt.plot(df.xright, df.yright)
    #plt.plot((df.xleft + df.yleft) / 2, (df.xright + df.yright) / 2)
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.legend(['Left Eye', 'Right Eye'])
    plt.show()

plot = Visualization()
