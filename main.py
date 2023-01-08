from ble.BleScanner import BLEScanner
from mqtt.MqttClient import MqttClient

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sb_addr = "da:0a:5e:39:12:39"

    scan = {
        "da:0a:5e:39:12:39": 1
    }

    mqttClient = MqttClient("192.168.178.43", 1883, "RPI_SB_HUB1", "test1", "123456")
    scanner = BLEScanner(scan)
    while True:
        scanResult = scanner.scanAndUpdateData()
        res = scanResult[1]
        print(res.temperature)
        print(res.humidity)
        mqttClient.publish("test1/temperature1", str(res.temperature))
        mqttClient.publish("test1/humidity", str(res.humidity))
        mqttClient.publish("test1/batteryLevel", str(res.batteryLevel))
        print("Next Round!")