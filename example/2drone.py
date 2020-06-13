import CoDrone
from CoDrone import Direction
import time


def main():
    master = CoDrone.CoDrone()
    master.connect("None", "COM5", False)  # 안 날고 연결만
    slave = CoDrone.CoDrone()
    slave.connect("None", "COM6", False)

    while True:
        time.sleep(5)
    # print the acceleration of drone
        position = master.get_opt_flow_position()  # 상대좌표 (시작 0,0)
        height = master.get_height()  # 고
        print("x={} y={} z={}".format(position.X, position.Y, height))  # 단위(mm)
        if 30 > height > 20:
            slave.takeoff()
            slave.go(Direction.FORWARD, position.X, 10)
    # drone.turn(Direction.LEFT, 3, 30)  # 돌려서 이동하려 했었다.
            slave.hover(5)
            slave.go(Direction.FORWARD, position.X, 10)
    #while True:


if __name__ == '__main__':
    main()


