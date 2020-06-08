from CoDrone.codrone import *
from time import sleep


def main():
    drone = CoDrone()
    drone.pair()

    # print angles
    GyroAngles = drone.get_gyro_angles()
    print(GyroAngles.ROLL, GyroAngles.PITCH, GyroAngles.YAW)
    drone.set_event_handler(DataType.Altitude, eventAltitude)
    drone.send_request(DeviceType.Drone, DataType.Altitude)
    sleep(0.1)

    drone.close()


def eventAltitude(altitude):
    print("eventAltitude()")
    print("Altitude : {0:.3f}".format(altitude.altitude))


if __name__ == '__main__':
    main()
