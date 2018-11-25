import os
import numpy

class Turing_machine:
    def __init__(self):
        pass

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
            elif "start_state" in line:
                line = line.rstrip()
                self.start_state = list(filter(
                                    None,line.split(":")[1].split(","))
                                    )[0]
            else:
                delta.append(line)
        self.variables.append(self.endsymbol)
        self.delta = self.extra_delta(delta, self.variables)
        print(self.delta)

    def simulate(self, input):
        next_state = self.start_state
        print(self.delta[next_state])
        next_index = 0
        for index, symbol in enumerate(input):
            print(index)
            symbol = input[next_index]
            try:
                action = self.delta[next_state][symbol]
            except:
                print("HALT")
                return
            print(input)
            print(action)
            if not action:
                print("HALT")
                return
            if 'R' in action:
                next_index = index + 1
                if next_index > len(input)-1:
                    input += self.endsymbol
                next_state = action.split('R')[-1]
            else:
                next_index = index - 1
                if next_index < 0:
                    input = self.endsymbol + input
                next_state = action.split('L')[-1]

if __name__ == "__main__":
    tm = Turing_machine()
    tm.get_config("config.txt")
    tm.simulate("aaaaa")
