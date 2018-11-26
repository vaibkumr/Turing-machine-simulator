import os
import numpy
import time
from display_tm import Display_tm
from threading import Thread
import multiprocessing

def is_comment(line):
    if line[0] == "#":
        return True
    return False

class Turing_machine:
    def __init__(self, tape_file, colors=['pink', 'purple'], speed = 0.1 ):
        self.tape_file = tape_file
        self.speed = speed
        self.colors = colors

    def extra_delta(self, lines, variables):
        lines = list(filter(None,lines))
        if "delta" not in lines[0]:
            print("Invalid delta")
            return 0
        lines = lines[1:]
        delta = {}
        for line in lines:
            key = line.split(":")[0]
            values = dict(zip(
                            variables, line.split(":")[1].split()
                            ))
            delta[key] = values
        return delta

    def get_config(self, filename):
        with open(filename, 'r') as handle:
            config = handle.readlines()
        delta = []
        for line in config:
            if "states" in line:
                line = line.rstrip()
                self.states = list(filter(
                                    None,line.split(":")[1].split(","))
                                    )
            elif "variables" in line:
                line = line.rstrip()
                self.variables = list(filter(
                                    None,line.split(":")[1].split(","))
                                    )
            elif "endsymbol" in line:
                line = line.rstrip()
                self.endsymbol = list(filter(
                                    None,line.split(":")[1].split(",")
                                    ))[0]
            elif "final_state" in line:
                line = line.rstrip()
                self.final_state = list(filter(
                                    None,line.split(":")[1].split(",")
                                    ))[0]
            elif "start_state" in line:
                line = line.rstrip()
                self.start_state = list(filter(
                                    None,line.split(":")[1].split(","))
                                    )[0]
            elif not is_comment(line):
                delta.append(line)
        self.variables.append(self.endsymbol)
        self.delta = self.extra_delta(delta, self.variables)
        print(self.delta)

    def write_tape(self, cur_cell, tape_string, next_state, halted = False):
        if halted and self.isFinal(next_state):
            status = "ACCEPTED"
        elif halted:
            status = "REJECTED"
        else:
            status = "RUNNING"
        with open(self.tape_file, 'w+') as handle:
            handle.write(str(cur_cell) + "\n"
                         + tape_string + "\n"
                         + status + "\n"
                         + str(next_state) + "\n"
                         + str(self.speed))

    def isFinal(self, state):
        if state == self.final_state:
            return True
        return False

    def display(self):
        d = Display_tm(self.tape_file, colors=self.colors)

    def run(self, input):
        multiprocessing
        # simulate = Thread(target=self.simulate, args=(input,))
        # display = Thread(target=self.display)
        simulate = multiprocessing.Process(target=self.simulate, args=(input,))
        display = multiprocessing.Process(target=self.display)
        display.start()
        simulate.start()

    def get_action(self, action, input, index):
        if not action:
            return False
        if 'R' in action:
            next_index = index + 1
            if next_index > len(input)-1:
                input += self.endsymbol
            next_state = action.split('R')[-1]
            input = input[:index] + action.split('R')[0] + input[(index+1):]
        else:
            next_index = index - 1
            if next_index < 0:
                input = self.endsymbol + input
            next_state = action.split('L')[-1]
            input = input[:index] + action.split('L')[0] + input[(index+1):]
        return next_index, input, next_state

    def simulate(self, input):
        if input[-1] != self.endsymbol:
            input += self.endsymbol
        next_state = self.start_state
        next_index = 0
        status = "Running"
        for index, symbol in enumerate(input):
            self.write_tape(index, input, next_state)
            symbol = input[next_index]
            try:
                action = self.delta[next_state][symbol]
            except:
                self.write_tape(index, input, next_state, halted=True)
                return
            print(f"String: {input}")
            print(f"Action: {action}")
            next_action = self.get_action(action, input, index)
            next_index, input, next_state = next_action
            time.sleep(self.speed)
        self.write_tape(index, input, next_state, halted=True)

if __name__ == "__main__":
    tm = Turing_machine("tape.txt",colors=['pink', 'red'], speed = 0.1)
    tm.get_config("config.txt")
    # tm.run("aaa") #This should get accepted
    # tm.run("cacacac") #This should get accepted
    tm.run("aaabaabbaaacabbsss") #This should get rejected
