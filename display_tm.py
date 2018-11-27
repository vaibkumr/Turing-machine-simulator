import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import colors
import numpy as np
import time
style.use('dark_background')
class Display_tm():
    def __init__(self, filename, colors=['pink', 'purple']):
        self.time_flag = True
        self.start_time = time.time()
        self.time = 0
        self.fn = filename
        self.colors = colors
        self.fig, self.ax = plt.subplots()
        self.show()

    def show(self):
        # plt.text(5,5,
        #          "Turing Machine Simulator | By TimeTraveller",
        #          size="xx-large")
        label = "Turing Machine Simulator\nBy TimeTraveller"
        plt.title(label, fontdict=None, loc='center', pad=70, size=12)
        an1 = animation.FuncAnimation(self.fig, self.animate, interval=1)
        plt.show()

    def read_tape(self):
        with open(self.fn,'r') as handle:
            lines = handle.readlines()
        color_code_array = [[
                            0 for x in range(len(lines[1]) - 1)
                            ]]
        color_code_array[0][int(lines[0])] = 1
        return color_code_array, lines[1], lines[2].strip(), lines[3], lines[4]

    def flush_chars(self):
        try:
            self.runtime_text.remove()
            self.status_t.remove()
            self.speed_text.remove()
            self.state_t.remove()
            for t in self.chars:
                t.remove()
        except:
            return

    def runtime(self):
        if self.time_flag:
            return str(round(time.time() - self.start_time))
        return self.saved_time

    def animate(self, i):
        color_code_array, tape_string, status, cur_state, speed = self.read_tape()
        cmap = colors.ListedColormap(self.colors)
        norm = colors.BoundaryNorm([0,1,1], ncolors=cmap.N)
        fig, ax = self.fig, self.ax
        ax.imshow(color_code_array, cmap=cmap, norm=norm)
        ax.grid(which='major', axis='both',
                linestyle='-', color='white', linewidth=1
                )
        ax.set_xticks([ -0.5 + i for i in range(
                                                len(color_code_array[0])
                                                )])
        #Remove xy ticks
        ax.set_xticklabels([])
        ax.set_yticks([]);

        #Flush previous text
        self.flush_chars()

        #Update text
        posx = -0.5
        posy = -0.5
        if str(status) != "RUNNING":
            self.saved_time = self.runtime()
            self.time_flag = False
        #Show machine status
        self.status_t = plt.text(posx, posy, f"State: {cur_state}\n")
        #Runtime
        self.runtime_text = plt.text(-0.5, 1, f"Runtime: {self.runtime()}s\n")
        self.speed_text = plt.text(-0.5, 1, f"Speed: {speed}")
        #Show current state
        self.state_t = plt.text(posx, posy, f"Status: {status}\n")
        self.chars = []
        for index, var in enumerate(tape_string):
            self.chars.append(plt.text(index, 0.1, var, color = 'k'))
