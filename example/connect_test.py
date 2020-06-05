from time import sleep
import CoDrone

def main():
    drone = CoDrone.CoDrone()
    drone.pair()

    drone.sendBuzzer(BuzzerMode.Scale, BuzzerScale.C4.value, 500)
    sleep(1)

    drone.close()

if __name__ == '__main__':
    main()
