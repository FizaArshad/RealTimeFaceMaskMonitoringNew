import cv2
import numpy as np
import mysql.connector as mysql
import os
from PIL import Image
import numpy as np
from numpy import asarray
import threading
import matplotlib.pyplot as plt
import base64
import time
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    db="facemask"
)
cursor = db.cursor()
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

face_cascade_Path = "haarcascade_frontalface_default.xml"

path="C:/xampp/htdocs/RealTimeFaceMaskMonitoringNew/admin_panel/CV-Mask-detection-master/CV-Mask-detection-master/newimages/"

path1="C:/xampp/htdocs/RealTimeFaceMaskMonitoringNew/admin_panel/CV-Mask-detection-master/CV-Mask-detection-master/2nd/"
print(path)

faceCascade = cv2.CascadeClassifier(face_cascade_Path)

font = cv2.FONT_HERSHEY_SIMPLEX


id = 0

i=656


# names related to ids: The names associated to the ids: 1 for Mohamed, 2 for Jack, etc...
names = [ '22929','22927','22922', '22962'] # add a name into this list
#Video Capture



    

while True :

    time.sleep(5)
    def write_file(data, filename):
    
        with open(filename, 'wb') as file:
            file.write(data)
            
            
            
    def readBLOB(id,imge):
        print("Reading BLOB data from notification table")
       

        try:
            sql_fetch_blob_query = """SELECT * from 2ndnotification where id = %s"""
        
            cursor.execute(sql_fetch_blob_query, (id,))
        
            record = cursor.fetchall()
            for row in record:
                global image
                global status
                status=row[10]
                id=row[0]
                print(id)
                image = row[12]
                
            
                print("Storing notificatio image and bio-data on disk \n")
                write_file(image, imge)
            

    

        finally:
            if db.connect():
                print("MySQL connection is closed")       
            
            
            
    readBLOB(i, "C:/xampp/htdocs/RealTimeFaceMaskMonitoringNew/admin_panel/CV-Mask-detection-master/CV-Mask-detection-master/2nd/"+'.'+str(i)+".jpg")
    
    cc=base64.b64decode(image)
    img = Image.open("C:/xampp/htdocs/RealTimeFaceMaskMonitoringNew/admin_panel/CV-Mask-detection-master/CV-Mask-detection-master/2nd/"+'.'+str(i)+".jpg")
    numpydata = asarray(img)
    cc=numpydata          
    gray = cv2.cvtColor(cc, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
             )
    print(faces)
    if status == "0" :
        mydb = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        db="facemask"
              )
        idd=i

        mycursor = mydb.cursor()

        sql = "UPDATE 2ndnotification SET status = '1' where id='idd'"
        mycursor.execute("""UPDATE 2ndnotification SET status = %s Where id = %s""",(1, idd))
        mycursor.execute(sql)

        mydb.commit()
        
        
        
        
        for (x, y, w, h) in faces:
            cv2.rectangle(cc, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        
            if (confidence >45 and confidence < 100) :
                id= names[id]
                count=0
                s='i'
                images=cv2.imwrite(str(path)+ '.'+str(i)+ '.jpg',cc)
            

                def convertToBinaryData(images):
   
                    with open(images, 'rb') as images:
                        binaryData = images.read()
                    return binaryData
                def insertBLOB(images):
                    print("Inserting BLOB ")
                
                    try:
                        sql ="INSERT INTO notification(studentid ,value,confidence,img)VALUES(%s,%s,%s,%s)"
                        empPicture = convertToBinaryData(images)
                        cursor.execute(sql,(id,'.'+ str(i)+ '.jpg',confidence,empPicture));
                        db.commit()
                        print("Image inserted successfully as a BLOB into table")
                    finally:
                        if db.connect():
                            cursor.close()
                            db.close()
                            print("MySQL connection is closed")
                insertBLOB( path+'.'+str(i)+".jpg")

                confidence = "  {0}%".format(round(100 - confidence))
            
            else:
           
            # Unknown Face
                id = "Unknown Person  ?"
                print(id)
                images=cv2.imwrite(str(path)+ '.'+str(i)+ '.jpg',cc)
                def convertToBinaryData(images):
   
                    with open(images, 'rb') as images:
                        binaryData = images.read()
                    return binaryData
                def insertBLOB(images):
                    print("Inserting BLOB ")
                    try:
                        sql ="INSERT INTO notification(studentid ,value,confidence,img)VALUES(%s,%s,%s,%s)"
                        empPicture = convertToBinaryData(images)
                    
                        cursor.execute(sql,(id,'.'+ str(i)+ '.jpg',confidence,empPicture));
                        db.commit()
                        print("Image and file inserted successfully as a BLOB into python_employee table")
                    finally:
                        if db.connect():
                            cursor.close()
                            db.close()
                            print("MySQL connection is closed")
                insertBLOB( path +'.'+str(i)+".jpg")
                confidence = "  {0}%".format(round(100 - confidence))
    i+=1
       
        
    

    
   
    
    # Escape to exit the webcam / program
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
print("\n [INFO] Exiting Program.")
cam.release()
cv2.destroyAllWindows()