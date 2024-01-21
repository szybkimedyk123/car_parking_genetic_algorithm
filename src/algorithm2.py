import numpy as np
from car import *



def evolutionary_algorithm(algorith_parameters, options, target_position, parking_spot, parking, start_position):

    mutation_option = options[0]
    crossover_option = options[1]
    selection_option = options[2]

    current_best = None
    best_fitness = float('inf')

    best_solutions_history = []

    speed_values = np.random.uniform(low=-0.2, high=0.5, size=(algorith_parameters[2], algorith_parameters[1], 1))
    angle_values = np.random.uniform(low=-np.pi / 16, high=np.pi / 16, size=(algorith_parameters[2], algorith_parameters[1], 1))

    population = np.concatenate((speed_values, angle_values), axis=2)

    generation = 0
    history = []
    
    while generation < algorith_parameters[0]:
        print(generation + 1)
        best_population = float('inf')
        fitness_scores = []
        for i in range(algorith_parameters[2]):
            actions = population[i]
            state = start_position.copy()

            fitness, trajectory, grade, stop = algorithm_evaluation(state, actions, target_position, parking_spot, parking)
            fitness_scores.append(fitness)

            if fitness < best_population:
                current_best = actions[:trajectory]
                new_row = np.array([[-stop, 0]])
                current_best = np.vstack((current_best, new_row))
                new_row = np.array([[0, 0]])
                current_best = np.vstack((current_best, new_row))
                best_population = fitness
                best_grade = grade

        history.append((generation, best_grade))

        if best_population < best_fitness:
            best_fitness = best_population
            best_solutions_history = [current_best, best_population]

        selected = selection(selection_option, population, fitness_scores, int(algorith_parameters[2] / 2))

        new_population = crossover(crossover_option, selected, int(algorith_parameters[2] / 2), algorith_parameters[1])

        new_population = mutation(mutation_option, new_population, int(algorith_parameters[2] / 2), algorith_parameters[1])

        population = new_population + selected

        generation += 1

    current_best = best_solutions_history[0]

    print(current_best)
    #print(best_fitness)
    return current_best, history


def selection(selection_option, population, fitness_scores, num_selected):

    if selection_option == "roulette":
        pass
    elif selection_option == "ranking":
        after_selection = rank_selection(population, fitness_scores, num_selected)
    elif selection_option == "tournament":
        pass

    return after_selection


def mutation(mutation_option, new_population, population_size, sequence_length):

    if mutation_option == "single-point":
        pass
    elif mutation_option == "multi-point":
        pass
    elif mutation_option == "gaussian":
        after_mutation = mutation_gaussian(new_population, population_size, sequence_length)

    return after_mutation


def crossover(crossover_option, population, population_size, sequence_length):

    if crossover_option == "single-point":
        after_crossover = crossover_single(population, population_size, sequence_length)
    elif crossover_option == "two-point":
        pass
    elif crossover_option == "multi-point":
        pass

    return after_crossover


def roulette_wheel_selection(population, fitness_scores, num_selected):
    total_fitness = sum(fitness_scores)
    probabilities = [fitness / total_fitness for fitness in fitness_scores]

    selected_indices = np.random.choice(range(len(population)), size=num_selected, p=probabilities, replace=False)
    selected_individuals = [population[i] for i in selected_indices]

    return selected_individuals

def rank_selection(population, fitness_scores, num_selected):
    ranked_indices = np.argsort(fitness_scores)
    ranks = np.arange(len(population), 0, -1)

    probabilities = ranks / sum(ranks)

    selected_indices = np.random.choice(ranked_indices, size=num_selected, p=probabilities, replace=False)
    selected_individuals = [population[i] for i in selected_indices]

    return selected_individuals

def crossover_single(population, population_size, sequence_length):

    crossover_probability = 0.8
    new_population = []

    for i in range(population_size):
        if np.random.rand() < crossover_probability:
            parent1 = population[np.random.randint(0, population_size)]
            parent2 = population[np.random.randint(0, population_size)]
            crossover_point = np.random.randint(1, sequence_length)
            child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            new_population.append(child)
        else:
            parent = population[np.random.randint(0, population_size)]
            new_population.append(parent.copy())


    return new_population

def mutation_gaussian(new_population, population_size, sequence_length):

    mutation_probability = 0.2

    for i in range(population_size):
        if np.random.rand() < mutation_probability:
            mutation_rate = 0.2
            mutation_rand = np.random.normal(0, mutation_rate, (sequence_length, 2))
            mutated_population = new_population[i] + mutation_rand

            mutated_population[:, 0] = np.clip(mutated_population[:, 0], -0.2, 0.5)
            mutated_population[:, 1] = np.clip(mutated_population[:, 1], -np.pi / 16, np.pi / 16)

            new_population[i] = mutated_population

    return new_population


def algorithm_evaluation(state, actions, target_position, parking_spot, parking):

    penalty = 0
    distance = 0
    time = 0
    position = [0, 0]

    for u in actions:
        time += 1
        state = kinematic_model(state, u)
        car_vertices = calc_car_vertices(state)

        x_diff = position[0] - state[0]
        y_diff = position[1] - state[1]
        distance += np.sqrt(x_diff ** 2 + y_diff ** 2)

        position[0] = state[0]
        position[1] = state[1]

        for spot in parking:
            vertices_inside_spot = ((spot[0] <= car_vertices[:, 0]) & (car_vertices[:, 0] <= spot[1]) &
                                    (spot[2] <= car_vertices[:, 1]) & (car_vertices[:, 1] <= spot[3]))
            vertices_count = np.sum(vertices_inside_spot)

            if vertices_count > 0:
                penalty += 100 * vertices_count

        if (
                (parking_spot[0] <= car_vertices[:, 0]).all() and (
                car_vertices[:, 0] <= parking_spot[0] + parking_spot[2]).all()
                and (parking_spot[1] <= car_vertices[:, 1]).all() and (
                car_vertices[:, 1] <= parking_spot[1] + parking_spot[3]).all()
                # and np.linalg.norm(z[:2] - target_position) < 1
        ):
            stop = state[4]
            break

        else:
            stop = state[4]


    d_centre = np.sqrt((position[0] - target_position[0]) ** 2 + (position[1] - target_position[1]) ** 2)
    angle = state[3]

    if angle > np.pi:
        angle = np.pi - (angle - np.pi)

    o = 0.5 * d_centre + distance + time / 10 + 0.5 * abs(90 - abs(np.degrees(angle))) + penalty

    # print("distance from center = " + str(d_centre))
    # print("distance = " + str(distance))
    # print("time = " + str(len(best_generation)))
    # print("angle = " + str(90 - np.degrees(abs(angle))))
    # print("algorithm evaluation = " + str(o))

    rate = [o, d_centre, distance, time, abs(90 - abs(np.degrees(angle)))]

    return o, time, rate, stop

