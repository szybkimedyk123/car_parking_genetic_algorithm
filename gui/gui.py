import sys
import os
from PySide2.QtWidgets import *

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

src_dir = os.path.join(parent_dir, 'src')

sys.path.append(src_dir)

import program
#import const

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_options = {"Mutation": None, "Crossover": None, "Selection": None}

        self.setWindowTitle("genetic algorithm")
        self.setGeometry(600, 100, 400, 400)

        self.parameters_box = QGroupBox("Parameters")
        self.label_generations = QLabel("Generations:")
        self.text_edit_generations = QLineEdit()
        self.label_generations_range = QLabel("(1 - 1000)")
        self.label_sequence = QLabel("Lenght of squence:")
        self.text_edit_sequence = QLineEdit()
        self.label_sequence_range = QLabel("(1 - 1000)")
        self.label_population = QLabel("Population:")
        self.text_edit_population = QLineEdit()
        self.label_population_range = QLabel("(1 - 1000)")

        layout = QGridLayout(self.parameters_box)
        layout.addWidget(self.label_generations, 0, 0)
        layout.addWidget(self.text_edit_generations, 0, 1)
        layout.addWidget(self.label_generations_range, 0, 2)
        layout.addWidget(self.label_population, 1, 0)
        layout.addWidget(self.text_edit_population, 1, 1)
        layout.addWidget(self.label_sequence_range, 1, 2)
        layout.addWidget(self.label_sequence, 2, 0)
        layout.addWidget(self.text_edit_sequence, 2, 1)
        layout.addWidget(self.label_population_range, 2, 2)
        self.parameters_box.setLayout(layout)

        self.mutation = self.mutation_group_box("Mutation:")
        self.crossover = self.crossover_group_box("Crossover:")
        self.selection = self.selection_group_box("Selection:")

        self.car = QGroupBox("Car:")
        self.car_yes = QRadioButton("yes")
        self.car_no = QRadioButton("no")
        # self.car_no.toggled.connect(self.on_radio_button_no_toggled)
        # self.car_yes.toggled.connect(self.on_radio_button_yes_toggled)
        car = QHBoxLayout(self.car)
        car.addWidget(self.car_yes)
        car.addWidget(self.car_no)
        self.car.setLayout(layout)
        #
        # self.label_generations = QLabel("Generations:")
        # self.text_edit_generations = QLineEdit()
        # self.label_generations_range = QLabel("(1 - 1000)")
        # self.label_sequence = QLabel("Lenght of squence:")
        # self.text_edit_sequence = QLineEdit()
        # self.label_sequence_range = QLabel("(1 - 1000)")
        # self.label_population = QLabel("Population:")
        # self.text_edit_population = QLineEdit()
        # self.label_population_range = QLabel("(1 - 1000)")
        #
        # layout = QGridLayout(self.car)
        # layout.addWidget(self.label_generations, 0, 0)
        # layout.addWidget(self.text_edit_generations, 0, 1)
        # layout.addWidget(self.label_generations_range, 0, 2)
        # layout.addWidget(self.label_population, 1, 0)
        # layout.addWidget(self.text_edit_population, 1, 1)
        # layout.addWidget(self.label_sequence_range, 1, 2)
        # layout.addWidget(self.label_sequence, 2, 0)
        # layout.addWidget(self.text_edit_sequence, 2, 1)
        # layout.addWidget(self.label_population_range, 2, 2)
        # self.car.setLayout(layout)

        layout = QVBoxLayout(self)
        layout.addWidget(self.parameters_box)
        layout.addWidget(self.mutation)
        layout.addWidget(self.crossover)
        layout.addWidget(self.selection)
        layout.addWidget(self.car)

        self.clear_button = QPushButton("Clear")
        self.start_button = QPushButton("Start")
        self.demo_button = QPushButton("Demo")
        layout.addWidget(self.clear_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.demo_button)

        self.clear_button.clicked.connect(self.on_clear_button_click)
        self.start_button.clicked.connect(self.on_start_button_click)
        self.demo_button.clicked.connect(self.on_demo_button_click)

    # def on_radio_button_no_toggled(self, checked):
    #     if checked:
    #         self.parameters_car.hide()
    #
    # def on_radio_button_yes_toggled(self, checked):
    #     if checked:
    #         self.parameters_car.show()


    def mutation_group_box(self, label):
        group_box = QGroupBox(label)
        radio_button_1 = QRadioButton("jednopunktowa")
        radio_button_2 = QRadioButton("wielopunktowa")
        radio_button_3 = QRadioButton("gaussowska")
        layout = QHBoxLayout(group_box)
        layout.addWidget(radio_button_1)
        layout.addWidget(radio_button_2)
        layout.addWidget(radio_button_3)
        group_box.setLayout(layout)

        radio_button_1.toggled.connect(lambda: self.on_toggle(radio_button_1, label))
        radio_button_2.toggled.connect(lambda: self.on_toggle(radio_button_2, label))
        radio_button_3.toggled.connect(lambda: self.on_toggle(radio_button_3, label))

        return group_box

    def crossover_group_box(self, label):
        group_box = QGroupBox(label)
        radio_button_1 = QRadioButton("jednopunktowa")
        radio_button_2 = QRadioButton("dwupunktowa")
        radio_button_3 = QRadioButton("wielopunktowa")
        layout = QHBoxLayout(group_box)
        layout.addWidget(radio_button_1)
        layout.addWidget(radio_button_2)
        layout.addWidget(radio_button_3)
        group_box.setLayout(layout)

        radio_button_1.toggled.connect(lambda: self.on_toggle(radio_button_1, label))
        radio_button_2.toggled.connect(lambda: self.on_toggle(radio_button_2, label))
        radio_button_3.toggled.connect(lambda: self.on_toggle(radio_button_3, label))

        return group_box

    def selection_group_box(self, label):
        group_box = QGroupBox(label)
        radio_button_1 = QRadioButton("ruletka")
        radio_button_2 = QRadioButton("rankingowa")
        radio_button_3 = QRadioButton("turniejowa")
        layout = QHBoxLayout(group_box)
        layout.addWidget(radio_button_1)
        layout.addWidget(radio_button_2)
        layout.addWidget(radio_button_3)
        group_box.setLayout(layout)

        radio_button_1.toggled.connect(lambda: self.on_toggle(radio_button_1, label))
        radio_button_2.toggled.connect(lambda: self.on_toggle(radio_button_2, label))
        radio_button_3.toggled.connect(lambda: self.on_toggle(radio_button_3, label))

        return group_box

    def on_clear_button_click(self):
        self.clear_radio_buttons(self.mutation)
        self.clear_radio_buttons(self.crossover)
        self.clear_radio_buttons(self.selection)
        self.text_edit_sequence.clear()
        self.text_edit_generations.clear()
        self.text_edit_population.clear()

    def clear_radio_buttons(self, group_box):
        for button in group_box.findChildren(QRadioButton):
            button.setAutoExclusive(False)
            button.setChecked(False)
            button.setAutoExclusive(True)

    def on_toggle(self, button, label):
        if button.isChecked():
            self.selected_options[label[:-1]] = button.text()

    def on_start_button_click(self):
        empty_options = {key: value for key, value in self.selected_options.items() if value is None}
        if empty_options or self.text_edit_sequence.text()=="" or self.text_edit_generations.text()=="" \
            or self.text_edit_population.text()=="":
            QMessageBox.warning(self, 'Warning', 'Nic nie wybrano!')
        else:
            print("Wybrane opcje:", self.selected_options)
            population = self.text_edit_population.text()
            generation = self.text_edit_generations.text()
            sequence = self.text_edit_sequence.text()

            if population.isdigit() and generation.isdigit() and sequence.isdigit():
                setting = [int(generation), int(sequence), int(population)]
                options = []
                for value in self.selected_options.values():
                    options.append(value)
                print(setting)
                self.close()
                program.start(algorith_parameters=setting,options=options)
            else:
                QMessageBox.warning(self, 'Warning', 'Wprowadzone są błędne')

    def on_demo_button_click(self):
        self.close()
        program.start()

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
     main()