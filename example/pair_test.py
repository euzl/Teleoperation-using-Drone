import CoDrone

def main():
    drone = CoDrone.CoDrone()
    drone.pair()

    drone.takeoff()
    drone.hover(3)
    drone.land()


if __name__ == '__main__':
    main()
