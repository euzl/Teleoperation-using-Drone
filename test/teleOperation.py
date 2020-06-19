# step 2 : 높이 + 위치조정 (master도 날 때)
import CoDrone
import keyboard
from CoDrone.system import Direction
from CoDrone.system import Mode
from time import sleep


errorRange = 100  # 오차범위
heightRange = 70  # 움직였다고 판단할 거리 height
posiRange = 5  # position (x, y) 변화 인지 거리
fbRange = 15  # 피드백받을 slave의 높이 범위


def stop(_master, _slave):
    # 키보드로 콘솔창에 'q'를 누르면 드론이 착륙하게 만드는 코드
    # $pip3 install keyboard
    # 로 keyboard를 설치한 다음 실행해야 합니다.
    # 성공 : q를 계속 누르고 계세요! ex) qqqqqqqqqqqqqq
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
    slave = CoDrone.CoDrone()
    slave.connect("None", "COM7", False)

    master.takeoff()
    slave.takeoff()

    # master의 이전 좌표값(움직임 추적용) 초기화
    bHeight = 0
    sbHeight = 0
    bX = 0
    bY = 0

    direction = 1  # slave 방향 변화 (1:위/0:아래)

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

        # slave의 이전 좌표값 저장
        sbHeight = sHeight


        # master의 전 높이 대비 heightRange 만큼의 차이가 있으면 slave가 움직이도록
        if abs(mHeight - bHeight) > heightRange:
            print('[height change!]')
            # LED 효과
            master.arm_strobe()
            slave.arm_strobe()
            setHeight(master, mHeight, slave)

        # master의 좌표가 posiRange만큼 차이가 생기면 움직이도록
        if abs(bX - mPosition.X) + abs(bY - mPosition.Y) > posiRange:
            print('[position change!]')
            # LED 효과
            master.arm_strobe()
            slave.arm_strobe()
            slave.move(abs(mPosition.Y - bY)/20, abs(bX - mPosition.X)/20, 0, 0)  # move(roll 좌우, pitch 전후, yaw = 0, throttle = 0)

        # slave의 전 높이 대비 heightRange 만큼의 차이가 있으면 master가 움직이도록
        if abs(sHeight - sbHeight) > fbRange:
            print('[slave feedback!]')
            setHeight(slave, sHeight, master)  # master의 높이 이동
        # master의 이전 좌표값 저장
        bHeight = mHeight
        bX = mPosition.X
        bY = mPosition.Y

    print('드론을 착륙시킵니다.')
    slave.arm_pattern()  # LED 효과

    print('Land')
    master.land()
    slave.land()  # 착륙
    master.arm_off()
    slave.arm_off()

    # 연결해제 -> 여기까지 성공했다면 배터리 안 빼도 다시 연결 됩니다.
    slave.disconnect()
    master.disconnect()


if __name__ == '__main__':
    main()
