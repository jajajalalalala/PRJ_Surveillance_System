# Raspberrypi Multi-Camera Surveillance system
Allows you to start a surveillance system using 3 Raspberry Pis.

Previously set Up:</br>
- You need have three Raspberry Pis 3B attached with the camera module. 
- The Raspberry pis and server always need to running under the same local network.
- Create a telegram bot  ==> [this link](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0)
- Collect the telegram bot chat id ==> [this link](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)


## Dependencies 
You will need to download the package requirement on both Raspbery Pi and local server to set up correct enviroument</br>

It is recommonded to run it within a independent environment for both client and server, [python virtual enviroument](https://docs.python.org/3/tutorial/venv.html) can be used to do so
```mkvirtualenv surveillance_server```

- On server side run</br>
```sudo pip3 install -r dependencies/server_requirements.txt```

- Copy the `dependencies/client_requirements.txt` file to each client, and run</br>
```sudo pip3 install -r client_requirements.txt```



## Client Setup:

- Send one of the `camera_client_x.py` and the corresponding `client_x.sh` to each Rasperry Pi. Rename the `client_x.sh` to `client.sh`.
- change the ip address in `camera_client_x.py` to the server ip address.
```sender = imagezmq.ImageSender(connect_to='tcp://<server_ip_address>:5554')```


## Server Setup:


- Set the client ip address in `app.py`.
```
client_list = [Client("<Client_1_IP>"), Client("<Client2_IP>"), Client("<Client_3_IP>")]
```

- Set the client ip address in `client_init.py` and `base_camera.py`.
```
switcher = {
            "cam1": "<Client_1_IP>",
            "cam2": "<Client_2_IP>",
            "cam3": "<Client_3_IP>"

        }
```

- Configure the remote directory of `client.sh` in the `start` method in `client_init.py`.

```
client.exec_command('/<remote_directory>/client.sh')
```
- Configure the telegram bot token and chat id in `notifier.py`.
```
token = '1546815383:AAGf-drVoek0FmaGsOtFHkZT0-3li6ojHRc'
chat_id = '-556671391'
```

## Usage 
```python3 app.py```

## Futher Modification
You can to change the motion detection algorithm by specify the algorithm in `camera_server.py`.
