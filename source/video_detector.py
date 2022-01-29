import time
import numpy as np
import cv2
import imutils
import mysql.connector
import time
from threading import Event
from imutils.video import VideoStream
from tensorflow import keras
from tensorflow.python.keras.applications.mobilenet_v2 import preprocess_input

from source.utils import preprocess_face_frame, decode_prediction, write_bb, load_cascade_detector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    db="facemask"
)
cursor = mydb.cursor()

model = keras.models.load_model('models/mask_mobilenet.h5')
face_detector = load_cascade_detector()


def video_mask_detector():
    video = VideoStream(src=0).start()
    time.sleep(1.0)
    while True:
        # Capture frame-by-frame
        frame = video.read()

        frame = detect_mask_in_frame(frame)
        # Display the resulting frame
        # show the output frame
        cv2.imshow("Mask detector", frame)

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    # cleanup
    cv2.destroyAllWindows()
    video.stop()


def detect_mask_in_frame(frame):
    frame = imutils.resize(frame, width=500)

    # convert an image from one color space to another
    # (to grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray,
                                           scaleFactor=1.1,
                                           minNeighbors=5,
                                           minSize=(40, 40),
                                           flags=cv2.CASCADE_SCALE_IMAGE,
                                           )

    faces_dict = {"faces_list": [],
                  "faces_rect": []
                  }
    count=0              
    for rect in faces:
        (x, y, w, h) = rect
        face_frame = frame[y:y + h, x:x + w]
        # preprocess image
        face_frame_prepared = preprocess_face_frame(face_frame)

        faces_dict["faces_list"].append(face_frame_prepared)
        faces_dict["faces_rect"].append(rect)
        count+=1
    cv2.putText(frame, f'Total Persons : {count}', (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.3, (0, 0, 255), 2)
    
    def executedb():
        global mydb
        cv2.putText(frame, f'Threshold Exceed, Crowd detected', (20,50), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 0, 255), 2)
        total = str(count)
        sql = "INSERT INTO notification (studentid, detected, totalperson) VALUES ('Crowd','Crowd has been detected', '"+ total  +"')"
        cursor.execute(sql)
        mydb.commit()
       
        print(cursor.rowcount, "record inserted.")  

    if count==1:
       
        executedb()

  
    if faces_dict["faces_list"]:
        faces_preprocessed = preprocess_input(np.array(faces_dict["faces_list"]))
        preds = model.predict(faces_preprocessed)

        for i, pred in enumerate(preds):
            mask_or_not, confidence = decode_prediction(pred)
            write_bb(mask_or_not, confidence, faces_dict["faces_rect"][i], frame)

    return frame


if __name__ == '__main__':
    video_mask_detector()
