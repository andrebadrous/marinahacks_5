import cv2 as cv
import dlib

def main():
    frontal_face_detection()

def frontal_face_detection():
    capture = cv.VideoCapture(0)

    hog_face_detector = dlib.get_frontal_face_detector()

    dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    num = 0
    while True:
        isTrue, frame = capture.read()
        if not isTrue:
            break

        frame = rescaleFrame(frame)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = hog_face_detector(gray)

        for face in faces:
            face_landmarks = dlib_facelandmark(gray, face)

            for n in range(0,68):
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                cv.circle(frame, (x, y), 1, (0, 255, 255), 1)

        cv.imshow("Face Landmarks", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv.destroyAllWindows()

def rescaleFrame(frame, scale=0.60):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

if __name__ == "__main__":
    main()