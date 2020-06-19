# step 2 : 높이 + 위치조정 (민감버전)
import CoDrone
import keyboard
from CoDrone.system import Direction
from CoDrone.system import Mode
from time import sleep


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


def main():
    master = CoDrone.CoDrone()
    master.connect("None", "COM5", False)
    slave = CoDrone.CoDrone()
    slave.connect("None", "COM6", False)

    bHeight = master.get_height()  # 고도
    if bHeight > 20:  # 마스터의 높이가 20이상이면 slave 날기 시작
        slave.takeoff()
        print('slave take off!!!')

    # master의 이전 좌표값(움직임 추적용) 초기화
    bHeight = 0
    bX = 0
    bY = 0

    while True:
        master.arm_off()
        slave.arm_off()
        slave.takeoff()
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

        # master의 전 높이 대비 heightRange 만큼의 차이가 있으면 slave가 움직이도록
        # if abs(mHeight - bHeight) > heightRange:
        #     print('[height change!]')
        #     # LED 효과
        #     master.arm_strobe()
        #     slave.arm_strobe()
        #     setHeight(mHeight, slave)

        if mPosition.X > bX:
            slave.go(Direction.FORWARD, 1)
            print('[Move Forward]')
        elif mPosition.X < bX:
            slave.go(Direction.BACKWARD, 1)
            print('[Move Backward]')

        # elif mPosition.Y > bY:
        #     slave.go(Direction.LEFT, 0.4)
        #     print('[Move Left]')
        # elif mPosition.Y < bY:
        #     slave.go(Direction.RIGHT, 0.4)
        #     print('[Move Right]')

        # master의 이전 좌표값 저장
        bHeight = mHeight
        bX = mPosition.X
        bY = mPosition.Y
        # slave.hover()

    print('드론을 착륙시킵니다.')
    slave.arm_pattern()  # LED 효과

    print('Land')
    slave.land()  # 착륙
    master.arm_off()
    slave.arm_off()

    # 연결해제 -> 여기까지 성공했다면 배터리 안 빼도 다시 연결 됩니다.
    slave.disconnect()
    master.disconnect()


if __name__ == '__main__':
    main()
