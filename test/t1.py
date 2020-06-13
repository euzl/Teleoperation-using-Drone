# 앞으로 이동하고 거리를 일치시키는 테스트
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
        mPosition = master.get_opt_flow_mPosition()  # 상대좌표 (시작 0,0)
        mHeight = master.get_mHeight()  # 고도
        print("x={} y={} z={}".format(mPosition.X, mPosition.Y, mHeight))  # 단위(mm)
        if 40 > mHeight > 20:  # 높이 제약
            slave.takeoff()
            slave.go(Direction.FORWARD, mPosition.X, 10)
            slave.hover(5)
            slave.go(Direction.FORWARD, mPosition.X, 10)

        # 종료조건
        elif mHeight < -20:
            slave.land()
            return


if __name__ == '__main__':
    main()
