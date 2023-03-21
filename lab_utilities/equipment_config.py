# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 19:08:04 2023

@author: stefa
"""


import json
import importlib
import sys
import os

class ConfigLoader:
    def __init__(self, filename):
        with open(filename) as f:
            self.config = json.load(f)

    def load_class(self, key):
        entry = self.config['equipment'][key]
        if entry['type'] == 'module':
            module = importlib.import_module(entry['import'])
            return module
            class_obj = getattr(module, entry['class'])
            return class_obj(**entry.get('args', {}))
        elif entry['type'] == 'path':
            module_path = entry['import']
            module_dir = os.path.dirname(module_path)  # extract directory containing module
            sys.path.append(module_dir)  # add directory to sys.path
            module_name = os.path.basename(module_path)
            module = importlib.import_module(module_name)
            return module
            class_obj = getattr(module, entry['class'])
            return class_obj(**entry.get('args', {}))
        else:
            raise ValueError(f"Unsupported type {entry['type']} for key {key}")

if __name__ == '__main__':
    a = ConfigLoader('config.json')
    a.load_class()
