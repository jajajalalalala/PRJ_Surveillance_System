import paramiko
import csv
import time
#Class to start a server
class Client:
    password = 'pi'
    username = 'pi'
    hostname = ''


    def __init__(self, host):
        self.hostname = host

    def get_cam_ip(self, cam_name):
        switcher = {
            "cam1": "192.168.0.172",
            "cam2": "192.168.0.145",
            "cam3": "192.168.0.144"

        }
        return switcher.get(cam_name, "Invalid")

    #id specify the
    def start(self):
        print ("start client")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)
        # bash_script = open('resource/client_{}.sh'.format(id)).read()
        #
        # stdin, stdout, stderr = client.exec_command(bash_script)

        client.exec_command('/home/pi/PRJ/Client/client.sh')


        # close the connection
        client.close()

    #restart the client
    def restart(self):
        print("restart client")
        self.stop()
        self.start()

    def stop(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)
        print ("stop client")

        #Host name on 192.168.0.172 is running on python 3
        if(self.hostname == '192.168.0.172'):
            stdin, stdout, stderr = client.exec_command('pgrep -o -x python3')
        else:
            stdin, stdout, stderr = client.exec_command('pgrep -o -x python')
        pid = stdout.read().decode("utf-8")
        stdin, stdout, stderr = client.exec_command('kill ' + format(pid))

        # print errors if there are any
        err = stderr.read().decode()
        if err:
            print(err)
            # close the connection
        stdin.close()


