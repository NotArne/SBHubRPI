# SBHubRPI
## Functionality:
This simple program reads the ble advertisements of the SwitchBot SmartMeter and sends them via mqtt to any mqtt broker.
The program should run on a wide range of Linux-based systems as well as should be compatible to any mqtt broker and can so integrated in many home-automation softwares.
I have tested it using a Raspberry Pi 3 and ioBroker`s Mqtt broker.

## Supported Devices:
Only the Smart Meter by SwitchBot is supported by now, because I only can test with this device, yet. 
## Run:
The project needs the python packages bluepy and paho-mqtt as external dependencies.
On a debian based systems you need the packages:
```
$ sudo apt-get install python-pip libglib2.0-dev
```
Then run: 
```
$ sudo pip install bluepy paho-mqtt
```
Unfortunately BLE scan needs root permissions, so you can run the program by:
```
sudo python3 app.py [pathToConfigFile]
```

## Configuration:
The program needs a configuration Json-file like the following in order to work.
```
{
  "brokerIP": "192.168.178.5",
  "brokerPort": 1883,
  "hubName": "RPI_HUB1",
  "brokerUsername": "test",
  "brokerPassword": "123456",
  "scanForSeconds": 10.0,
  "rescanTime": 60,
  "publishOnlyChanges": true,
  "devices": [
    {
      "bleMacAddress": "de:ea:db:ee:f1:23",
      "deviceDescription": "LivingRoom",
      "deviceType": "SB_Meter"
    }
  ]
}
```

### Parameter Explanation:
- ```scanForSeconds```: Specifies the amount of seconds a ble active scan will be performed. This should not be to large and not to small.
- ```rescanTime```: Specifies the amount of seconds which will be waited between different ble active scan runs.
- ```deviceDescription```: Description of the device, can be set free but should be unique. Resulting values of the device will be pushed to ```deviceDescription/variable```
- ```deviceType```: Must be "SB_Meter" by now, because now only the Smart Meter is supported. This might change in future.
- ```publishOnlyChanges```: If this parameter is set true, than only if a change is detected, the data will be published to the broker. If set to false, updates occur after every ble scan operation.

## Restrictions/Hints:
- ````sudo```` permissions are required to scan for ble devices
- The temperature which will be sent is always in celsius!
- If you get an python ````KeyError````, please check the json config file. All parameters must be set!
