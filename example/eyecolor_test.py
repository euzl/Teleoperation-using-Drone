from CoDrone.codrone import *

if __name__ == '__main__':

    drone = CoDrone()
    drone.pair()
    #drone.open("COM5")
    
    #drone.connect(portName="COM5")
    sleep(1)

    while drone.isConnected():

        drone.setEyeDefaultRGB(0, 255, 0)
        drone.setArmRGB(100, 0, 0)
        sleep(1)
        drone.setEyeDefaultRGB(255, 255, 0)
        drone.setArmRGB(0, 255, 0)
        sleep(1)

    drone.sendLinkDisconnect()
    sleep(0.2)

    drone.close()
