import time
import threading
import imagezmq
import notifier
from client_init import Client
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent:
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera:
    threads = {}  # background thread that reads frames from camera
    frame = {}  # current frame is stored here by background thread
    last_access = {}  # time of last client access to the camera
    first_frame = None
    event = {}

    def __init__(self, device, port_list):
        """Start the background camera thread if it isn't running yet."""
        BaseCamera.event[device] = CameraEvent()

        if device not in BaseCamera.threads:
            BaseCamera.threads[device] = None
        if BaseCamera.threads[device] is None:
            BaseCamera.last_access[device] = time.time()

            # start background frame thread
            BaseCamera.threads[device] = threading.Thread(target=self._thread,
                                                                    args=(device, port_list))
            BaseCamera.threads[device].start()

            # wait until frames are available
            while self.get_frame(device) is None:
                time.sleep(0)


    @classmethod
    def get_frame(cls, device):
        """Return the current camera frame."""
        BaseCamera.last_access[device] = time.time()

        # wait for a signal from the camera thread
        BaseCamera.event[device].wait()
        BaseCamera.event[device].clear()
        return BaseCamera.frame[device]


    @classmethod
    def server_thread(cls, device, port):

        image_hub = imagezmq.ImageHub(open_port='tcp://*:{}'.format(port))

        frames_iterator = cls.server_frames(image_hub)

        switcher = {
            "cam1": "192.168.0.172",
            "cam2": "192.168.0.145",
            "cam3": "192.168.0.144"

        }

        try:
            for cam_id, frame in frames_iterator:
                #set the current frame
                BaseCamera.frame[device] = cam_id, frame
                BaseCamera.event[device].set()  # send signal to clients
                time.sleep(0)

                #If we don't get frame for 10 seconds, then close the connection
                if time.time() - BaseCamera.last_access[device] > 10:
                    ip = switcher.get(cam_id, "Invalid IP")

                    frames_iterator.close()
                    image_hub.zmq_socket.close()
                    print('Closing server socket at port {}.'.format(port))

                    notifier.telegram_bot_sendText("Camera {} is down, please check the camera.".format(cam_id))
                    #When Camera is invalid, restart the camera
                    client = Client(ip)
                    client.restart()
                    # Notify the user restart the camera
                    notifier.telegram_bot_sendText("Camera {} has restarted.".format(cam_id))
                    print('Restarting server thread for device {} due to inactivity.'.format(device))
                    pass
        except Exception as e:

            frames_iterator.close()
            image_hub.zmq_socket.close()
            notifier.telegram_bot_sendText("Camera is down, please check the camera ")

            notifier.telegram_bot_sendText("Camera has started.")
            print('Closing server socket at port {}.'.format(port))
            print('Stopping server thread for device {} due to error.'.format(device))
            print(e)

    @classmethod
    #A class method indicates a thread
    def _thread(cls, device, port_list):
        port = port_list[int(device)]
        print('Starting server thread for device {} at port {}.'.format(device, port))
        cls.server_thread(device, port)


        BaseCamera.threads[device] = None