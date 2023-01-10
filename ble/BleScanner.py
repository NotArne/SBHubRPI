from bluepy.btle import DefaultDelegate, Scanner

from devices.DeviceDescription import DeviceDescription, DeviceType
from devices.MeterData import MeterData
from datetime import datetime


class BLEScanner:
    DataFound: dict = {}

    def __init__(self, searchDevices: dict[str, DeviceDescription], scanForSeconds: float):
        self.scanner = Scanner()
        self._scanReult: dict = {}
        self.scanner.withDelegate(HandleDataWithoutConnection(searchDevices, self._scanReult))
        self.scanForSeconds = scanForSeconds

    def scanAndUpdateData(self) -> dict[int, MeterData]:
        self.scanner.start(False)
        self.scanner.process(self.scanForSeconds)
        self.scanner.stop()
        return self._scanReult

    def finish(self):
        self.scanner.stop()


class HandleDataWithoutConnection(DefaultDelegate):

    def __init__(self, searchDevices: dict[str,DeviceDescription], scanResult: dict):  # Dictionary between BLE Mac address to id
        DefaultDelegate.__init__(self)
        self.searchDevices = searchDevices
        self._scanResult = scanResult

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr.lower() in self.searchDevices.keys():
            deviceId: int = self.searchDevices[dev.addr.lower()].deviceId

            # Handle SB smart meter
            if self.searchDevices[dev.addr.lower()].deviceType == DeviceType.SB_METER:
                if dev.getValueText(22) is not None:
                    hexData = int(dev.getValueText(22), 16)
                    self._scanResult[deviceId] = MeterData(hexData, deviceId, datetime.now())