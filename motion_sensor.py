import cv2
import os
from email_sending import send_email
import time
import glob
from datetime import datetime
from threading import Thread

def del_images():
    images_all = glob.glob("images/*.png")
    for image in images_all:
        os.remove(image)

video = cv2.VideoCapture(0)
first_frame = None
time.sleep(1)
count = 1
status_list = []

while True:
    day_time = datetime.now()
    current_time = day_time.strftime("%H:%M:%S")
    current_day = day_time.strftime("%A")
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = blur_frame

    diff_frame = cv2.absdiff(first_frame, blur_frame)
    thresh_frame = cv2.threshold(diff_frame, 40, 255, cv2.THRESH_BINARY)[1]
    dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, hierarchy = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 6000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_image = glob.glob(f"images/*.png")
            index  = int(len(all_image) / 2)
            image_path = all_image[index]

    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_path, ))
        email_thread.start()
        clean_thread = Thread(target=del_images)
        print("email sent")

    cv2.putText(img=frame, text=current_day, org=(50, 50),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0),
                thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(img=frame, text=current_time, org=(50, 100),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0),
                thickness=2, lineType=cv2.LINE_AA)

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
clean_thread.start()
print("images deleted")