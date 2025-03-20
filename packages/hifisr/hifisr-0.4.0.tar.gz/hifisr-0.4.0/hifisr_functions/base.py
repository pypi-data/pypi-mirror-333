import subprocess
import sys


def get_cli_output_lines(commands, side_effect = False):
    if side_effect:
        ret = subprocess.call(commands, shell=True)
        return ret
    else:
        output_lines = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.decode().split("\n")[0:-1]
        return output_lines


def get_file_lines(file):
    with open(file, "rt") as fin:
        lines = [ line.rstrip("\n") for line in fin.readlines() ]
    return lines


def load_soft_paths(soft_paths_file):
    soft_paths_dict = { line.split("\t")[0]:line.split("\t")[1] for line in get_file_lines(soft_paths_file) }
    print("", file=sys.stderr)
    print("Loaded paths:")
    for key in soft_paths_dict.keys():
        print(key + " -> " + soft_paths_dict[key], file=sys.stderr)
    print("", file=sys.stderr)
    return soft_paths_dict
