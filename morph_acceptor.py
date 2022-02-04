import sys
import os
import subprocess
from subprocess import PIPE
import re


def carmelize_fst(fst_path, input_path, output_path):
    with open(input_path, 'r', encoding='utf8') as f:
        input_text = [re.sub(r"\n", "", x) for x in f.readlines()]

    input_split = [list(x) for x in input_text]
    input_split = [[str('"' + y + '"') for y in x] for x in input_split]

    input_string = ""
    for x in input_split:
        for idy, item in enumerate(x):
            if idy < len(x) - 1:
                input_string += item
                input_string += " "
            else:
                input_string += item
                input_string += '\n'

    carmel_args = ['carmel', '-b', '-sli', fst_path]
    epsilon = '*e*'

    p1 = subprocess.Popen(carmel_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p1_out = p1.communicate(input=input_string.encode())[0]
    p1_out = p1_out.decode().strip()
    p1_list = re.split(r"\n", p1_out)

    all_results = []
    for line in p1_list:
        if line == '0':
            all_results.append('*NONE*')
        else:
            transitions = re.split(r"\)\s\(", line)
            transitions = [re.findall(r"\:\s(.*?)\s\/", x)[0] for x in transitions]
            if epsilon in transitions:
                transitions.remove(epsilon)
            result_list = []
            for item in transitions:
                item_strip = re.sub(r'\"', "", item)
                if len(item_strip) > 1:
                    result_list.append('/')
                    result_list.append(item_strip)
                    result_list.append(" ")
                else:
                    result_list.append(item_strip)

            result_concat = "".join(result_list).strip()
            all_results.append(result_concat)
    input_list = input_text

    output_lines = []
    for i, o in zip(input_list, all_results):
        output_lines.append(i + " => " + o)

    with open(output_path, 'w', encoding='utf8') as f:
        f.writelines("%s\n" % line for line in output_lines)


if __name__ == "__main__":
    TEST = False
    if TEST:
        FST_PATH = "output_fst"
        INPUT_PATH = "examples/wordlist_ex"
        carmelize_fst(FST_PATH, INPUT_PATH)
    else:
        carmelize_fst(sys.argv[1], sys.argv[2], sys.argv[3])
