from paho.mqtt import client as mqtt_client
import logging
import time

class MqttClient:

    def __init__(self, brokerIP: str, brokerPort: int, mqttClientName: str, username: str, password: str = None):
        self.brokerIP = brokerIP
        self.brokerPort = brokerPort
        self.mqttClientName = mqttClientName
        self.username = username
        self.password = password
        self.isConnected = False

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.isConnected = True
                logging.info("Connected to MQTT Broker at address: " + self.brokerIP)
            else:
                self.isConnected = False
                logging.error("Failed to connect, return code is %d\n", rc)

        self._client = mqtt_client.Client(self.mqttClientName)
        self._client.username_pw_set(self.username, self.password)
        self._client.on_connect = on_connect
        self._client.reconnect_delay_set(1,60)
        self._client.connect(self.brokerIP, self.brokerPort)
        self._client.loop_start()

    def publish(self, topic: str, content: str) -> int:
        result = self._client.publish(topic, content)
        status = result[0]
        if status == 0:
            logging.info(f"Send `{content}` to topic `{topic}`")
        else:
            logging.error(f"Failed to send message to topic {topic}")
        return status
