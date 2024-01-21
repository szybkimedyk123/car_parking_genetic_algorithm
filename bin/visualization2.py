import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from car import *
from const import *


class MyMainWindow(QMainWindow):
    def __init__(self, state_trajectory, parking_space, parking, trajectory_x, trajectory_y):
        super(MyMainWindow, self).__init__()

        # Inicjalizacja interfejsu użytkownika
        self.init_ui(state_trajectory, parking_space, parking)

    def init_ui(self, state_trajectory, parking_spot, parking):
        # Utwórz główny widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Utwórz obiekt Figure z Matplotlib
        self.figure = Figure()

        # Utwórz Canvas, który będzie używany do rysowania wykresu
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        # Dodaj Canvas bezpośrednio do głównego okna
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.canvas)

        # Utwórz obiekt liniowy
        car_vertices = calc_car_vertices(state_trajectory[0])
        self.car_patch = self.figure.gca().add_patch(
            plt.Polygon(car_vertices, closed=True, edgecolor='black', facecolor='red'))

        f_l = Ellipse((0, 0), 0.5, 0.25, angle=0, fill=True, color='black')
        self.figure.gca().add_patch(f_l)
        f_r = Ellipse((0, 0), 0.5, 0.25, angle=0, fill=True, color='black')
        self.figure.gca().add_patch(f_r)
        b_l = Ellipse((0, 0), 0.5, 0.25, angle=0, fill=True, color='black')
        self.figure.gca().add_patch(b_l)
        b_r = Ellipse((0, 0), 0.5, 0.25, angle=0, fill=True, color='black')
        self.figure.gca().add_patch(b_r)

        wheels = [f_l, f_r, b_l, b_r]

        parking_patches = []
        for spot in parking:
            parking_patch = self.figure.gca().add_patch(
                plt.Rectangle((spot[0], spot[2]), spot[1] - spot[0], spot[3] - spot[2],
                              edgecolor='grey', facecolor='grey', linestyle='--'))
            parking_patches.append(parking_patch)

        self.parking_spot_patch = self.figure.gca().add_patch(
            plt.Rectangle(parking_spot[:2], parking_spot[2], parking_spot[3],
                          edgecolor='blue', facecolor='none', linewidth=2))

        self.trajectory_line, = self.figure.gca().plot([], [], color='green', linestyle='-', label='Car Trajectory')

        self.figure.gca().set_xlabel('X-position')
        self.figure.gca().set_ylabel('Y-position')
        self.figure.gca().set_title('Car Parking Simulation')
        self.figure.gca().legend()

        self.figure.gca().set_xlim(-2, 15)
        self.figure.gca().set_ylim(-2, 15)

        self.ani = FuncAnimation(self.figure, self.update,
                                 frames=len(state_trajectory),
                                 fargs=(wheels, state_trajectory),
                                 blit=True, interval=100, repeat=False)

        # Wyświetl główne okno
        self.show()


    def update(self, frame, wheels, state_trajectory):
        if frame < len(state_trajectory):
            current_state = state_trajectory[frame]
            x, y, delta, theta, v = current_state
            car_vertices = calc_car_vertices(current_state)
            self.car_patch.set_xy(car_vertices)

            r_1 = wheel(theta)
            r_2 = wheel(-theta)

            wheels[0].set_center((x + r_1[0], y + r_1[1]))
            wheels[0].set_angle(np.degrees(theta + delta))

            wheels[1].set_center((x + r_2[0], y - r_2[1]))
            wheels[1].set_angle(np.degrees(theta + delta))

            wheels[2].set_center((x - r_2[0], y + r_2[1]))
            wheels[2].set_angle(np.degrees(theta))

            wheels[3].set_center((x - r_1[0], y - r_1[1]))
            wheels[3].set_angle(np.degrees(theta))

            trajectory_x = [state[0] for state in state_trajectory[:frame + 1]]
            trajectory_y = [state[1] for state in state_trajectory[:frame + 1]]

            self.trajectory_line.set_data(trajectory_x, trajectory_y)

            return [self.car_patch, self.parking_spot_patch, self.trajectory_line] + wheels
        else:
            return [self.car_patch, self.parking_spot_patch, self.trajectory_line] + wheels
