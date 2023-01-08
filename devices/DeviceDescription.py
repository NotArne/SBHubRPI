from enum import Enum


class DeviceType(Enum):
    SB_METER = 0


class DeviceDescription:
    def __init__(self, deviceId: int, bleMacAddress: str, deviceDescription: str, deviceType: DeviceType):
        self._deviceId = deviceId
        self.bleMacAddress = bleMacAddress
        self.deviceDescription = deviceDescription
        self.deviceType = deviceType
