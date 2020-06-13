# 앞으로 이동하고 거리를 일치시키는 테스트 (duration 없이, 일치하면 stop)
import CoDrone
from CoDrone import Direction
import time


def main():
    # 드론 셋팅
    master = CoDrone.CoDrone()
    master.connect("None", "COM5", False)
    slave = CoDrone.CoDrone()
    slave.connect("None", "COM6", False)

    while True:
        # master
        mPosition = master.get_opt_flow_position()  # 상대좌표 (시작 0,0)
        mHeight = master.get_height()  # 고도
        # slave
        sPosition = slave.get_opt_flow_position()
        sHeight = slave.get_height()
        print("master [x={} y={} z={}]   slave [x={} y={} z={}]"
              .format(mPosition.X, mPosition.Y, mHeight, sPosition.X, sPosition.Y, sHeight))  # 좌표출력/단위(mm)
        if mHeight > 20:  # 높이 제약
            slave.takeoff()
            while sPosition.X <= mPosition.X:  # slave의 x좌표가 master의 x보다 작을 때까지!
                # 약간... 양수로만 움직인다고 가정
                slave.go(Direction.FORWARD)

        # 종료조건
        elif mHeight < -20:
            slave.land()
            # 연결끊기
            master.disconnect()
            slave.disconnect()
            return


if __name__ == '__main__':
    main()
