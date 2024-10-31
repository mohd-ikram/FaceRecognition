import cv2 as cv
import face_recognition
import numpy as np
import os
from attendance import mark_attendance
import threading
import socket



PATH = "./"
resource_img_list = []
person_name_list = []
encoding_list = []
"""
Returns list of face encodings in image_list
"""
def all_face_encodings(img_list):
  for index, image in enumerate(img_list):
    # cv2_imshow(image)
    face_encoding_list = face_recognition.face_encodings(image)
    if len(face_encoding_list)==0:
       img_name = person_name_list[index]
       print("No face found for image: ${}".format(img_name))
       continue
    encoding = face_encoding_list[0]
    encoding_list.append(encoding)
  return encoding_list


"""
read_images_resources function reads images file from resource 
and store in list resource_img_list
Corresponding names in person_name_list
"""
def read_images_resources():
  image_files = os.listdir(f"{PATH}/resources/")
  # print(image_files)
  for img_file in image_files:
    resource_img_list.append(cv.imread(f"{PATH}/resources/{img_file}"))
    person_name_list.append(img_file.split(".")[0])
  # print(resource_img_list)

read_images_resources()
all_face_encodings(resource_img_list)

"""
funtion read_camera_faces reads the faces from camera stream
compare the faces with the existing faces in resource directory
Record the checkin/checkout time in excel sheet
is_checkin indicates that camera open for checkin/checkout
"""
def read_camera_faces(is_checkin=True):
  cap = cv.VideoCapture(0)
  # url = 'http://192.168.1.54/8080/video'
  
  
  # ip= "192.168.1.46"
  # url = 'rtmp://{}:8000/stream'.format(ip)
  # url = 'http://{}:8000/video'.format(ip)
  # cap = cv.VideoCapture(url)

  while True:
      success, img = cap.read()
      # print("IP VALID", is_valid_ip(ip))
      if not success:
          break
      # Convert frame to MJPEG format (adjust as needed)
      if cv.waitKey(1) & 0xFF == ord('q'):
        break
      
      # Find the location of faces on image of video stream
      test_faces_location = face_recognition.face_locations(img)
      # encoded test faces on given location in img
      test_encoded = face_recognition.face_encodings(img,test_faces_location)

      # Getting face encoding and location of face in side image one by one
      for encoded_face, location in zip(test_encoded, test_faces_location):
            # Conpare the steam face encoding with the face encoding list of resource directory, 
            # Returns list with True/False values indicating which encoding_list match the face encoding to check 
            matches = face_recognition.compare_faces(encoding_list,encoded_face)
            # A numpy ndarray with the distance for each face in the same order as the ‘faces’ array
            face_distances = face_recognition.face_distance(encoding_list,encoded_face)
            # print(face_distances)

            # Get the minimum value index from the ndarray using numpy
            match_index = np.argmin(face_distances)
            if matches[match_index] & (np.min(face_distances)<.5):
                name = person_name_list[match_index]
                y1,x2,y2,x1 = location
                cv.rectangle(img,(x1,y1),(x2,y2),(255,0,0),3)
                cv.putText(img,name,(x1+8,y2-6),cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 3)
                mark_attendance_thread = threading.Thread(target=mark_attendance, args = (name,is_checkin))
                mark_attendance_thread.start()
      # img = thread_exec_process_image(process_image,img)
      cv.imshow("Image",img)
      # Set the JPEG quality (1-100, lower means higher compression)
      # quality = 80

      # Encode parameters for saving with JPEG compression
      # encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
      # success, buffer = cv.imencode('.jpg', img,encode_param)
      # frame = buffer.tobytes()
      # yield (b'--frame\r\n'
              #  b'Content-Type: image/*\r\n\r\n' + frame + b'\r\n')

  cap.release()
  cv.waitKey(10)
  cv.destroyAllWindows()

# Function to validate IP address
def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
def process_image(img):
      # Find the location of faces on image of video stream
      test_faces_location = face_recognition.face_locations(img)
      # encoded test faces on given location in img
      test_encoded = face_recognition.face_encodings(img,test_faces_location)

      # Getting face encoding and location of face in side image one by one
      for encoded_face, location in zip(test_encoded, test_faces_location):
            # Conpare the steam face encoding with the face encoding list of resource directory, 
            # Returns list with True/False values indicating which encoding_list match the face encoding to check 
            matches = face_recognition.compare_faces(encoding_list,encoded_face)
            # A numpy ndarray with the distance for each face in the same order as the ‘faces’ array
            face_distances = face_recognition.face_distance(encoding_list,encoded_face)
            # print(face_distances)

            # Get the minimum value index from the ndarray using numpy
            match_index = np.argmin(face_distances)
            if matches[match_index] & (np.min(face_distances)<.5):
                name = person_name_list[match_index]
                y1,x2,y2,x1 = location
                cv.rectangle(img,(x1,y1),(x2,y2),(255,0,0),3)
                cv.putText(img,name,(x1+8,y2-6),cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 3)
                mark_attendance_thread = threading.Thread(target=mark_attendance, args = (name,is_checkin))
                mark_attendance_thread.start()
      return img
def thread_exec_process_image(func,img):
    result = None
    def run():
      nonlocal result
      result = func(img)
    thread = threading.Thread(target=run)
    thread.start()
    thread.join()
    return result
# read_camera_faces(True)