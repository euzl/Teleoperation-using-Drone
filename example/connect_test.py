from time import sleep

from e_drone.drone import *
from e_drone.protocol import *

if __name__ == '__main__':

    drone = Drone()
    drone.open("COM5")

    drone.sendBuzzer(BuzzerMode.Scale, BuzzerScale.C4.value, 500)
    sleep(1)

    drone.close()
