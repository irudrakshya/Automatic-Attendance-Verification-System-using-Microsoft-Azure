import glob
import time
import os
import sys
from azure.cognitiveservices.vision.face.models import TrainingStatusType


class Person:

    def __init__(self,PERSON_GROUP_ID,face_client):
        self.PERSON_GROUP_ID = PERSON_GROUP_ID
        self.face_client = face_client

    def createPersonGroup(self):
        self.face_client.person_group.create(person_group_id=self.PERSON_GROUP_ID, name=self.PERSON_GROUP_ID)
        return 'Person Group created'

    def createPerson(self):
        no_of_persons = int(input("How many person you want to create?\n"))
        names = {}

        for _ in range(no_of_persons):
            names[input("Person {}: ".format(_+1))] = 0

        for key in names:
            names[key] = self.face_client.person_group_person.create(self.PERSON_GROUP_ID, key)

        print("{} Persons created successfully.\n".format(no_of_persons))

        return names

    def addFaces(self,names):
        print("")
        loc = os.path.join(r'C:\Users\Rudrakshya\Desktop\PythonAzure\Images')
        for key in names.keys():
            images = [file for file in glob.glob(loc+'\\'+'*.jpg') if file.startswith(loc+'\\'+key)]

            for image in images:
                img = open(image, 'r+b')
                self.face_client.person_group_person.add_face_from_stream(self.PERSON_GROUP_ID, names[key].person_id, img)
                print("{} uploaded for {}.".format(image, key))

    def trainPerson(self):
        self.face_client.person_group.train(self.PERSON_GROUP_ID)

        while True:
            training_status = self.face_client.person_group.get_training_status(self.PERSON_GROUP_ID)
            print("\nTraining status: {}.".format(training_status.status))
            print()
            if training_status.status is TrainingStatusType.succeeded:
                break
            elif training_status.status is TrainingStatusType.failed:
                sys.exit('Training the person group has failed.')
            time.sleep(5)

