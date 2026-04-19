import cv2
import time
import glob
from Emailing import send_email

video = cv2.VideoCapture(0)
time.sleep(2)

 #Descarta los primeros 30 frames para estabilizar la cámara
for i in range(30):
    video.read()

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    check, frame = video.read()

    if not check:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau.astype("float")
        continue

    # Actualiza el fondo poco a poco — detecta solo objetos QUE ESTAN SOLO EN MOVIMIENTO
    cv2.accumulateWeighted(gray_frame_gau, first_frame, 0.02)
    background = cv2.convertScaleAbs(first_frame)

    delta_frame = cv2.absdiff(background, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=5)

    contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    frame_area = frame.shape[0] * frame.shape[1]

    # Filtra contornos válidos (ni muy pequeños ni muy grandes)
    valid_contours = [
        c for c in contours
        if 3000 < cv2.contourArea(c) < frame_area * 0.5
    ]

    if valid_contours:
        # Toma solo el contorno MÁS GRANDE en movimiento
        biggest = max(valid_contours, key=cv2.contourArea)
        status = 1
        (x, y, w, h) = cv2.boundingRect(biggest)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.imwrite(f"imagenes/{count}.png", frame)
        count += 1
        all_images= glob.glob("imagenes/*.png")
        index = int(len(all_images) / 2)
        iobject = all_images[index]
    else:
        status = 0

    status_list.append(status)
    status_list = status_list[-2:]

    if len(status_list) == 2 and status_list[-1] == 1 and status_list[0] == 0:
        send_email()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    if key == ord("r"):
        first_frame = gray_frame_gau.astype("float")
        print("Frame base reseteado!")

video.release()
cv2.destroyAllWindows()