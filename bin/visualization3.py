import tkinter as tk
from tkinter import messagebox
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

src_dir = os.path.join(parent_dir, 'src')

sys.path.append(src_dir)

import program


class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.selected_options = {"Mutation": None, "Crossover": None, "Selection": None}

        self.title("Genetic Algorithm")
        self.geometry("500x500")

        self.parameters_box = tk.LabelFrame(self, text="Parameters")
        self.label_generations = tk.Label(self.parameters_box, text="Generations:")
        self.text_edit_generations = tk.Entry(self.parameters_box)
        self.label_generations_range = tk.Label(self.parameters_box, text="(1 - 1000)")
        self.label_population = tk.Label(self.parameters_box, text="Population:")
        self.text_edit_population = tk.Entry(self.parameters_box)
        self.label_population_range = tk.Label(self.parameters_box, text="(1 - 1000)")
        self.label_sequence = tk.Label(self.parameters_box, text="Length of sequence:")
        self.text_edit_sequence = tk.Entry(self.parameters_box)
        self.label_sequence_range = tk.Label(self.parameters_box, text="(1 - 1000)")

        self.label_generations.grid(row=0, column=0)
        self.text_edit_generations.grid(row=0, column=1)
        self.label_generations_range.grid(row=0, column=2)
        self.label_population.grid(row=1, column=0)
        self.text_edit_population.grid(row=1, column=1)
        self.label_sequence_range.grid(row=1, column=2)
        self.label_sequence.grid(row=2, column=0)
        self.text_edit_sequence.grid(row=2, column=1)
        self.label_population_range.grid(row=2, column=2)
        self.parameters_box.pack(pady=10)

        # Używamy jednej instancji StringVar na poziomie klasy
        self.var_mutation = tk.StringVar()
        self.var_crossover = tk.StringVar()
        self.var_selection = tk.StringVar()

        self.mutation = self.create_radio_buttons("Mutation:", ["jednopunktowa", "wielopunktowa", "gaussowska"],
                                                  self.var_mutation)
        self.crossover = self.create_radio_buttons("Crossover:", ["jednopunktowa", "dwupunktowa", "wielopunktowa"],
                                                   self.var_crossover)
        self.selection = self.create_radio_buttons("Selection:", ["ruletka", "rankingowa", "turniejowa"],
                                                   self.var_selection)

        self.car = tk.LabelFrame(self, text="Car:")
        self.car_var = tk.StringVar()
        self.car_yes = tk.Radiobutton(self.car, text="yes", variable=self.car_var, value="yes")
        self.car_no = tk.Radiobutton(self.car, text="no", variable=self.car_var, value="no")
        self.car_yes.grid(row=0, column=0)
        self.car_no.grid(row=0, column=1)
        self.car.pack(pady=10)

        self.options = tk.LabelFrame(self, text="")
        self.clear_button = tk.Button(self.options, text="Clear", command=self.on_clear_button_click)
        self.start_button = tk.Button(self.options, text="Start", command=self.on_start_button_click)
        self.demo_button = tk.Button(self.options, text="Demo", command=self.on_demo_button_click)

        self.options.pack(pady=10)

        self.clear_button.pack(side=tk.LEFT)
        self.start_button.pack(side=tk.LEFT)
        self.demo_button.pack(side=tk.LEFT)

    def create_radio_buttons(self, label, options, var):
        group_box = tk.LabelFrame(self, text=label)
        for option in options:
            radio_button = tk.Radiobutton(group_box, text=option, variable=var, value=option, indicatoron=False)
            radio_button.pack(side=tk.LEFT)
        group_box.pack(pady=10)
        return group_box

    def on_clear_button_click(self):
        self.clear_radio_buttons(self.mutation, self.var_mutation)
        self.clear_radio_buttons(self.crossover, self.var_crossover)
        self.clear_radio_buttons(self.selection, self.var_selection)
        self.text_edit_sequence.delete(0, tk.END)
        self.text_edit_generations.delete(0, tk.END)
        self.text_edit_population.delete(0, tk.END)

    def clear_radio_buttons(self, group_box, var):
        var.set("")  # Deselect wszystkie przyciski
        for child in group_box.winfo_children():
            if isinstance(child, tk.Radiobutton):
                child.deselect()

    def on_start_button_click(self):
        # Ustawianie wybranych opcji
        self.selected_options["Mutation"] = self.var_mutation.get()
        self.selected_options["Crossover"] = self.var_crossover.get()
        self.selected_options["Selection"] = self.var_selection.get()

        empty_options = {key: value for key, value in self.selected_options.items() if not value}
        if empty_options or self.text_edit_sequence.get() == "" or self.text_edit_generations.get() == "" \
                or self.text_edit_population.get() == "":
            messagebox.showwarning("Warning", "Nothing selected!")
        else:
            print("Selected options:", self.selected_options)
            population = self.text_edit_population.get()
            generation = self.text_edit_generations.get()
            sequence = self.text_edit_sequence.get()

            if population.isdigit() and generation.isdigit() and sequence.isdigit():
                setting = [int(generation), int(sequence), int(population)]
                options = [value for value in self.selected_options.values()]
                print(setting)
                self.destroy()
                program.start(algorithm_parameters=setting, options=options)
            else:
                messagebox.showwarning("Warning", "Invalid input")

    def on_demo_button_click(self):
        self.destroy()
        gen = 10
        max_len = 200
        pop = 300
        algorithm_parameters = [gen, max_len, pop]
        program.start(algorithm_parameters=algorithm_parameters, options=algorithm_parameters)


if __name__ == "__main__":
    window = MyWindow()
    window.mainloop()
