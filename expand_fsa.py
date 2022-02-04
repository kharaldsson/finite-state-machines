import sys
import re


class Machine:
    def __init__(self):
        self.initial_state = None
        self.final_states = None
        self.states = set()
        self.vocab = set()
        self.rules = None
        self.lexicon = {}
        self.new_rules = {}
        self.carmel_lines = []

    def from_carmel_format(self, fsa_file):
        with open(fsa_file, 'r', encoding='utf8') as f:
            lines = f.readlines()

        lines = [re.sub('\n|\(|\)', '', x) for x in lines]
        states = set()
        vocab = set()
        rules = {}
        final_states = lines[0]
        initial_state = None
        for line in lines[1:]:
            line = line.strip()
            if line == '':
                continue
            splits = line.split()
            from_state = splits[0]
            to_state = splits[1]
            input_symbol = splits[2]

            if initial_state is None:
                initial_state = from_state

            if from_state not in states:
                states.add(from_state)
            if to_state not in states:
                states.add(to_state)
            if input_symbol not in vocab and not input_symbol == '*e*':
                vocab.add(input_symbol)

            if from_state not in rules:
                rules[from_state] = {}
            if input_symbol not in rules[from_state]:
                rules[from_state][input_symbol] = set()
            rules[from_state][input_symbol].add(to_state)

        self.initial_state = initial_state
        self.final_states = final_states
        self.states = states
        self.vocab = vocab
        self.rules = rules

    def create_lexicon(self, lexicon_list):
        lex_split = [re.split(r"\s+", x) for x in lexicon_list]
        lex_dict = {}
        for i in lex_split:
            word = i[0]
            ling_class = i[1]
            if ling_class not in lex_dict:
                lex_dict[ling_class] = set()
            lex_dict[ling_class].add(word)
        self.lexicon = lex_dict

    def expand(self, lexicon_list):
        self.create_lexicon(lexicon_list)
        for key, val in self.rules.items():
            initial_state = key

            for lex_class, final_states in val.items():
                if lex_class == '*e*' or lex_class not in self.lexicon:
                    if key not in self.new_rules:
                        self.new_rules[key] = {}
                    if lex_class not in self.new_rules[key]:
                        self.new_rules[key][lex_class] = set()
                        if type(to_state) is set:
                            self.new_rules[key][lex_class] = self.new_rules[key][lex_class].union(final_states)
                        else:
                            self.new_rules[key][lex_class].add(final_states)
                else:
                    lex_words = self.lexicon[lex_class]

                    for word in lex_words:
                        letters = list(word)
                        from_state = initial_state
                        for idx, item in enumerate(letters):
                            input_symbol = str('"' + item + '"')

                            if idx < len(letters) - 1:
                                to_state = str(key + letters[idx + 1]) + "_" + str(idx + 1)
                            else:
                                to_state = final_states


                            if from_state not in self.new_rules:
                                self.new_rules[from_state] = {}
                            if input_symbol not in self.new_rules[from_state]:
                                self.new_rules[from_state][input_symbol] = set()

                            if type(to_state) is set:
                                # print(to_state)
                                self.new_rules[from_state][input_symbol] = self.new_rules[from_state][
                                    input_symbol].union(to_state)
                            else:
                                self.new_rules[from_state][input_symbol].add(to_state)
                            from_state = to_state

    def to_carmel_format(self):
        self.carmel_lines.append(self.final_states)
        for from_state, rule in self.new_rules.items():
            for input_value, to_state in rule.items():
                for state in to_state:
                    carmel_line = '(' + from_state + ' (' + state + ' ' + input_value + '))'
                    self.carmel_lines.append(carmel_line)


def process_file(lexicon_path, morph_rules_path, output_fsa_path):
    with open(lexicon_path, 'r', encoding='utf8') as f:
        lexicon_lines = [l for l in (line.strip() for line in f) if l]

    machine = Machine()
    machine.from_carmel_format(morph_rules_path)
    machine.expand(lexicon_lines)
    machine.to_carmel_format()
    with open(output_fsa_path, 'w', encoding='utf8') as f:
        f.writelines("%s\n" % line for line in machine.carmel_lines)


if __name__ == "__main__":
    process_file(sys.argv[1], sys.argv[2], sys.argv[3])


