import cv2
import datetime

from threading import Thread
from gi.repository import GLib

# print(cv2.version)

main_loop = GLib.MainLoop()
main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

video = cv2.VideoCapture('rtmp://192.168.10.126/live/password')

try:
    while True:
        ret,frame = video.read()
        if frame is None:
            break

        # save image
        cv2.imwrite("build/image" + str(str(datetime.datetime.now())) + ".png", frame)

except KeyboardInterrupt:
    pass

main_loop.quit()
main_loop_thread.join()