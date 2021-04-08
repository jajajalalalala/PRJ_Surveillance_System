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



## Documentation 
- Receiving joystick input ==> [this link](https://www.pygame.org/docs/ref/joystick.html?highlight=joystick)
- Simulate keyboard input ==> [this link](https://pypi.org/project/pynput/)

## Usage 
```python  raspberry_gamepad_interface.py  ```

## Futher Modification
It is possible that you modify the behaviour of each joystick input by modifing the event handlder in the code 
```python 


def AxisEventHandler(self, axis, degree)
    #define your action 
    
def ArrowButtonEventHandler(self,button)
    #define your action 


```
