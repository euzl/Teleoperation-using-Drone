import CoDrone
import keyboard
from CoDrone.system import Direction
from time import sleep


def setHeight(_mHeight, _slave):
    while True:
        _sHeight = _slave.get_height()
        if _mHeight - 100 <= _sHeight <= _mHeight + 100:
            return
        elif _sHeight < _mHeight - 100:
            _slave.go(Direction.UP)
            sleep(0.2)
        elif _sHeight > _mHeight + 100:
            _slave.go(Direction.DOWN)
            sleep(0.2)


def main():
    master = CoDrone.CoDrone()
    master.connect("None", "COM5", False)
    slave = CoDrone.CoDrone()
    slave.connect("None", "COM6", False)

    bHeight = master.get_height()  # 고도
    if bHeight > 20:  # 마스터의 높이가 20이상이면 slave 날기 시작
        slave.takeoff()

    while True:
        # master
        mPosition = master.get_opt_flow_position()  # 상대좌표 (시작 0,0)
        mHeight = master.get_height()  # 고도
        # slave
        sPosition = slave.get_opt_flow_position()
        sHeight = slave.get_height()
        print("master [x={} y={} z={}]   slave [x={} y={} z={}]"
              .format(mPosition.X, mPosition.Y, mHeight, sPosition.X, sPosition.Y, sHeight))  # 좌표출력/단위(mm)

        # 키보드로 콘솔창에 'q'를 누르면 드론이 착륙하게 만드는 코드인데
        # 한 번 성공하고 그 이후로 안 되네요
        # $pip3 install keyboard
        # 로 깔아야 합니다.
        if keyboard.is_pressed('q'):
            print('드론을 착륙시킵니다.')
            slave.land()
            print('land')
            # slave.emergency_stop()
            # print('emergency_stop')
            break

        # master의 전 높이 대비 +- 150의 차이가 있으면 slave가 움직이도록
        if mHeight > bHeight + 150 or mHeight < bHeight - 150:
            setHeight(mHeight, slave)

        bHeight = mHeight


if __name__ == '__main__':
    main()
