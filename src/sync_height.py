import CoDrone
import keyboard
from CoDrone.system import Direction
from CoDrone.system import Mode
from time import sleep


errorRange = 50  # 오차범위
moveRange = 150  # 움직였다고 판단할 거리
heightRange = 70  # 움직였다고 판단할 거리 height

# 키보드로 콘솔창에 'q'를 누르면 드론이 착륙하게 만드는 코드
def stop(_master, _slave):
    if keyboard.is_pressed('q'):  # 키보드에서 'q'가 입력되면 while문 탈출
        print('[Keyboard input occur: Quit!]')
        # 착륙에 성공할 때까지 LED 효과
        _master.arm_default_pattern(0, 125, 155, Mode.DOUBLE_BLINK, 10)
        _slave.arm_default_pattern(0, 125, 155, Mode.DOUBLE_BLINK, 10)
        return True
    elif not _slave.isConnected():  # slave 연결이 끊기면 프로그램 종료
        print('[Slave Disconnected]')
        return True


def setHeight(_master, _mHeight, _slave):
    print('목표높이 : ', _mHeight)
    while True:
        _master.hover()
        print('hover')
        _sHeight = _slave.get_height()
        print('현재높이 : ', _sHeight)

        if stop(_master, _slave):
            return

        if _mHeight - errorRange <= _sHeight <= _mHeight + errorRange:
            print('[hit]')
            return
        elif _sHeight < _mHeight - errorRange:
            _slave.go(Direction.UP, 0, 100)
            # sleep(0.2)
            print('[up]')
        elif _sHeight > _mHeight + errorRange:
            _slave.go(Direction.DOWN, 0, 100)
            # sleep(0.2)
            print('[down]')


def main():
    master = CoDrone.CoDrone()
    master.connect("None", "COM7", False)
    slave = CoDrone.CoDrone()
    slave.connect("None", "COM5", False)

    bHeight = master.get_height()  # 고도
    if bHeight > 20:  # 마스터의 높이가 20이상이면 slave 날기 시작
        slave.takeoff()


    while True:
        master.arm_off()
        slave.arm_off()
        # master
        mPosition = master.get_opt_flow_position()  # 상대좌표 (시작 0,0)
        mHeight = master.get_height()  # 고도
        # slave
        sPosition = slave.get_opt_flow_position()
        sHeight = slave.get_height()
        print("master [x={} y={} z={}]   slave [x={} y={} z={}]"
              .format(mPosition.X, mPosition.Y, mHeight, sPosition.X, sPosition.Y, sHeight))  # 좌표출력/단위(mm)

        if stop(master, slave):
            break

        # master의 전 높이 대비 +- moveRange 만큼의 차이가 있으면 slave가 움직이도록
        if abs(mHeight - bHeight) > heightRange:
            print('[height change!]')
            # LED 효과
            master.arm_strobe()
            slave.arm_strobe()
            setHeight(master, mHeight, slave)

    print('Land')
    slave.land()  # 착륙
    master.arm_off()
    slave.arm_off()

    # 연결해제 -> 여기까지 성공했다면 배터리 안 빼도 다시 연결 됩니다.
    slave.disconnect()
    master.disconnect()


if __name__ == '__main__':
    main()
