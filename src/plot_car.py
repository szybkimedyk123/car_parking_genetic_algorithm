import matplotlib.pyplot as plt
import math
import os


time_values = []
x_values = []
y_values = []
delta_values = []
theta_values = []
v_values = []
a_values = []
psi_values = []


folder_name = os.path.join('..', 'data')
car_name = 'simulation.txt'
file_path_car = os.path.join(folder_name, car_name)

with open(file_path_car, 'r') as file:
    for line in file:
        values = line.strip().split()
        time_values.append(float(values[0]))
        x_values.append(float(values[1]))
        y_values.append(float(values[2]))
        delta_values.append(float(values[3]))
        theta_values.append(float(values[4]))
        v_values.append(float(values[5]))
        a_values.append(float(values[6]))
        psi_values.append(float(values[7]))

fig, axs = plt.subplots(4, figsize=(8, 6))

psi_values_degrees = [math.degrees(rad) for rad in psi_values]
delta_values_degrees = [math.degrees(rad) for rad in delta_values]
theta_values_degrees = [math.degrees(rad) for rad in theta_values]

axs[0].plot(time_values, x_values, label="X", color='blue')
axs[0].set_xlabel(f'czas [s]')
axs[0].set_ylabel(f'położenie X [m]')
axs[0].legend(fontsize=8)
axs[0].grid(True)

axs[1].plot(time_values, y_values, label="Y", color='red')
axs[1].set_xlabel(f'czas [s]')
axs[1].set_ylabel(f'położenie Y [m]')
axs[1].legend(fontsize=8)
axs[1].grid(True)

axs[2].plot(time_values, v_values, label="v", color='green')
axs[2].set_xlabel(f'czas [s]')
axs[2].set_ylabel(r'prędkość [$\frac{m}{s}$]')
axs[2].legend(fontsize=8)
axs[2].grid(True)

axs[3].plot(time_values, a_values, label="a", color='black')
axs[3].set_xlabel(f'czas [s]')
axs[3].set_ylabel(r'przyśpieszenie [$\frac{m}{s^2}$]')
axs[3].legend(fontsize=8)
axs[3].grid(True)

fig2, axs2 = plt.subplots(3, figsize=(8, 6))

axs2[0].plot(time_values, theta_values_degrees, label="theta", color='red')
axs2[0].set_xlabel(f'czas [s]')
axs2[0].set_ylabel(r'kąt theta [$^\circ$]')
axs2[0].legend(fontsize=8)
axs2[0].grid(True)

axs2[1].plot(time_values, delta_values_degrees, label="delta", color='blue')
axs2[1].set_xlabel(f'czas [s]')
axs2[1].set_ylabel(r'kąt delta [$^\circ$]')
axs2[1].legend(fontsize=8)
axs2[1].grid(True)

axs2[2].plot(time_values, psi_values_degrees, label="psi", color='black')
axs2[2].set_xlabel(f'czas [s]')
axs2[2].set_ylabel(f'kąt psi [$^\circ$]')
axs2[2].legend(fontsize=8)
axs2[2].grid(True)

fig.subplots_adjust(hspace=1)
fig.suptitle('Wykres położenia, prędkości i przyśpieszenia')

fig2.subplots_adjust(hspace=1)
fig2.suptitle('Wykres kąta pojazdu, kąta kół i kąta kierującego')

plt.tight_layout()
plt.show()