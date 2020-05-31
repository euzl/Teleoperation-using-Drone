from CoDrone.codrone import *

if __name__ == '__main__':
    drone = CoDrone()
    drone.connect(portName="/dev/tty.SLAB_USBtoUART")
    sleep(1)
    if drone.isConnected():
        drone.setEyeDefaultRGB(0, 255, 0)
        drone.setArmRGB(100, 0, 0)
        sleep(1)
        drone.setEyeDefaultRGB(255, 255, 0)
        drone.setArmRGB(0, 255, 0)
        sleep(1)

        drone.sendLinkDisconnect()
        sleep(0.2)

    drone.close()
