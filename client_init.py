import paramiko
from datetime import  datetime
#

class Client:
    password = 'pi'
    username = 'pi'
    hostname = ''


    def __init__(self, host):
        self.hostname = host
        self.start_time = 0

    # Get the Ip of Camera
    def get_cam_ip(self, cam_name):
        switcher = {
            "cam1": "192.168.0.172",
            "cam2": "192.168.0.145",
            "cam3": "192.168.0.144"

        }
        return switcher.get(cam_name, "Invalid")

    #Start the client by execute an bash file
    def start(self):
        print ("start client")
        self.start_time = datetime.now()
        print(self.start_time)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)
        # The  directory of the  bash file is located under the directory of the raspberry pi
        client.exec_command('/home/pi/PRJ/Client/client.sh')
        # close the connection
        client.close()



    # Stop an camera by killing the python process.

    def stop(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)
        print ("stop client")

        # Grep the pid of python3 task running on the raspberry Pi

        stdin, stdout, stderr = client.exec_command('pgrep -o -x python3')
        # Collect the PID and kill it
        pid = stdout.read().decode("utf-8")
        stdin, stdout, stderr = client.exec_command('kill ' + format(pid))

        # print errors if there are any
        err = stderr.read().decode()
        if err:
            print(err)
            # close the connection
        stdin.close()

    #restart the client by firstly stop the raspberry Pi and restart it.
    def restart(self):
        print("restart client")
        self.stop()
        self.start()


