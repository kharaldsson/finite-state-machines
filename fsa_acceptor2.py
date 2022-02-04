#!/opt/python-3.6/bin/python3.6

import sys
import os
import subprocess
import collections
import re


class Machine:
    def __init__(self):
        self.transitions = {}
        self.states2int = {}
        self.final_state = None
        self.fsa = {}
        self.is_nfa = None

    def create(self, fsa_input):
        lines_clean = [re.sub('\n|\(|\)', '', x) for x in fsa_input]
        self.final_state = lines_clean[0]
        lines_clean.pop(0)
        lines_split = [re.split(r"\s", x) for x in lines_clean]

        for line in lines_split:
            if line[0] not in self.transitions:
                self.transitions[line[0]] = {}
            if line[2] == '*e*':
                self.is_nfa = True
            if line[2] in self.transitions[line[0]]:
                self.is_nfa = True
            self.transitions[line[0]][line[2]] = line[1]

        # Convert input states to integer for iteration
        all_states = [key for key in self.transitions.keys()]
        all_states.append(self.final_state)
        all_states = list(dict.fromkeys(all_states)) # Dedupe
        self.states2int = dict(enumerate(all_states))
        self.states2int = {v: k for k, v in self.states2int.items()}
        for line in lines_split:
            if self.states2int[line[0]] not in self.fsa:
                self.fsa[self.states2int[line[0]]] = {}
            self.fsa[self.states2int[line[0]]][line[2]] = self.states2int[line[1]]

        self.final_state = self.states2int[self.final_state]


    def check_acceptance(self, input_tape):
        tape = re.split(r"\s+", input_tape)
        tape_index = 0
        tape_end_index = len(tape) - 1
        current_state_index = 0
        for char in tape:
            if tape_index == tape_end_index:
                try:
                    current_state_index = self.fsa[current_state_index][char]
                    if current_state_index == self.final_state:
                        return "yes"
                    else:
                        return "no"
                except:
                    return "no"
            elif char not in self.fsa[current_state_index]:
                return "no"
            else:
                current_state_index = self.fsa[current_state_index][char]
                tape_index += 1


def process_file(fsa_path, input_path):
    with open(fsa_path, 'r', encoding='utf8') as f:
        fsa_lines = f.readlines()

    machine = Machine()
    machine.create(fsa_lines)

    if machine.is_nfa:
        print("My code cannot handle NFAs")
    else:
        # Import input text
        with open(input_path, 'r', encoding='utf8') as f:
            input_lines = [l for l in (line.strip() for line in f) if l]

        for line in input_lines:
            print(line + " => " + machine.check_acceptance(line))


if __name__ == "__main__":
    process_file(sys.argv[1], sys.argv[2])