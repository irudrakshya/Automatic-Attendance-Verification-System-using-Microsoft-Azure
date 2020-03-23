import os
import cv2
from time import sleep
from PIL import Image, ImageDraw, ImageFont
from person import Person
from face import Face
from attendance import Attendance
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']


try:
    # Create an authenticated FaceClient.
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    # name should be in lowercase
    # PERSON_GROUP_ID = input("Enter a Person Group Name: ")
    PERSON_GROUP_ID = 'mca'
    p = Person(PERSON_GROUP_ID,face_client)
    # print(p.createPersonGroup())
    names = p.createPerson()
    p.addFaces(names)
    p.trainPerson()

    f = Face(PERSON_GROUP_ID,face_client)

    filename = r'C:\Users\Rudrakshya\Desktop\Internship\Attendance.csv'
    header = ('Names', 'Attendance')
    data = [('Abhishek', 0),
            ('Abinash', 0),
            ('Amar', 0),
            ('Aparna', 0),
            ('Bikash', 0),
            ('Birendra', 0),
            ('Deepak', 0),
            ('Donally', 0),
            ('Ebadat', 0),
            ('Hafiz', 0),
            ('Hanu', 0),
            ('Prakash', 0),
            ('Priyadarshinee', 0),
            ('Priyatosh', 0),
            ('Rudrakshya', 0),
            ('Sachin', 0),
            ('Samir', 0),
            ('Siddharth', 0),
            ('Subhankar', 0),
            ('Taquiuddin', 0),
            ('Uday', 0)
            ]

    at = Attendance()
    at.writer(header, data, filename, 'write')
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    sleep(2)
    print("Camera opening...")
    print("\nPress S to capture and Q to quit")
    while True:

        try:
            check, frame = webcam.read()

            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd

            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):

                cv2.imwrite(filename='saved_img.jpg', img=frame)

                # webcam.release()
                print("Processing image...")
                img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)

                img_ = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
                temp_add = r"C:\Users\Rudrakshya\Desktop\Internship\test.jpg"
                cv2.imwrite(temp_add, img_)
                print()
                faces, face_ids = f.detectFaces(temp_add)
                person_Ids = f.identifyFaces(KEY, face_ids)
                person_identified = f.getPersonName(KEY, person_Ids)
                at.updater(filename, person_identified)
                print("\nAttendance taken successfully!")
                font = ImageFont.truetype("arial.ttf", 20)
                print()
                img = Image.fromarray(img_)
                draw = ImageDraw.Draw(img)
                for face, name in zip(faces, person_identified):
                    x = f.getRectangle(face)
                    draw.rectangle(f.getRectangle(face), outline='white')
                    draw.text((x[0][0], x[0][1] - 20), name, (255, 255, 255), font=font)
                img.show()


            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

    # Attendance



except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


