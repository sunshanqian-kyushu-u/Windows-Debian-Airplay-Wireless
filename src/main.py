import threading
from time import sleep
import cv2
import datetime
from queue import Queue

frame_read_flag = False
frame_process_flag = False
frame_finished_flag = False
frame_get_flag = False
link_flag = False
link_result_flag = False

def frame_process(var):
    global frame_finished_flag
    global frame_process_flag
    global frame_get_flag
    
    frame_finished_flag = True
    sleep(1) # wait var get the first frame
    print("frame process start!")

    while frame_process_flag:
        if frame_get_flag:
            frame_get_flag = False

            # test
            print("start process.")
            cv2.imwrite("build/image" + str(datetime.datetime.now()) + ".png", var.get())
            sleep(5)
            print("process finished.")

            # image process


            frame_finished_flag = True
        else:
            sleep(0.1)

def frame_read(var):
    global frame_process_flag
    global frame_get_flag
    global frame_read_flag
    global frame_finished_flag
    global link_flag
    global link_result_flag

    cap = cv2.VideoCapture("rtmp://192.168.10.126/live/password")
    if(cap.isOpened()):
        link_result_flag = True
        link_flag = True
        print("link to stream successfully!")

        # start frame_process_thread
        frame_process_thread = threading.Thread(target=frame_process, args=(var,))
        frame_process_flag = True
        frame_process_thread.start()

        while frame_read_flag:
            ret,frame = cap.read()

            if frame_finished_flag:
                frame_finished_flag = False
                var.put(frame)
                frame_get_flag = True

        frame_process_flag = False
        frame_process_thread.join()
        cap.release()
    else:
        cap.release()
        link_result_flag = False # as it defined
        link_flag = True
        print("can not link to the stream. please try again.")

def main():
    # print(threading.active_count())
    # print(threading.enumerate())
    # print(threading.current_thread())

    var = Queue()
    global frame_process_flag
    global frame_get_flag
    global frame_read_flag
    global frame_finished_flag
    global link_flag
    global link_result_flag

    frame_read_thread = threading.Thread(target=frame_read, args=(var,))
    frame_read_flag = True
    frame_read_thread.start()

    while True:
        if not link_flag:
            # do nothing
            sleep(0.1)
        else:
            if link_result_flag:
                # link succeed
                break
            else:
                # link failed and exit directly
                exit(1)

    # wait for keyboard input to exit
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass

    frame_read_flag = False
    frame_read_thread.join() # wait frame_read_thread stopped

if __name__ == '__main__':
    main()
