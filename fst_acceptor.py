import sys
import subprocess
import re


def carmelize(fst_path, input_path):
    with open(input_path, 'r', encoding='utf8') as f:
        input_text = f.read()

    carmel_args = ['carmel', '-b', '-sli', fst_path]
    epsilon = '*e*'

    p1 = subprocess.Popen(carmel_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p1_out = p1.communicate(input=input_text.encode())[0]
    p1_out = p1_out.decode().strip()
    p1_list = re.split(r"\n", p1_out)
    probabilities = []
    all_results = []
    for line in p1_list:
        if line == '0':
            all_results.append('*none*')
            probabilities.append('0')
        else:
            probabilities.append(line.rsplit(" ", 1)[1])
            transitions = re.split(r"\)\s\(", line)
            transitions = [re.findall(r"\:\s(.*?)\s\/", x)[0] for x in transitions]
            if epsilon in transitions:
                transitions.remove(epsilon)
            transitions = " ".join(transitions)

            all_results.append(transitions)

    input_list = re.split(r"\n", input_text)

    for i, o, p in zip(input_list, all_results, probabilities):
        print(i + " => " + o + " " + p)


if __name__ == "__main__":
    carmelize(sys.argv[1], sys.argv[2])
