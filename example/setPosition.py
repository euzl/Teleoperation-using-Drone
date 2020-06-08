import CoDrone
from CoDrone import Direction


def main():
    drone = CoDrone.CoDrone()
    drone.connect()


    drone.takeoff()
    drone.go(Direction.FORWARD, 3, 10)
    # drone.turn(Direction.LEFT, 3, 30)  # 돌려서 이동하려 했었다.
    drone.go(Direction.LEFT, 7, 10)

    getPosition(drone)
    drone.land()


if __name__ == '__main__':
    main()


def getPosition(drone):
    position = drone.get_opt_flow_position()  # 상대좌표 (시작 0,0)
    height = drone.get_height()  # 고
    print("x={} y={} z={}".format(position.X, position.Y, height))  # 단위(mm)
