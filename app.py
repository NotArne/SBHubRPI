from ble.BleScanner import BLEScanner
from devices.DeviceDescription import DeviceDescription, DeviceType
from mqtt.MqttClient import MqttClient
import json, sys, logging, sched, time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR) # Set to info for more information

    # Read json config
    if len(sys.argv) != 2:
        sys.exit("You must supply exactly one config file!")
    try:
        jsonConfigFile = open(sys.argv[1], "r")
    except:
        sys.exit(f'Error: Cannot read the filename: {sys.argv[1]}')
    jsonConfigText = jsonConfigFile.read()

    jsonConfig = json.loads(jsonConfigText)

    # Interpret supplied devices, create indices
    bleMacToDevice = {}
    idToDevice = {}
    for i in range(0, len(jsonConfig["devices"])):
        dev = jsonConfig["devices"][i]
        if dev["deviceType"] == "SB_Meter":
            deviceType = DeviceType.SB_METER
        else:
            sys.exit(f'Found unsupported deviceType {dev["deviceType"]}!')
        d= DeviceDescription(i,dev["bleMacAddress"].lower(),dev["deviceDescription"],deviceType)
        bleMacToDevice[dev["bleMacAddress"].lower()] = d
        idToDevice[i] = d

    # Initialize ble and mqqt module
    mqttClient = MqttClient(jsonConfig["brokerIP"].lower(), int(jsonConfig["brokerPort"]), jsonConfig["hubName"],
                            jsonConfig["brokerUsername"], jsonConfig["brokerPassword"])
    scanner = BLEScanner(bleMacToDevice, jsonConfig["scanForSeconds"])

    # Handle scan and publish
    lastPushed = {} # Needed for publishOnlyChanges option
    def scanAndHandleResult():
        logging.info("Scan for BLE devices!")
        scanResult = scanner.scanAndUpdateData()
        for deviceId in scanResult.keys():
            scanData = scanResult[deviceId]
            deviceData = idToDevice[deviceId]
            # Handle smart meter
            if deviceData.deviceType == DeviceType.SB_METER:
                hasPushedLastAndActive = (deviceId in lastPushed) and jsonConfig["publishOnlyChanges"]
                publishStatus: int = 0
                if not hasPushedLastAndActive or lastPushed[deviceId].temperature != scanData.temperature:
                    publishStatus = mqttClient.publish(f'{deviceData.deviceDescription}/temperature', str(scanData.temperature))
                if not hasPushedLastAndActive or lastPushed[deviceId].humidity != scanData.humidity:
                    publishStatus = mqttClient.publish(f'{deviceData.deviceDescription}/humidity', str(scanData.humidity))
                if not hasPushedLastAndActive or lastPushed[deviceId].batteryLevel != scanData.batteryLevel:
                    publishStatus = mqttClient.publish(f'{deviceData.deviceDescription}/batteryLevel', str(scanData.batteryLevel))

                # Update only when publish operation succeeded
                if publishStatus == 0:
                    lastPushed[deviceId] = scanData
        # New round
        scheduler.enter(jsonConfig["rescanTime"],1,scanAndHandleResult)

    # Scheduler
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(10,1,scanAndHandleResult) # Wait 10 seconds in order to establish connection
    scheduler.run(True)
