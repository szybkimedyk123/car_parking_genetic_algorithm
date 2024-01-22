# Car Parking Genetic Algorithm
This repository contains a python implementation of automatic vehicle parking based on genetic algorithms modified by user.
The project utilizes the following libraries: Matplotlib, NumPy, and Tkinter.

## Gui

Users have the ability to input the number of generations, population size, and sequence length. 
Additionally, they can choose the type of mutation, crossover, and selection methods. 
Demo is simply a demonstration of the working algorithm using standard parameters.

![gui.png](img%2Fgui.png)

Then an animation will be displayed. 
After closing the animation, a second GUI will appear, for displaying graphs.

![gui2.png](img%2Fgui2.png)

Car parameters chart displays Position, Velocity, Acceleration, Vehicle Angle, Wheel Angle Steering Angle.
Algorithm evaluation chart displays Final Evaluation Value and individual assessments of Time, Path, Place and Parking at each step of the algorithm.

## Car model
**The kinematic model** of the car is reduced to a bicycle model based on [Modern Robotics](https://www.google.com/books?hl=pl&lr=&id=5NzFDgAAQBAJ&oi=fnd&pg=PR11&dq=Modern+Robotics:+Mechanics,+Planning,+and+Control.+Cambridge+University&ots=qsIj_Zo1Ok&sig=6JGaOpg92ovUrMC5EKNKVRw8mQo):

```math
\begin{cases}
\dot{x} = v \cdot \cos(\psi + \beta) \
\dot{y} = v \cdot \sin(\psi + \beta) \
\cot{\delta} = \delta
\dot{\theta} = \frac{v \cdot \tan(\delta) \cdot \cos(\beta)}{L} \
\dot{v} = a \
\beta = \arctan\left(\frac{l_r \cdot \tan(\delta)}{L}\right)
\end{cases}
```
```a: acceleration, δ: steering angle, θ: yaw angle, L: wheelbase, x: x-position, y: y-position, v: velocity β: correction angle, l_r: distance between the rear axle and the center```

**The state vector** is:
```math
z=[x,y,δ,θ,v]
```
```x: x-position, y: y-position, v: velocity, θ: yaw angle, δ: current steering angle```

**The input vector** is:
```math
u=[a, φ]
```
```a: acceleration, φ: modify steering angle```

**Algorithm evaluation** is based on:
```math
O = 0.5 \cdot O_c \cdot O_d \cdot \frac{O_t}{10} \cdot 0.5 \cdot O_a + P
```
```O: overall evaluation, O_d: distance, O_c: distance from the center of the parking space, O_t: time, O_a: vertical angle difference, P: penalty```

## Simulation

![animation.gif](img%2Fanimation.gif)

## Future Development Plans:

1. Parallel Parking
2. Obstacle avoidance





