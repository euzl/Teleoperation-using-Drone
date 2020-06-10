import CoDrone
from CoDrone import Direction
from time import sleep


def main():
    drone = CoDrone.CoDrone()
    drone.connect()

    drone.takeoff()

    drone.go(Direction.DOWN)
    sleep(0.001)
    drone.go(Direction.UP)
    sleep(0.2)

    drone.land()


if __name__ == '__main__':
    main()