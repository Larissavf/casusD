from ultralytics import YOLO
import os

mypath = "C:/Users/btnap/Documents/School/Thema_10"
os.chdir(mypath)

model = YOLO(f'{mypath}/runs/detect/train2/weights/best.pt')
img = f'{mypath}/complete_images/9075.jpeg'

model.predict(img, save=True)