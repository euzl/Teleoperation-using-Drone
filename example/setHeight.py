# 드론 높이조정 테스트 코드 (드론 1대용)
import CoDrone
from CoDrone.system import Direction
from time import sleep


errorRange = 50  # 오차범위


def getPosition(drone):
    position = drone.get_opt_flow_position()  # 상대좌표 (시작 0,0)
    height = drone.get_height()  # 고
    print("x={} y={} z={}".format(position.X, position.Y, height))  # 단위(mm)


def setHeight(_mHeight, _slave):
    while True:
        _sHeight = _slave.get_height()
        if _mHeight - errorRange <= _sHeight <= _mHeight + errorRange:
            print('hit')
            return
        elif _sHeight < _mHeight - errorRange:
            _slave.go(Direction.UP)
            getPosition(_slave)
            sleep(0.2)
            print('up')
        elif _sHeight > _mHeight + errorRange:
            _slave.go(Direction.DOWN)
            getPosition(_slave)
            sleep(0.2)
            print('down')


def main():
    drone = CoDrone.CoDrone()
    drone.connect()

    oHeight = 200  # 목적 높이

    drone.takeoff()
    getPosition(drone)
    setHeight(oHeight, drone)
    getPosition(drone)
    drone.hover(3)
    print('Land')
    drone.land()


if __name__ == '__main__':
    main()



