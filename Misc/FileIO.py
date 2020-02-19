from os.path import join, isfile, isdir
from os import listdir
import json

def files_in_path(filepath):
    return [f for f in listdir(filepath) if isfile(join(filepath, f))]

def dirs_in_path(filepath):
    return [f for f in listdir(filepath) if isdir(join(filepath, f))]

def open_file(filepath):
    if "/" in filepath:
        filepath = filepath.replace("/", "\\")

    split_path = filepath.split("\\")
    file_cfg = split_path[len(split_path)-1].split(".")
    lines = []
    with open(filepath, "r") as reader:
        if file_cfg[1] in ["txt", "cfg"]:
            for line in reader.readlines():
                lines.append(line)
        elif file_cfg[1] in ["json"]:
            lines = json.load(reader)
        reader.close()
    return lines


