import cv2
import gi
import datetime

from threading import Thread

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")

from gi.repository import Gst, GstApp, GLib

_ = GstApp

Gst.init()

main_loop = GLib.MainLoop()
main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

pipeline = Gst.parse_launch("rtmpsrc location=rtmp://192.168.10.126/live/password ! decodebin ! appsink name=sink")
appsink = pipeline.get_by_name("sink")

pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        sample = appsink.try_pull_sample(Gst.SECOND)
        if sample is None:
            continue

        # print("I got a sample!")
        buffer = sample.gst_sample_get_buffer()
        cv2.imwrite("build/image" + str(datetime.datetime.now()) + ".png", sample)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()