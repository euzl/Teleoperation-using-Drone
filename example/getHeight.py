import CoDrone
from CoDrone import Direction
from time import sleep

def main():
    drone = CoDrone.CoDrone()
    drone.pair()

    drone.takeoff()

    for i in range(50):
        height = drone.get_height()
        if height > 1000:
            drone.go(Direction.DOWN)
        elif height < 500:
            drone.go(Direction.UP)
        sleep(0.1)

    drone.land()

if __name__ == '__main__':
    main()