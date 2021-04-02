from Btle import BtleDevice
import struct, bluepy
from time import sleep

class SmartTemp(BtleDevice):

    def __init__(self, mac_addy):
        BtleDevice.__init__(self, mac_addy)

    def run(self):

        try:
            while True:

                while not self.connected():
                    print("Connecting...")
                    try:
                        self.connect()
                    except bluepy.btle.BTLEDisconnectError as e:
                        print("Unable to connect.  Trying again in 1 minute (%s)"%(e,))
                        sleep(60)
                    else:
                        print("Connected.")

                try:
                    handledata = self.wait_for_notification()
                except bluepy.btle.BTLEDisconnectError:
                    print("Device disconnected.  Shutting down old connection...")
                    self.disconnect()
                else:
                    if handledata is None:
                        print("Wait_for_notification returned None even though no timeout given.")
                        break
                    handle, data = handledata
                    if handle == 0x18 and len(data) == 8:
                        temp = struct.unpack('<H', data[-4:-2])[0]
                        print("Temperature: %.2fC / %.2fF"%(temp/100, temp/100*9/5+32))

        finally:
            self.disconnect()


st = SmartTemp("AA:BB:CC:DD:EE:FF") # <- MAC addy of your thermometer goes here...
st.run()