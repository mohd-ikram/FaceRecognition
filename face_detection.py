import cv2 as cv
import os
# from google.colab.patches import cv2_imshow
from matplotlib import pyplot as plt
import face_recognition
import numpy as np

resource_img_list = []
person_name_list = []
PATH = "./"
"""
bill_gates = cv.imread("./resources/Bill_Gates.jpg")
elon_musk = cv.imread("./resources/Elon_Musk.jpg")
barack_obama = cv.imread("./resources/Barack_Obama.jpg")
sundar_pichai = cv.imread("./resources/Sundar_Pichai.jpg")

bg_face_location = face_recognition.face_locations(bill_gates)[0]
em_face_location = face_recognition.face_locations(elon_musk)[0]
bo_face_location = face_recognition.face_locations(barack_obama)[0]
sp_face_location = face_recognition.face_locations(sundar_pichai)[0]

encodeBill = face_recognition.face_encodings(bill_gates)[0]
encodeMusk = face_recognition.face_encodings(elon_musk)[0]
encodeObama = face_recognition.face_encodings(barack_obama)[0]
encodePichai = face_recognition.face_encodings(sundar_pichai)[0]

"""

def all_face_encodings(img_list):
  encoding_list = []
  for image in img_list:
    # cv2_imshow(image)
    encoding = face_recognition.face_encodings(image)[0]
    encoding_list.append(encoding)
  return encoding_list

def read_images_resources():
  image_files = os.listdir(f"{PATH}/resources/")
  # print(image_files)
  for img_file in image_files:
    resource_img_list.append(cv.imread(f"{PATH}/resources/{img_file}"))
    person_name_list.append(img_file.split(".")[0])
  # print(resource_img_list)

def get_result(img_file):
  identified_person_name = ''
  face_encoding_list = all_face_encodings(resource_img_list)
  test_image = cv.imread(f"{PATH}/test_resources/{img_file}")
  # cv2_imshow(face_encoding_list)
  test_face_location = face_recognition.face_locations(test_image)
  test_image_encoding = face_recognition.face_encodings(test_image,test_face_location)
  for encode, location in zip(test_image_encoding,test_face_location):
    matches = face_recognition.compare_faces(face_encoding_list,test_image_encoding[0])
    face_distance = face_recognition.face_distance(face_encoding_list,test_image_encoding[0])
    # print(face_distance)
    match_index = np.argmin(face_distance)
    if matches[match_index]:
      identified_person_name = person_name_list[match_index]
  print(identified_person_name)

read_images_resources()
get_result("test_elon_musk3.jpg")