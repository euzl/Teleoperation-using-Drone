import CoDrone
from CoDrone.system import Direction


def getPosition(drone):
    position = drone.get_opt_flow_position()  # 상대좌표 (시작 0,0)
    height = drone.get_height()  # 고
    print("x={} y={} z={}".format(position.X, position.Y, height))  # 단위(mm)


def main():
    drone = CoDrone.CoDrone()
    drone.connect()

    drone.takeoff()
    getPosition(drone)
    drone.move(-5, 4, 0, 0)  # move(roll 좌우, pitch 전후, yaw, throttle)
    # drone.go(Direction.FORWARD, 0.5)
    # print('forward')
    # getPosition(drone)
    # drone.go(Direction.LEFT, 1)
    # print('left')
    getPosition(drone)
    drone.hover(3)
    getPosition(drone)
    print('land')
    getPosition(drone)
    drone.land()


if __name__ == '__main__':
    main()



