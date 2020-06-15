# step 2 : 높이 + 위치조정
import CoDrone
import keyboard
from CoDrone.system import Direction
from time import sleep


errorRange = 50  # 오차범위
moveRange = 150  # 움직였다고 판단할 거리


def setHeight(_mHeight, _slave):
    while True:
        _sHeight = _slave.get_height()
        if _mHeight - errorRange <= _sHeight <= _mHeight + errorRange:
            print('hit')
            return
        elif _sHeight < _mHeight - errorRange:
            _slave.go(Direction.UP)
            sleep(0.2)
            print('up')
        elif _sHeight > _mHeight + errorRange:
            _slave.go(Direction.DOWN)
            sleep(0.2)
            print('down')


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
        # 로 keyboard를 설치한 다음 실행해야 합니다.
        if keyboard.is_pressed('q'):
            print('드론을 착륙시킵니다.')
            slave.land()
            print('land')
            # slave.emergency_stop()
            # print('emergency_stop')
            break

        # master의 전 높이 대비 moveRange 만큼의 차이가 있으면 slave가 움직이도록
        if abs(mHeight-bHeight) > moveRange:
            setHeight(mHeight, slave)

        # master의 좌표가 moveRange만큼 차이가 생기면 움직이도록
        if abs(bX - mPosition.X) > moveRange or abs(bY - mPosition.Y) > moveRange:
            slave.move(mPosition.Y - bY, bX - mPosition.X, 0, 0)  # move(roll 좌우, pitch 전후, yaw = 0, throttle = 0)

        # master의 이전 좌표값 저장
        bHeight = mHeight
        bX = mPosition.X
        bY = mPosition.Y


if __name__ == '__main__':
    main()
