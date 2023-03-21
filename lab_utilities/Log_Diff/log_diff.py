# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:48:26 2023

@author: stefa
"""

import difflib

def write_list_to_file(string_list, file_path):
    with open(file_path, "w") as file:
        for string in string_list:
            file.write(string + "\n")


def remove_timestamp(line):
    try:
        return line.split("INFO ")[1]
    except IndexError:
        return None

def extract_logs(file_path, log_marker, keywords):
    keywords.append(log_marker)
    with open(file_path, "r") as file:
        lines = file.readlines()
        lines = [line for line in lines if 'parse DEBUG format' not in line]
        lines = [line for line in lines if line is not None]
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if any([word in line for word in keywords])]
        lines = [line.split('INFO')[1] for line in lines]
        cycle_indices = [i for i, line in enumerate(lines) if log_marker in line]
        return lines[cycle_indices[0]:cycle_indices[1]+1]

def compare_log_files(file1_path, file2_path, split_marker, keywords):
    # function to remove timestamps from log lines


    # read first file and split into cycles
    lines1 = extract_logs(file1_path, split_marker, keywords = ['aspirate', 'dispense', 'tip'])
    lines2 = extract_logs(file2_path, split_marker, keywords = ['aspirate', 'dispense', 'tip'])
    
    write_list_to_file(lines1, "output1.txt")
    write_list_to_file(lines2, "output2.txt")
    

    d = difflib.Differ()
    diff = list(d.compare(lines1, lines2))
    write_list_to_file(diff, "diff.txt")

    return lines1, lines2
