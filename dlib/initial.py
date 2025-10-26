import cv2 as cv
import dlib
from enum import Enum
import numpy as np
import tensorflow as tf
import pandas as pd
import os


class State(Enum):
    Sad = 0
    Happy = 1
    Mad = 2
    Relaxed = 3
    Shocked = 4
    Confused = 5
    freaky = 6


#print(State(0).name)
#print(State.Sad.value)

def main():
    frontal_face_detection()

def frontal_face_detection():
    num = 0
    row = []
    ################################
    dataset_frame_dir = "../data/frames/freaky"
    image_path = "frames/freaky"
    
    thing = ["image_path", "width", "height", "label"]
    for i in range(68):
        thing.append("x"+str(i))
        thing.append("y"+str(i))

    df_coordinates = pd.DataFrame(columns=thing)

    capture = cv.VideoCapture(0)

    hog_face_detector = dlib.get_frontal_face_detector()

    dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    while True:
        isTrue, frame = capture.read()
        if not isTrue:
            break

        frame = rescaleFrame(frame)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        H, W = frame.shape[:2]
        faces = hog_face_detector(gray)

        for face in faces:    
            array = np.array([])

            height_crop, width_crop= add_frame_to_dataset(dataset_frame_dir, num, gray, face)
            
            face_landmarks = dlib_facelandmark(gray, face)

            for n in range(0,68):
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                array = np.append(array, [x,y])
                cv.circle(frame, (x, y), 1, (0, 255, 255), 1)
            array_norm = (array - np.array([face.left(), face.top()]*68, np.float32)) 
            final_array = array_norm / np.array([width_crop, height_crop]*68, np.float32)
            #########################
            info = np.append([image_path+"frame" + str(num) + ".jpg", width_crop, height_crop, 6], final_array)
            df_coordinates.loc[len(df_coordinates)] = info
            num += 1

        cv.imshow("Face Landmarks", frame)

        if cv.waitKey(5) & 0xFF == ord('q'):
            break

    ###################
    df_coordinates.to_csv("../data/andre_freaky.csv")

    capture.release()
    cv.destroyAllWindows()

def rescaleFrame(frame, scale=0.60) -> tuple:

    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

def add_frame_to_dataset(dataset_frame_dir, num, frame, face):

    cropped_frame = frame[face.top():face.bottom(), face.left():face.right()]
    image_filename = os.path.join(dataset_frame_dir, "frame" + str(num) + ".jpg")
    cv.imwrite(image_filename, cropped_frame)
    return cropped_frame.shape

if __name__ == "__main__":
    main()
