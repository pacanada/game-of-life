from gameoflife import GameOfLife
from pathlib import Path
import numpy as np

initial_state = np.array(
       [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 1, 0],
        [1, 0, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# make sure N and M corresponds to 
game = GameOfLife(N=30, M=30, n_steps=10, initial_state=None)

game.simulate()

game.save_as_gif(filename_path=Path("N_30_M_30_n_steps_10.gif"), fps=1,frames=10)
game.save_as_txt(filename_path=Path("N_30_M_30_n_steps_10.txt"))
# Should be the same as game.states (size 10,10,10)
states = game.load_from_txt(filename_path=Path("N_30_M_30_n_steps_10.txt"), n_steps=10)