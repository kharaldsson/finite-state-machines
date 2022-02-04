#!/opt/python-3.6/bin/python3.6 python3

import sys
import os
import subprocess
from subprocess import PIPE
import re


def carmelize(fsa_path, input_path):
    with open(input_path, 'r', encoding='utf8') as f:
        input_text = f.read()

    carmel_args = ['carmel', '-b', '-sli']
    carmel_args.append(fsa_path)

    p1 = subprocess.Popen(carmel_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p1_out = p1.communicate(input=input_text.encode())[0]
    p1_out = p1_out.decode().strip()#.encode()
    p1_list = re.split(r"\n", p1_out)
    accept_ls = ["no" if x == '0' else 'yes' for x in p1_list]
    input_list = re.split(r"\n", input_text)
    for i, a in zip(input_list, accept_ls):
        print(i + " => " + a)


if __name__ == "__main__":
    carmelize(sys.argv[1], sys.argv[2])
