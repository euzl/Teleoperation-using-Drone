# 움직임 감지 (드론 1대)
import CoDrone
import keyboard
from CoDrone.system import Direction
from CoDrone.system import Mode
from time import sleep


errorRange = 50  # 오차범위
heightRange = 50  # 움직였다고 판단할 거리 height
posiRange = 50  # position (x, y) 변화 인지 거리


def setHeight(_mHeight, _slave):
    while True:
        _sHeight = _slave.get_height()
        if _mHeight - errorRange <= _sHeight <= _mHeight + errorRange:
            print('[hit]')
            return
        elif _sHeight < _mHeight - errorRange:
            _slave.go(Direction.UP)
            sleep(0.2)
            print('[up]')
        elif _sHeight > _mHeight + errorRange:
            _slave.go(Direction.DOWN)
            sleep(0.2)
            print('[down]')


def main():
    master = CoDrone.CoDrone()
    master.connect("None", "COM5", False)

    bHeight = 0
    bX = 0
    bY = 0

    while True:
        master.arm_off()
        # master
        mPosition = master.get_opt_flow_position()  # 상대좌표 (시작 0,0)
        mHeight = master.get_height()  # 고도
        print("master x={} y={} z={}"
              .format(mPosition.X, mPosition.Y, mHeight))  # 좌표출력/단위(mm)
        print("before x={} y={} z={}"
              .format(bX, bY, bHeight))  # 좌표출력/단위(mm)

        # 성공 : q를 계속 누르고 계세요! ex) qqqqqqqqqqqqqq
        if keyboard.is_pressed('q'):  # 키보드에서 'q'가 입력되면 while문 탈출
            print('[Keyboard input occur: Quit!]')
            master.arm_default_pattern(0, 125, 155, Mode.DOUBLE_BLINK, 10)
            break
        elif not master.isConnected():  # slave 연결이 끊기면 프로그램 종료
            print('[Slave Disconnected]')
            return

        # master의 전 높이 대비 heightRange 만큼의 차이가 있으면 slave가 움직이도록
        if abs(mHeight-bHeight) > heightRange:
            # setHeight(mHeight, slave)
            print('[height change!]')
            master.arm_strobe()

        # master의 좌표가 posiRange만큼 차이가 생기면 움직이도록
        if abs(bX - mPosition.X) + abs(bY - mPosition.Y) > posiRange:
            # slave.move(mPosition.Y - bY, bX - mPosition.X, 0, 0)  # move(roll 좌우, pitch 전후, yaw = 0, throttle = 0)
            print('[position change!]')
            master.arm_strobe()

        # master의 이전 좌표값 저장
        bHeight = mHeight
        bX = mPosition.X
        bY = mPosition.Y

    print('드론을 착륙시킵니다.')
    master.arm_pattern()  # LED 효과
    print('Land')
    master.land()  # 착륙
    master.arm_off()
    # 연결해제 -> 여기까지 성공했다면 배터리 안 빼도 다시 연결 됩니다.
    master.disconnect()


if __name__ == '__main__':
    main()
