from car import *
import tkinter as tk
import program

class GenerationCounter(tk.Tk):
    def __init__(self, algorith_parameters, target_position, parking_spot, parking, start_position):
        super().__init__()

        self.title("Current generation")
        self.geometry("150x100")

        self.number = 0

        self.label_text = tk.StringVar()
        self.label_text.set(f"Generation: {self.number}")

        self.label = tk.Label(self, textvariable=self.label_text, font=("Arial", 16))
        self.label.pack(pady=20)

        self.evolutionary_algorithm(algorith_parameters, target_position, parking_spot, parking, start_position)

    def update_gen(self):
        self.number += 1
        self.label_text.set(f"Generation: {self.number}")

    def end_count(self, current_best, history):
        self.destroy()
        program.save_best(current_best, history)



    def evolutionary_algorithm(self, algorith_parameters, target_position, parking_spot, parking, start_position):
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
            self.update_gen()

            best_population = float('inf')
            fitness_scores = []
            for i in range(algorith_parameters[2]):
                actions = population[i]
                state = start_position.copy()

                fitness, trajectory, grade, stop = self.algorithm_evaluation(state, actions, target_position, parking_spot, parking)
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

            #selected = roulette_wheel_selection(population, fitness_scores, int(population_size / 2))
            selected = self.rank_selection(population, fitness_scores, int(algorith_parameters[2] / 2))

            new_population = self.crossover(selected, int(algorith_parameters[2] / 2), algorith_parameters[1])

            new_population = self.mutation(new_population, int(algorith_parameters[2] / 2), algorith_parameters[1])

            population = new_population + selected

            generation += 1

        current_best = best_solutions_history[0]

        print(current_best)
        #print(best_fitness)
        #return current_best, history

        self.end_count(current_best, history)

    def roulette_wheel_selection(self, population, fitness_scores, num_selected):
        total_fitness = sum(fitness_scores)
        probabilities = [fitness / total_fitness for fitness in fitness_scores]

        selected_indices = np.random.choice(range(len(population)), size=num_selected, p=probabilities, replace=False)
        selected_individuals = [population[i] for i in selected_indices]

        return selected_individuals

    def rank_selection(self, population, fitness_scores, num_selected):
        ranked_indices = np.argsort(fitness_scores)
        ranks = np.arange(len(population), 0, -1)

        probabilities = ranks / sum(ranks)

        selected_indices = np.random.choice(ranked_indices, size=num_selected, p=probabilities, replace=False)
        selected_individuals = [population[i] for i in selected_indices]

        return selected_individuals

    def crossover(self, population, population_size, sequence_length):

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

    def mutation(self, new_population, population_size, sequence_length):

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


    def algorithm_evaluation(self, state, actions, target_position, parking_spot, parking):

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

        # print("odległość = " + str(d_centre))
        # print("droga = " + str(distance))
        # print("czas = " + str(len(best_generation)))
        # print("kąt = " + str(90 - np.degrees(abs(angle))))
        # print("ocena = " + str(ocena))

        rate = [o, d_centre, distance, time, abs(90 - abs(np.degrees(angle)))]

        return o, time, rate, stop

