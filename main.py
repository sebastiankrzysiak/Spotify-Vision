from spotifyvision import SpotifyVision
from ultralytics import YOLO
import cv2
import math
from time import sleep

sv = SpotifyVision()
cap = cv2.VideoCapture(0)
print("Camera is ready!\n")

model = YOLO("best.pt")
classNames = ["like", "pause_resume", "redo", "stop", "skip"]
stop = False

sv.select_playlist()

while True:

    success, img = cap.read()
    results = model(img, stream=True, verbose=False)

    for r in results:
        for box in r.boxes:
            action = classNames[int(box.cls[0])]
            confidence = math.ceil((box.conf[0]*100))/100

            print(f"Action: {action}, Confidence: {confidence}")

            status = sv.is_playing()

            if action == "pause_resume" and status == False and confidence > 0.65:
                print(sv.print_playing())
                sv.resume()
                sleep(2)

            elif action == "pause_resume" and status == True and confidence > 0.65:
                print(sv.print_paused())
                sv.pause()
                sleep(2)

            elif action == "skip" and confidence > 0.65:
                sv.next_song()
                print(sv.print_playing())
                sleep(2)

            elif action == "like" and confidence > 0.65:
                sv.like_song()
                print(sv.print_liked())
                sleep(2)

            elif action == "stop" and confidence > 0.65:
                if status == True:
                    sv.pause()
                print("Stopped")
                stop = True
            
    if stop == True:
        break

cap.release()
cv2.destroyAllWindows()