from __future__ import division
import os
import cv2
import dlib
from eye import Eye
from calibration import Calibration
import pandas as pd
import pyautogui
from dataset import data
import csv
pyautogui.FailSafeException= False

# path = r'.\test2.PNG'
# image = cv2.imread(path)

datalist = data()
class GazeTracking(object):
    """9
    This class tracks the user's gaze.
    It provides useful information like the position of the eyes
    and pupils and allows to know if the eyes are open or closed
    """


    def __init__(self):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()

        # _face_detector is used to detect faces
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor is used to get facial landmarks of a given face
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detects the face and initialize Eye objects"""
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)

        try:
            landmarks = self._predictor(frame, faces[0])
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)

        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, frame):
        """Refreshes the frame and analyzes it.

        Arguments:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame
        self._analyze()

    def pupil_left_coords(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.origin[0] + self.eye_left.pupil.x
            y = self.eye_left.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def pupil_right_coords(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_left.pupil.x
            y = self.eye_right.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def horizontal_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        horizontal direction of the gaze. The extreme right is 0.0,
        the center is 0.5 and the extreme left is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def vertical_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        vertical direction of the gaze. The extreme top is 0.0,
        the center is 0.5 and the extreme bottom is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def is_right(self):
        """Returns true if the user is looking to the right"""
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.35

    def is_left(self):
        """Returns true if the user is looking to the left"""
        if self.pupils_located:
            return self.horizontal_ratio() >= 0.65

    def is_center(self):
        """Returns true if the user is looking to the center"""
        if self.pupils_located:
            return self.is_right() is not True and self.is_left() is not True

    def is_blinking(self):
        """Returns true if the user closes his eyes"""
        if self.pupils_located:
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            return blinking_ratio > 3.8

    def annotated_frame(self):
       # global df
        #"""Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)

            #print(df.head())
            # while True:
            #     if cv2.waitKey(1) == 27:
            #         break
            #     else:
            # print("BYYYYYY")
            # while True:
            #     print("HIIIIIIIIIIIIIII")
            x_left, y_left = self.pupil_left_coords()

            datalist.xleftlist.append(x_left) #appending the data in list
            datalist.yleftlist.append(y_left) #appending the data in list
            x_right, y_right = self.pupil_right_coords()
            datalist.xrightlist.append(x_right) #appending the data in list
            datalist.yrightlist.append(y_right) #appending the data in list
            datalist.avg_x.append((x_left+y_left)/2)
            datalist.avg_y.append((x_right + y_right) / 2)
            with open('data_csv.csv', 'a',  newline = "") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([x_left,y_left, x_right, y_right, (x_right+x_left)/2, (y_right+y_left)/2])
            # global df
            # df = pd.DataFrame({'xleft':datalist.xleftlist, 'yleft':datalist.yleftlist, 'xright':datalist.xrightlist, 'yright':datalist.yrightlist, 'average_x':datalist.avg_x, 'average_y':datalist.avg_y}) #creating a new Dataframe
            # writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
            # df.to_excel(writer,sheet_name='Sheet 1') #writing the dataframe in excel
            # writer.save()
            #df.to_csv('G:\RAIT\BE Project\GazeTracking-master\GazeTracking-master\gaze_tracking\data.csv', header=True)
            #pyautogui.moveTo((x_left+x_right)/2, (y_left+y_right)/2)
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)
        # if cv2.waitKey(1) == 27:
        #     df.to_csv('G:\RAIT\BE Project\GazeTracking-master\GazeTracking-master\gaze_tracking\data.csv',mode='a',header=True)
        #     #break

        return frame
    #def saveresult():
# global df
# df.to_csv(r'G:\RAIT\BE Project\GazeTracking-master\GazeTracking-master\gaze_tracking\data.csv', mode='a',header=False)
#global df
#GazeTracking.saveresult(GazeTracking.annotated_frame)
    #df.to_csv(r'G:\RAIT\BE Project\GazeTracking-master\GazeTracking-master\gaze_tracking\data.csv', mode='a',header=False)
