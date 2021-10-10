import numpy as np
from scipy.signal import convolve2d
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
from typing import Optional
from pathlib import Path
import matplotlib.animation as animation


class GameOfLife:
    def __init__(self, N: int, M: int, n_steps: int, initial_state: np.array = None):
        """
        args:
            N: x dimension, int,
            M: y dimension, int,
            n_steps: number of steps in the simulation
            initial_state: initial state of the game, numpy.array
        """
        self.N = N
        self.M = M
        self.n_steps = n_steps
        self.initial_state = self.get_initial_state(initial_state)
        self.states = np.zeros(shape=(self.n_steps, self.N, self.M))
        self.is_finished = False
        
    @staticmethod
    def compute_sum_neighbours(state: np.array)->np.array:
        """Use scipy.signal.convolve2d for computing the alive neighbours of each cell"""
        kernel_neighbours = np.array([[1,1,1], [1,0,1], [1,1,1]]) 
        return convolve2d(state, kernel_neighbours, mode="same")

    @staticmethod
    def compute_next_state(state: np.array, neighbours=np.array)->np.array:
        """Compute next state based on game-of-life rules."""
        next_state = state.copy()
        #Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        #Any live cell with more than three live neighbours dies, as if by overpopulation.
        mask_rule_1 = ((neighbours < 2) | (neighbours > 3)) & (state==1)
        #Any live cell with two or three live neighbours lives on to the next generation.
        mask_rule_2 = ((neighbours== 2) | (neighbours ==3)) & (state==1)
        #Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        mask_rule_3 = (neighbours ==3) & (state==0)
        
        next_state[mask_rule_1] = 0
        next_state[mask_rule_2] = 1
        next_state[mask_rule_3] = 1
        return next_state

    def get_initial_state(self, initial_state: Optional[np.array]):
        """Return initial_state if defined or random state if not defined"""
        if initial_state is None:
            np.random.seed(0)
            state = np.random.randint(2, size=(self.N,self.M))
        else:
            a,b = initial_state.shape
            if a!=self.N or b!=self.M:
                raise ValueError(f"N or M does not correspond to the shape of initial_state:  {a,b}")
            state = initial_state.copy()
        return state


    def simulate(self):
        """Run the simulation and update self.states with the different iterations"""
        
        state = self.initial_state
        
        for step in range(self.n_steps):
            nei = self.compute_sum_neighbours(state)
            state = self.compute_next_state(state, nei)
            self.states[step,:,:] = state
        self.is_finished = True
        
    def save_as_txt(self, filename_path: Path):
        """Hack, we should add the n_steps in the file for the reshape when loading."""
        if not self.is_finished:
            raise Exception("Simulation is not finished, run: `GameOfLife.simulate()`")
        if str(filename_path)[-3:] != "txt":
            raise ValueError("`filename_path` must contain a filename with `.txt` extension.")
        np.savetxt(fname=filename_path, fmt='%i',X=self.states.reshape(-1, self.states.shape[2]))
        print(f"Simulation sucessfully saved as {filename_path} as a reshaped array. ")
    
    @staticmethod
    def load_from_txt(filename_path: Path, n_steps: int):
        # retrieving data from file.
        loaded_reshaped_states = np.loadtxt(filename_path)
        loaded_original_states = loaded_reshaped_states.reshape(
            n_steps, loaded_reshaped_states.shape[0] //n_steps, loaded_reshaped_states.shape[1])
        return loaded_original_states
  
     
    def save_as_gif(self, filename_path: Path, fps: int, frames:int):
        if not self.is_finished:
            raise Exception("Simulation is not finished, run: `GameOfLife.simulate()`")
        if str(filename_path)[-3:] != "gif":
            raise ValueError("`filename_path` must contain a filename with .gif extension.")
        states = self.states.copy()
        fig = plt.figure( figsize=(15,15) )
        im = imshow(states[0], cmap="Greys")
        
        def animate_func(i):
            if i % fps == 0:
                print( '.', end ='' )

            im.set_array(states[i])
            im.axes.set_title(f"Iteration: {i}")
            return [im]

        anim = animation.FuncAnimation(
                                       fig, 
                                       animate_func, 
                                       frames = frames,
                                       interval = 1000 / fps, # in ms
                                       )
        anim.save(filename_path, fps=fps, writer='Pillow')
        print(f"Simulation sucessfully saved as {filename_path}. ")