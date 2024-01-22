import numpy as np
from const import *


def kinematic_model(z, u):
    x, y, delta, theta, v = z
    a, phi = u

    max_velocity = steering[1]
    max_angle = steering[2]

    v += a
    delta += phi

    v_dot = np.clip(v, -max_velocity, max_velocity)
    delta = np.clip(delta, -max_angle, max_angle)

    beta = np.arctan(car_parameters[3] * delta / car_parameters[2])

    x_dot = v_dot * np.cos(theta + beta)
    y_dot = v_dot * np.sin(theta + beta)
    theta_dot = v_dot * np.tan(delta) * np.cos(beta) / car_parameters[2]

    x_next = x + x_dot * steering[3]
    y_next = y + y_dot * steering[3]
    theta_next = theta + theta_dot * steering[3]

    return np.array([x_next, y_next, delta, theta_next, v_dot])


def calc_car_vertices(z):
    x, y, _, theta, _ = z
    car_half_length = car_parameters[0] / 2
    car_half_width = car_parameters[1] / 2
    car_vertices = np.array([
        [x - car_half_length * np.cos(theta) - car_half_width * np.sin(theta),
         y - car_half_length * np.sin(theta) + car_half_width * np.cos(theta)],
        [x + car_half_length * np.cos(theta) - car_half_width * np.sin(theta),
         y + car_half_length * np.sin(theta) + car_half_width * np.cos(theta)],
        [x + car_half_length * np.cos(theta) + car_half_width * np.sin(theta),
         y + car_half_length * np.sin(theta) - car_half_width * np.cos(theta)],
        [x - car_half_length * np.cos(theta) + car_half_width * np.sin(theta),
         y - car_half_length * np.sin(theta) - car_half_width * np.cos(theta)],
    ])

    return car_vertices

def wheel(theta):
    #x, y, delta, theta, v = z

    half = car_parameters[5]
    rear_wheel_distance = car_parameters[3]
    r = np.sqrt(half ** 2 + rear_wheel_distance ** 2)

    wheel_distance = np.array([
        r * np.cos(half/rear_wheel_distance + theta),
        r * np.sin(half/rear_wheel_distance + theta)
    ])

    return wheel_distance