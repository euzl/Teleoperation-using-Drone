import CoDrone


def main():
    drone = CoDrone.CoDrone()
    drone.connect()  # 안 날고 연결만

    while True:
        # print the acceleration of drone
        position = drone.get_opt_flow_position()  # 상대좌표 (시작 0,0)
        height = drone.get_height()  # 고
        print("x={} y={} z={}".format(position.X, position.Y, height))  # 단위(mm)


if __name__ == '__main__':
    main()


