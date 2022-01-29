import mysql.connector

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBLOB(id,imge):
    print("Reading BLOB data from notification table")

    try:
        

        
        sql_fetch_blob_query = """SELECT * from notification where id = %s"""
        
        cursor.execute(sql_fetch_blob_query, (id,))
        print(imge)
        record = cursor.fetchall()
        for row in record:
            global image
            id=row[0]
            image = row[12]
            print(image)
            print("Storing notificatio image and bio-data on disk \n")
            write_file(image, imge)
            

    

    finally:
        if db.connect():
            cursor.close()
            db.close()
            print("MySQL connection is closed")


readBLOB(334,"C:/Users/Home/Desktop/Real-Time-Face-Recognition-master/2nd/image.jpg")
