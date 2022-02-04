#!/opt/python-3.6/bin/python3.6

import sys
import os
import subprocess
import collections
import re


class Machine:
    def __init__(self, initial_state, final_states, states, vocab, rules, output_symbols, is_ambiguous):
        self.initial_state = initial_state
        self.final_states = final_states
        self.states = states
        self.vocab = vocab
        self.rules = rules
        self.output_symbols = output_symbols
        self.is_ambiguous = is_ambiguous


    @classmethod
    def from_carmel_format(cls, fsa_file):
        with open(fsa_file, 'r', encoding='utf8') as f:
            lines = f.readlines()
        lines = [re.sub('\n|\(|\)', '', x) for x in lines]
        #         print(lines)

        final_states = set()
        states = set()
        vocab = set()
        rules = {}
        output_symbols = set()
        is_ambiguous = None

        final_states.add(lines[0].strip())
        initial_state = None
        for line in lines[1:]:
            line = line.strip()
            if line == '':
                continue
            splits = line.split()
            from_state = splits[0]
            to_state = splits[1]
            input_symbol = splits[2]
            output_symbol = splits[3]

            try:
                probability = float(splits[4])
            except:
                probability = 1.0

            if initial_state is None:
                initial_state = from_state

            if from_state not in states:
                states.add(from_state)
            if to_state not in states:
                states.add(to_state)
            if input_symbol not in vocab and not input_symbol == '*e*':
                vocab.add(input_symbol)

            if output_symbol not in output_symbols and not output_symbol == '*e*':
                output_symbols.add(output_symbol)

            if from_state not in rules:
                rules[from_state] = {}

            if input_symbol == '*e*':
                is_ambiguous = True

            if input_symbol in rules[from_state]:
                is_ambiguous = True

            if input_symbol not in rules[from_state]:
                rules[from_state][input_symbol] = list(set())

            rules[from_state][input_symbol].append(to_state)
            rules[from_state][input_symbol].append(output_symbol)
            rules[from_state][input_symbol].append(probability)

        fsa = cls(initial_state, final_states, states, vocab, rules, output_symbols, is_ambiguous)

        return fsa

    @staticmethod
    def rename_set(states):
        return '_'.join(sorted(list(states)))

    def accept_dfa(self, symbol_list):
        current_state = self.initial_state
        output_tape = []
        path_probability = 1
        NO_ACCEPT_TEXT = '*none* 0'
        ACCEPT_TEXT = ''
        epsilon_transition = '*e*'

        if symbol_list[0] == epsilon_transition:
            if self.initial_state in self.final_states:
                return ACCEPT_TEXT
            else:
                return NO_ACCEPT_TEXT

        for symbol in symbol_list:
            if symbol not in self.vocab:
                return NO_ACCEPT_TEXT

            if current_state not in self.rules or symbol not in self.rules[current_state]:
                return NO_ACCEPT_TEXT

            to_states = self.rules[current_state][symbol][0]
            if symbol[1] != epsilon_transition:
                output_tape.append(self.rules[current_state][symbol][1])
            path_probability = path_probability * self.rules[current_state][symbol][2]

            current_state = to_states
        ACCEPT_TEXT = ' '.join(output_tape)
        ACCEPT_TEXT = ACCEPT_TEXT + ' ' + str(path_probability)
        if current_state in self.final_states:
            return ACCEPT_TEXT
        else:
            return NO_ACCEPT_TEXT




def process_file(fst_path, input_path):
    machine = Machine.from_carmel_format(fst_path)

    if machine.is_ambiguous:
        print("The input FST is ambiguous")
    else:
        with open(input_path, 'r', encoding='utf8') as f:
            input_lines = [l for l in (line.strip() for line in f) if l]
            input_lines = [l.split() for l in input_lines]

        for line in input_lines:
            accept = machine.accept_dfa(line)
            print(' '.join(line) + " => " + str(accept))


if __name__ == "__main__":
    TEST = False
    FST_PATH = "examples/fst0"
    INPUT_PATH = "examples/ex"
    if TEST:
        process_file(FST_PATH, INPUT_PATH)
    else:
        process_file(sys.argv[1], sys.argv[2])
