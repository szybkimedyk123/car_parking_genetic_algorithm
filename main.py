import os
import sys

folder_name = os.path.abspath('gui')
sys.path.append(folder_name)

import gui2 as gui


if __name__ == "__main__":
    gui.main()