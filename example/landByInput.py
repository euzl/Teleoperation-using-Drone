# 드론 착륙 by 키보드; 테스트 코드 (드론 1대용)
import CoDrone
import keyboard


def getPosition(drone):
    position = drone.get_opt_flow_position()  # 상대좌표 (시작 0,0)
    height = drone.get_height()  # 고
    print("x={} y={} z={}".format(position.X, position.Y, height))  # 단위(mm)


def main():
    drone = CoDrone.CoDrone()
    drone.connect()

    drone.takeoff()  # 이륙

    while True:
        getPosition(drone)
        if keyboard.is_pressed('q'):  # 키보드에서 'q'가 입력되면 while문 탈출
            print('Keyboard input occur: Quit!')
            break
        elif not drone.isConnected():  # 연결이 끊기면 프로그램 종료
            print('Disconnected')
            return

    print('드론을 착륙시킵니다.')
    drone.arm_pattern()  # LED 효과
    print('Land')
    drone.land()  # 착륙
    drone.disconnect()  # 연결해제


if __name__ == '__main__':
    main()



