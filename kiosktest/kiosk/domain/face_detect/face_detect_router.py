import sys
sys.path.append(r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk')
import os
import cv2
import numpy as np

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from collections import Counter
from models import FaceAnalysis  # FaceAnalysis 모델을 가져옴

FILE_DIR = r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk\domain\face_detect'

face_classifier = cv2.CascadeClassifier(os.path.join(FILE_DIR, 'haarcascade_frontalface_default.xml'))
emotion_model = load_model(os.path.join(FILE_DIR, 'emotion_detection_model.h5'))  # 오타 수정
age_model = load_model(os.path.join(FILE_DIR, 'age.h5'))
gender_model = load_model(os.path.join(FILE_DIR, 'gender.h5'))

router = APIRouter()

class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
gender_labels = ['Male', 'Female']




@router.post("/analyze_video", tags=["고객 정보"])
async def 고객정보등록(file: UploadFile = File(...), customer_name: Optional[str] = None, db: Session = Depends(get_db)):
    temp_file = os.path.join(FILE_DIR, "temp_video.mp4")
    
    with open(temp_file, "wb") as buffer:
        buffer.write(file.file.read())

    video = cv2.VideoCapture(temp_file)
    emotions = []
    genders = []
    ages = []
    
    while True:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_model.predict(roi)[0]
            emotions.append(class_labels[preds.argmax()])

            roi_color = frame[y:y+h, x:x+w]
            roi_color = cv2.resize(roi_color, (200, 200), interpolation=cv2.INTER_AREA)

            gender_predict = gender_model.predict(np.array(roi_color).reshape(-1, 200, 200, 3))
            genders.append(gender_labels[int(gender_predict > 0.5)])

            age_predict = age_model.predict(np.array(roi_color).reshape(-1, 200, 200, 3))
            ages.append(round(age_predict[0][0]))

    video.release()
    os.remove(temp_file)

    most_common_emotion = Counter(emotions).most_common(1)[0][0]
    most_common_gender = Counter(genders).most_common(1)[0][0]
    median_age = sorted(ages)[len(ages)//2]

    face_analysis = FaceAnalysis(
        name=customer_name,
        emotion=most_common_emotion,
        gender=most_common_gender,
        age=median_age
    )
    
    db.add(face_analysis)
    db.commit()
    db.refresh(face_analysis)

    return {
        "customer_name": customer_name,
        "emotion": most_common_emotion, 
        "gender": most_common_gender, 
        "age": median_age
    }

