from bluepy.btle import DefaultDelegate, Scanner

from devices.MeterData import MeterData
from datetime import datetime


class BLEScanner:
    DataFound: dict = {}

    def __init__(self, searchDevices: dict[str, int]):
        self.scanner = Scanner()
        self._scanReult: dict[int, MeterData] = {}
        self.scanner.withDelegate(HandleDataWithoutConnection(searchDevices, self._scanReult))

    def scanAndUpdateData(self) -> dict[int, MeterData]:
        self.scanner.start(False)
        self.scanner.process(10.0)
        self.scanner.stop()
        return self._scanReult

    def finish(self):
        self.scanner.stop()


class HandleDataWithoutConnection(DefaultDelegate):

    def __init__(self, searchDevices: dict[str,int], scanResult: dict):  # Dictionary between BLE Mac address to id
        DefaultDelegate.__init__(self)
        self.searchDevices = searchDevices
        self._scanResult = scanResult

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr in self.searchDevices.keys():
            if dev.getValueText(22) is not None:
                deviceId: int = self.searchDevices[dev.addr]
                hexData = int(dev.getValueText(22), 16)
                self._scanResult[deviceId] = MeterData(hexData, deviceId, datetime.now())