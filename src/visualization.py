import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse
from car import *
from const import *
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

src_dir = os.path.join(parent_dir, 'gui')

sys.path.append(src_dir)

import gui2



def update(frame, car_patch, parking_spot_patch, state_trajectory, trajectory_line, wheels, trajectory_x, trajectory_y):
    if frame < len(state_trajectory):
        current_state = state_trajectory[frame]
        x, y, delta, theta, v = current_state
        #print(np.degrees(z[2]))
        #print(np.degrees(theta))
        car_vertices = calc_car_vertices(current_state)
        car_patch.set_xy(car_vertices)

        r_1 = wheel(theta)
        r_2 = wheel(-theta)

        wheels[0].set_center((x + r_1[0],y + r_1[1]))
        wheels[0].set_angle(np.degrees(theta + delta))

        wheels[1].set_center((x + r_2[0], y - r_2[1]))
        wheels[1].set_angle(np.degrees(theta + delta))

        wheels[2].set_center((x - r_2[0], y + r_2[1]))
        wheels[2].set_angle(np.degrees(theta))

        wheels[3].set_center((x - r_1[0], y - r_1[1]))
        wheels[3].set_angle(np.degrees(theta))

        trajectory_x.append(current_state[0])
        trajectory_y.append(current_state[1])
        trajectory_line.set_data(trajectory_x, trajectory_y)

        return [car_patch, parking_spot_patch, trajectory_line] + wheels
    else:
        return [car_patch, parking_spot_patch, trajectory_line] + wheels


def visualize_trajectory(state_trajectory, parking_spot, parking, trajectory_x, trajectory_y):
    fig, ax = plt.subplots()

    car_vertices = calc_car_vertices(state_trajectory[0])
    car_patch = plt.Polygon(car_vertices, closed=True, edgecolor='black', facecolor='red')
    ax.add_patch(car_patch)

    f_l = Ellipse((0, 0), 0.5, 0.25, angle=0, fill=True, color='black')
    ax.add_patch(f_l)
    f_r = Ellipse((0, 0), 0.5, 0.25, angle=0, fill=True, color='black')
    ax.add_patch(f_r)
    b_l = Ellipse((0, 0), 0.5, 0.25, angle=0, fill=True, color='black')
    ax.add_patch(b_l)
    b_r = Ellipse((0, 0), 0.5, 0.25, angle=0, fill=True, color='black')
    ax.add_patch(b_r)

    wheels = [f_l, f_r, b_l, b_r]


    parking_patches = []
    for spot in parking:
        parking_patch = plt.Rectangle((spot[0], spot[2]), spot[1] - spot[0], spot[3] - spot[2],
                                      edgecolor='grey', facecolor='grey', linestyle='--')
        ax.add_patch(parking_patch)
        parking_patches.append(parking_patch)

    parking_spot_patch = plt.Rectangle(parking_spot[:2], parking_spot[2], parking_spot[3],
                                       edgecolor='blue', facecolor='none', linewidth=2)
    ax.add_patch(parking_spot_patch)

    trajectory_line, = ax.plot([], [], color='green', linestyle='-', label='Car Trajectory')

    ax.set_xlabel('X-position')
    ax.set_ylabel('Y-position')
    ax.set_title('Car Parking Simulation')
    ax.legend()

    ax.set_xlim(-2, 15)
    ax.set_ylim(-2, 15)

    ani = FuncAnimation(fig, update, frames=len(state_trajectory),
                        fargs=(car_patch, parking_spot_patch, state_trajectory, trajectory_line, wheels, trajectory_x, trajectory_y),
                        blit=True, interval=100, repeat=False)

    plt.show()

    gui2.start()