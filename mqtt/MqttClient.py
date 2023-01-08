from paho.mqtt import client as mqtt_client

class MqttClient:

    def __init__(self, brokerIP: str, brokerPort: int, mqttClientName: str, username: str = None, password: str = None):
        self.brokerIP = brokerIP
        self.brokerPort = brokerPort
        self.mqttClientName = mqttClientName

        if username is not None:
            self.username = username
        if password is not None:
            self.password = password

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker at address: " + self.brokerIP)
            else:
                print("Failed to connect, return code is %d\n", rc)

        self._client = mqtt_client.Client(self.mqttClientName)
        self._client.username_pw_set(self.username, self.password)
        self._client.on_connect = on_connect
        self._client.connect(self.brokerIP, self.brokerPort)
        self._client.loop_start()

    def publish(self, topic: str, content: str):
        result = self._client.publish(topic, content)
        status = result[0]
        if status == 0:
            print(f"Send `{content}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

