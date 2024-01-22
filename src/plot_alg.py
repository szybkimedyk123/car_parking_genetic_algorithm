import matplotlib.pyplot as plt
import os

def start():
    iteration_values = []
    evaluation_values = []
    distance_values = []
    path_values = []
    time_values = []
    angle_values = []


    folder_name = os.path.join('..', 'data')
    data_name = 'performance.txt'
    file_path_data = os.path.join(folder_name, data_name)

    with open(file_path_data, 'r') as file:
        lines = file.readlines()

    # print(lines)

    for line in lines:
        parts = line.strip().strip('()').split('[', 1)

        index = parts[0].split(',')[0]

        values = parts[1].strip(']').split(', ')

        iteration_values.append(int(index))
        evaluation_values.append(float(values[0]))
        distance_values.append(float(values[1]))
        path_values.append(float(values[2]))
        time_values.append(float(values[3]))
        angle_values.append(float(values[4]))

        index = int(index)

        if index == 0 or index == 9 or index == 24 or index == 49 or index == 74 or index == 99 :
            print(index)
            print("distance = " + str(float(values[2])))
            print("time = " + str(float(values[3])))
            print("place = " + str(float(values[1])))
            print("angle = " + str(float(values[4])))
            print("evaluation = " + str(float(values[0])))


    fig, axs = plt.subplots(2, 2, figsize=(10, 6))

    axs[0, 0].plot(distance_values, linestyle='-')
    axs[0, 0].grid(True)
    axs[0, 0].set_title('Place Evaluation')
    axs[0, 0].set_xlabel('Algorithm Step')
    axs[0, 0].set_ylabel('Place Evaluation Value')

    axs[0, 1].plot(path_values, linestyle='-', color='red')
    axs[0, 1].grid(True)
    axs[0, 1].set_title('Path Evaluation')
    axs[0, 1].set_xlabel('Algorithm Step')
    axs[0, 1].set_ylabel('Path Evaluation Value')

    axs[1, 0].plot(time_values, linestyle='-', color='green')
    axs[1, 0].grid(True)
    axs[1, 0].set_title('Time Evaluation')
    axs[1, 0].set_xlabel('Algorithm Step')
    axs[1, 0].set_ylabel('Time Evaluation Value')

    axs[1, 1].plot(angle_values, linestyle='-', color='orange')
    axs[1, 1].grid(True)
    axs[1, 1].set_title('Parking Evaluation')
    axs[1, 1].set_xlabel('Algorithm Step')
    axs[1, 1].set_ylabel('Parking Evaluation Value')

    plt.tight_layout()
    plt.show()

    plt.plot(iteration_values, evaluation_values, linestyle='-', color='green')
    plt.title('Final Evaluation')
    plt.xlabel('Algorithm Step')
    plt.ylabel('Final Evaluation Value')
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    start()