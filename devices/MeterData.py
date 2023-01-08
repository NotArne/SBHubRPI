from enum import Enum

class TemperatureScale(Enum):
    F = 1  # Fahrenheit
    C = 2  # Celsius


class MeterData:

    # Have a look at: https://github.com/OpenWonderLabs/SwitchBotAPI-BLE/blob/latest/devicetypes/meter.md
    def __init__ (self, hexData: int, deviceId: int, timestamp):
        self.deviceId = deviceId
        self.timestamp = timestamp

        hexData &= 0x00000000000000000000FFFFFFFFFFFF  # Field can be up to 16b, zero not used byte
        byte5: int = (hexData & 0x0000000000FF)
        self.temperatureScale = TemperatureScale.F if ((byte5 >> 7) > 0) else TemperatureScale.C
        self.humidity = byte5 & 0b0111_1111
        byte4: int = (hexData & 0x00000000FF00) >> 2 * 4
        self.isTemperaturePositive = True if((byte4 >> 7) > 0) else False
        self.temperature = float(byte4 & 0b0111_1111)  # Always in Celsius
        byte3: int = ((hexData & 0x000000FF0000) >> (4 * 4)) & 0b0000_1111
        self.temperature += byte3 * 0.1
        if not self.isTemperaturePositive:
            self.temperature *= -1
        byte2: int = ((hexData & 0x0000FF000000) >> 6 * 4) & 0b0111_1111
        self.batteryLevel = byte2