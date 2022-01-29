import os
import cv2
import mysql.connector as mysql
import threading
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
from keras_preprocessing.image import img_to_array

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    db="facemask"
)
cursor = db.cursor()
detected ="true"
timerStarted="false"
global path
path="C:/xampp/htdocs/RealTimeFaceMaskMonitoringNew/admin_panel/CV-Mask-detection-master/CV-Mask-detection-master/source/newimages/"


print(path)
def startTimer():
     threading.Timer(7.0,startTimer).start()
     global detected
     detected= "false"
     
def preprocess_face_frame(face_frame):
    # convert to RGB
    global img
    global timerStarted
    if timerStarted=="false":
        startTimer()
        timerStarted ="true"
    face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
    # preprocess input image for mobilenet
    img=face_frame
    face_frame_resized = cv2.resize(face_frame, (224, 224))
    face_frame_array = img_to_array(face_frame_resized)

    return face_frame_array

def decode_prediction(pred):
    global i
    
    (mask, no_mask) = pred
     
  
    global detected
    global db
    global timerStarted 
    mask_or_not = "Mask" if mask > no_mask else "No mask"
    confidence = f"{(max(mask, no_mask) * 100):.2f}"
    if timerStarted=="false":
         startTimer()
         timerStarted ="true"
         
    if mask_or_not == "No mask" and  detected =="false":
        i=0
        s='i'
        images=cv2.imwrite(str(path)+ '.'+str(i)+ '.jpg',img)
        def convertToBinaryData(images):
   
            with open(images, 'rb') as images:
                binaryData = images.read()
            return binaryData
        def insertBLOB(images):
            print("Inserting BLOB ")
            try:
                sql ="INSERT INTO 2ndnotification(mask_or_not ,confidence,imge)VALUES(%s,%s,%s)"
                empPicture = convertToBinaryData(images)
                cursor.execute(sql,('false',confidence,empPicture));
                db.commit()
                print("Image inserted successfully as a BLOB into table")

                # select DATE_FORMAT(LastLoginTime,'%k:%i') as `Time`
            finally:
                if db.connect():
                    cursor.close()
                    db.close()
                    print("MySQL connection is closed")
                    print('record added')
        insertBLOB( path+'.'+str(i)+".jpg")
        detected="true"
        
        i+=1
       
    return mask_or_not, confidence



def write_bb(mask_or_not, confidence, box, frame):
    (x, y, w, h) = box
    color = (0, 255, 0) if mask_or_not == "Mask" else (0, 0, 255)
    label = f"{mask_or_not}: {confidence}%"

    if label==2:
        print('Hello')

    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


def load_cascade_detector():
    cascade_path = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
    face_detector = cv2.CascadeClassifier(cascade_path)
    return face_detector
