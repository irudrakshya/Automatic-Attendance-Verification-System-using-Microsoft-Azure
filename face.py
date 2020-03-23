import os
import glob
import json
import requests
from urllib.parse import urlparse
import http.client, urllib.request, urllib.parse, urllib.error, base64


class Face:

    def __init__(self, PERSON_GROUP_ID,face_client):
        self.PERSON_GROUP_ID = PERSON_GROUP_ID
        self.face_client = face_client

    def detectFaces(self, group_photo_name):

        # images_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        # test_image_array = glob.glob(os.path.join(images_folder, group_photo_name))
        # image = open(test_image_array[0], 'r+b')

        image = open(group_photo_name, 'r+b')

        # Detect faces
        face_ids = []
        faces = self.face_client.face.detect_with_stream(image)

        for face in faces:
            face_ids.append(face.face_id)
        print("{} faces detected.".format(len(face_ids)))

        return faces, face_ids

    def getRectangle(self,faceDictionary):
        rect = faceDictionary.face_rectangle
        left = rect.left
        top = rect.top
        right = left + rect.width
        bottom = top + rect.height

        return ((left, top), (right, bottom))

    def identifyFaces(self, KEY, face_ids):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': KEY,
        }

        params = urllib.parse.urlencode({'personId': 'true'
                                                 })

        body = {
            "personGroupId": self.PERSON_GROUP_ID,
            "faceIds": face_ids,
            "confidenceThreshold": 0.5
        }

        try:
            conn = http.client.HTTPSConnection("internshipproject.cognitiveservices.azure.com")
            conn.request("POST", "/face/v1.0/identify?%s" % params,
                         body=json.dumps(body),
                         headers=headers)
            response = conn.getresponse()
            data = json.loads(response.read().decode('UTF-8'))
            person_Ids = []
            for i in data:
                if i['candidates']!=[]:
                    person_Ids.append(((i['candidates'])[0])['personId'])
            conn.close()

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        return person_Ids

    def getPersonName(self,KEY,person_Ids):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': KEY,
        }
        person_identified = []
        for p_id in person_Ids:
            params = urllib.parse.urlencode({'personGroupId': self.PERSON_GROUP_ID,
                                             'personId': p_id
                                             })
            try:
                conn = http.client.HTTPSConnection("internshipproject.cognitiveservices.azure.com")
                conn.request("GET", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}?%s" % params, "{body}",
                             headers)
                response = conn.getresponse()
                data = json.loads((response.read()).decode('UTF-8'))
                name = data['name']
                person_identified.append(name)
                print("{} identified.".format(name))
                conn.close()
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return person_identified