import os
from algorithm2 import *
from visualization import *
from const import *


def start(algorithm_parameters, options, parking=parking, target_position=target_position, parking_space=parking_space, state=state):
#algorithm_parameters=algorithm_parameters, parking=parking, target_position=target_position, parking_space=parking_space, state=state):

    trajectory_x = []
    trajectory_y = []
    o_d = 0

    best_solution, history_alg = evolutionary_algorithm(
        algorith_parameters=algorithm_parameters,
        target_position=target_position,
        parking_spot=parking_space,
        parking=parking,
        start_position=state
    )

    state_trajectory = np.zeros((len(best_solution) + 1, 5))

    folder_name = 'data'
    data_name = 'performance.txt'
    car_name = 'simulation.txt'

    src_path = os.path.dirname(os.path.abspath(__file__))

    data_path = os.path.abspath(os.path.join(src_path, '..', folder_name))

    file_path_data = os.path.join(data_path, data_name)
    file_path_car = os.path.join(data_path, car_name)

    # if not os.path.exists(folder_name):
    #     os.makedirs(folder_name)

    with open(file_path_data, 'w') as file:

        for item in history_alg:
            file.write(str(item) + '\n')

    with open(file_path_car, 'w') as file:

        for i in range(len(best_solution)):
            u = best_solution[i]  
            state = kinematic_model(state, u)

            state_trajectory[i + 1] = state

            file.write(str(i / 10) + ' ')

            for item in state_trajectory[i]:
                file.write(str(item) + ' ')

            for item in best_solution[i]:
                file.write(str(item) + ' ')
            file.write('\n')

            if i > 0:
                x_diff = state_trajectory[i][0] - state_trajectory[i - 1][0]
                y_diff = state_trajectory[i][1] - state_trajectory[i - 1][1]

                o_d += np.sqrt(x_diff ** 2 + y_diff ** 2)

    o_m = np.sqrt((state_trajectory[len(best_solution)][0] - target_position[0]) ** 2 + (
                state_trajectory[len(best_solution)][1] - target_position[1]) ** 2)
    angle = state_trajectory[len(best_solution)][3]

    if angle > np.pi:
        angle = np.pi - (angle - np.pi)

    o = 0.5 * o_m + o_d + len(best_solution) / 10 + 0.5 * abs(90 - abs(np.degrees(angle)))

    print("odległość = " + str(o_m))
    print("droga = " + str(o_d))
    print("czas = " + str(len(best_solution)))
    print("kąt = " + str(90 - np.degrees(abs(angle))))
    print("ocena = " + str(o))

    visualize_trajectory(state_trajectory, parking_space, parking, trajectory_x, trajectory_y)
    # app = QApplication(sys.argv)
    # mainWin = MyMainWindow(state_trajectory, parking_space, parking, trajectory_x, trajectory_y)
    # sys.exit(app.exec_())

    # return state_trajectory, parking_space, parking, trajectory_x, trajectory_y


if __name__ == "__main__":
    start()