import numpy as np

#constants

#car
CAR_X = 0
CAR_Y = 0
car_length = 4.0
car_width = 1.8
L = 2.5
lr = L / 2
d = 1.2
dl = d / 2
car_parameters = [car_length, car_width, L, lr, d, dl]
state = np.array([CAR_X, CAR_X, 0, 0, 0])

#steering
A = 0.5
V = 2
DELTA = 45
dt = 0.1

steering = [A, V, DELTA, dt]

#wheels
# wheel_height =
# wheel_width =
# wheel_parameters =


#parking space const
PARKING_SPACE_X = 8
PARKING_SPACE_Y = 8
PARKING_SPACE_LENGTH = 4
PARKING_SPACE_WIDTH = 6

#target position
target_position = np.array(
    [(PARKING_SPACE_X + PARKING_SPACE_LENGTH / 2),
     (PARKING_SPACE_Y + PARKING_SPACE_WIDTH / 2)])

parking_space = np.array(
    [PARKING_SPACE_X, PARKING_SPACE_Y,
     PARKING_SPACE_LENGTH, PARKING_SPACE_WIDTH])


#parking const
PARKING_X_MIN = -8
PARKING_X_MAX = 20
PARKING_Y_MIN = 0
PARKING_Y_MAX = 20

#parking
parking = [
    [PARKING_X_MIN, PARKING_SPACE_X, PARKING_SPACE_Y, PARKING_Y_MAX],
    [PARKING_SPACE_X, PARKING_SPACE_Y + PARKING_SPACE_LENGTH, PARKING_SPACE_Y + PARKING_SPACE_WIDTH, PARKING_Y_MAX],
    [PARKING_SPACE_Y + PARKING_SPACE_LENGTH, PARKING_Y_MAX, PARKING_SPACE_Y, PARKING_Y_MAX]
    ]

# #algorithm
# GENERATIONS = 1
# MAX_LENGTH = 200
# POPULATION = 300
#
# algorithm_parameters = [GENERATIONS, MAX_LENGTH, POPULATION]