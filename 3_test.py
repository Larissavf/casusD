from ultralytics import YOLO
import os

mypath = "C:/Users/btnap/Documents/School/Thema_10"
os.chdir(mypath)

model = YOLO("yolov8n.pt")
model.train(data='dataset.yaml', epochs=20, single_cls=True)