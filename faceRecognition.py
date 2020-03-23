import os
from PIL import Image, ImageDraw, ImageFont
from person import Person
from face import Face
from attendance import Attendance
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']


def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height

    return ((left, top), (right, bottom))

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
    test_img = input("Enter a group photo name with extension: ")

    print()
    faces, face_ids = f.detectFaces(test_img)

    # For each face returned use the face rectangle and draw a red box.

    person_Ids = f.identifyFaces(KEY, face_ids)
    person_identified = f.getPersonName(KEY, person_Ids)

    img = Image.open(r'C:\Users\Rudrakshya\Desktop\Internship' + '\\' + test_img)
    # img = img.rotate(180)
    font = ImageFont.truetype("arial.ttf", 20)
    print('Drawing rectangle around face... see popup for results.')
    draw = ImageDraw.Draw(img)
    for face, name in zip(faces,person_identified):
        x = f.getRectangle(face)
        draw.rectangle(f.getRectangle(face), outline='white')
        draw.text((x[0][0], x[0][1]-20), name, (255, 255, 255), font=font)
    img.show()

    # Attendance
    filename = r'C:\Users\Rudrakshya\Desktop\Internship\Attendance.csv'
    header = ('Names', 'Attendance')
    data = [('Abhishek', 0),
            ('Abinash', 0),
            ('Amar', 1),
            ('Aparna', 0),
            ('Bikash', 0),
            ('Birendra', 0),
            ('Deepak',0),
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
    at.writer(header, data, filename,'write')
    print(person_identified)
    at.updater(filename, person_identified)
    print("Attendance taken successfully!")

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


