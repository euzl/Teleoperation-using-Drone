import CoDrone

def main():
    drone = CoDrone.CoDrone()
    drone.connect()

    while True:
        # print the acceleration of drone
        position = drone.get_opt_flow_position()
        height = drone.get_height()
        print("x={} y={} z={}".format(position.X, position.Y, height))


if __name__ == '__main__':
    main()