# Automatic Attendance Verification System

This project marks attendances of employees or students automatically by recognizing faces. It is developed using Python language and uses Microsoft Cognitive Services for recognizing faces.

## Requirements

A subscription for [Face API](https://azure.microsoft.com/en-in/services/cognitive-services/)

### Install following packages

```bash
azure
json
glob
pil
csv
```
### Install client library
```python
pip install --upgrade azure-cognitiveservices-vision-face
```

## Steps to run

1. Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
2. Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
3. Create Images folder in root directory containing images of faces
4. Run faceRecognition.py



## License
[MIT](https://choosealicense.com/licenses/mit/)
