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
        print("current generation: " + str(generation + 1))
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

    # print(current_best)
    #print(best_fitness)
    return current_best, history


def selection(selection_option, population, fitness_scores, num_selected):
    if selection_option == "roulette":
        after_selection = roulette_wheel_selection(population, fitness_scores, num_selected)
    elif selection_option == "ranking":
        after_selection = rank_selection(population, fitness_scores, num_selected)
    elif selection_option == "tournament":
        after_selection = tournament_selection(population, fitness_scores, num_selected)

    return after_selection


def tournament_selection(population, fitness_scores, num_selected):
    selected_individuals = []
    tournament_size_percentage = 0.2
    tournament_size = int(len(population) * tournament_size_percentage)

    for _ in range(num_selected):
        tournament_indices = np.random.choice(len(population), size=tournament_size, replace=False)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]

        winner_index = tournament_indices[np.argmax(tournament_fitness)]
        selected_individuals.append(population[winner_index])

    return selected_individuals


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


def mutation(mutation_option, new_population, population_size, sequence_length):
    if mutation_option == "single-point":
        after_mutation = mutation_single(new_population, population_size, sequence_length)
    elif mutation_option == "multi-point":
        after_mutation = mutation_multi(new_population, population_size, sequence_length)
    elif mutation_option == "gaussian":
        after_mutation = mutation_gaussian(new_population, population_size, sequence_length)

    return after_mutation


def mutation_multi(new_population, population_size, sequence_length):
    mutation_probability = 0.2
    min_num_mutation_points = 2
    max_num_mutation_points = 5

    for i in range(population_size):
        if np.random.rand() < mutation_probability:
            mutation_rate = 0.2

            num_mutation_points = np.random.randint(min_num_mutation_points, max_num_mutation_points + 1)

            mutation_points = np.random.choice(sequence_length, size=num_mutation_points, replace=False)
            mutation_values = np.random.normal(0, mutation_rate, (num_mutation_points, 2))

            new_population[i][mutation_points, :] += mutation_values

            new_population[i][:, 0] = np.clip(new_population[i][:, 0], -0.2, 0.5)
            new_population[i][:, 1] = np.clip(new_population[i][:, 1], -np.pi / 16, np.pi / 16)

    return new_population


def mutation_single(new_population, population_size, sequence_length):
    mutation_probability = 0.2

    for i in range(population_size):
        if np.random.rand() < mutation_probability:
            mutation_rate = 0.2
            mutation_point = np.random.randint(0, sequence_length)
            mutation_value = np.random.normal(0, mutation_rate, 2)

            new_population[i][mutation_point, :] += mutation_value

            new_population[i][:, 0] = np.clip(new_population[i][:, 0], -0.2, 0.5)
            new_population[i][:, 1] = np.clip(new_population[i][:, 1], -np.pi / 16, np.pi / 16)

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


def crossover(crossover_option, population, population_size, sequence_length):
    if crossover_option == "single-point":
        after_crossover = crossover_single(population, population_size, sequence_length)
    elif crossover_option == "two-point":
        after_crossover = crossover_two(population, population_size, sequence_length)
    elif crossover_option == "multi-point":
        after_crossover = crossover_multi(population, population_size, sequence_length)

    return after_crossover


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


def crossover_two(population, population_size, sequence_length):
    crossover_probability = 0.8
    new_population = []

    for i in range(population_size):
        if np.random.rand() < crossover_probability:
            parent1 = population[np.random.randint(0, population_size)]
            parent2 = population[np.random.randint(0, population_size)]

            crossover_points = sorted(np.random.choice(sequence_length, size=2, replace=False))

            child = np.concatenate((parent1[:crossover_points[0]],
                                    parent2[crossover_points[0]:crossover_points[1]],
                                    parent1[crossover_points[1]:]))
            new_population.append(child)
        else:
            parent = population[np.random.randint(0, population_size)]
            new_population.append(parent.copy())

    return new_population


def crossover_multi(population, population_size, sequence_length):
    crossover_probability = 0.8
    min_num_crossover_points = 3
    max_num_crossover_points = 5
    new_population = []

    for i in range(population_size):
        if np.random.rand() < crossover_probability:
            parent1 = population[np.random.randint(0, population_size)]
            parent2 = population[np.random.randint(0, population_size)]

            num_crossover_points = np.random.randint(min_num_crossover_points, max_num_crossover_points + 1)
            crossover_points = sorted(np.random.choice(sequence_length, size=num_crossover_points, replace=False))

            child_parts = []
            current_parent = parent1

            for j in range(num_crossover_points + 1):
                start = 0 if j == 0 else crossover_points[j - 1]
                end = crossover_points[j] if j < num_crossover_points else sequence_length
                child_parts.append(current_parent[start:end])
                current_parent = parent2 if current_parent is parent1 else parent1

            child = np.concatenate(child_parts)
            new_population.append(child)
        else:
            parent = population[np.random.randint(0, population_size)]
            new_population.append(parent.copy())

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

