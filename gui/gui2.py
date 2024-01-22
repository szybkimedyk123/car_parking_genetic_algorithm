import tkinter as tk
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

src_dir = os.path.join(parent_dir, 'src')

sys.path.append(src_dir)

import plot_alg
import plot_car


class MyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - 300) // 2
        y = (screen_height - 100) // 2

        self.title("Plots")
        self.geometry("300x100+{}+{}".format(x, y))

        self.car_button = tk.Button(self, text="Car Parameters", command=self.car_button_clicked)
        self.car_button.pack(pady=10)

        self.evaluation_button = tk.Button(self, text="Algorithm Evaluation", command=self.evaluation_button_clicked)
        self.evaluation_button.pack(pady=10)

        script_directory = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_directory)

    def car_button_clicked(self):
        plot_car.start()

    def evaluation_button_clicked(self):
        plot_alg.start()

def start():
    my_gui = MyGUI()
    my_gui.mainloop()

if __name__ == "__main__":
    my_gui = MyGUI()
    my_gui.mainloop()