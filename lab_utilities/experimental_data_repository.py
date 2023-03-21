# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:24:20 2022

@author: stefa
"""
from datetime import datetime as dt
import os
import re
import json
import shutil

def get_experimental_params(method_name, roboid):
    
    experimental_params_dict = {}
    
    experimental_params_dict.update({'Method_Name': method_name})
    experimental_params_dict.update({'Robot_ID': roboid})
    
    user_name = input("\n\n\nRunning " + method_name + "\n\n\n\nWhat is your name?: ")
    experimental_params_dict.update({'Username': user_name})
    
    experiment_name = input("Please provide a unique name for your experiment: ")
    experimental_params_dict.update({'Experiment_Name': experiment_name})
    
    experiment_desc = input("(Optional) Feel free to provide a description for your experiment: ")
    experimental_params_dict.update({'Experiment_Desc': experiment_desc})
    
    timestamp = str(dt.now())
    experimental_params_dict.update({'Timestamp': timestamp})
    
    with open('prompt_fields', 'r') as f:
        prompts = json.load(f)

    for prompt in prompts:
        parameter = input(prompt['prompt'] + ': ')
        if parameter:
            experimental_params_dict.update({prompt['field']: parameter})
        else:
            try:
                experimental_params_dict.update({prompt['default']: parameter})
            except KeyError:
                raise Exception("No default setting for this field")
    return experimental_params_dict


def define_experimental_config(experimental_params, data_repository):
    
    
    user = experimental_params['Username']
    exp_name = experimental_params['Experiment_Name']
    exp_desc = experimental_params['Experiment_Desc']
    timestamp = experimental_params['Timestamp']
    method_name = experimental_params['Method_Name']
    robot_id_num = experimental_params['Robot_ID']
    
    
    user_dir = os.path.join(data_repository, user + '_Robot_Experiments')
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    
    user_method_dir = os.path.join(user_dir, method_name)
    if not os.path.exists(user_method_dir):
        os.mkdir(user_method_dir)
    dir_string = timestamp.split(' ')[0]
    dir_string = re.sub('-', '', dir_string)
    dir_string = dir_string + '_' + exp_name + '_' + robot_id_num
    
    experiment_dir = os.path.join(user_method_dir, dir_string)
    if not os.path.exists(experiment_dir):
        os.mkdir(experiment_dir)
    

    return experiment_dir

def reset_config_dict(roboid):
    experimental_params_dict = {}
    experimental_params_dict.update({'Username': 'test'})
    params_file_str = 'experimental_params_' + roboid + '.json'
    with open(params_file_str, 'w') as fp:
        json.dump(experimental_params_dict, fp)

def create_config_dict(method_name, roboid, repository_path):
    experimental_params = get_experimental_params(method_name, roboid)
    params_file_str = 'experimental_params_' + roboid + '.json'
    with open(params_file_str, 'w') as fp:
        json.dump(experimental_params, fp)
    exp_dir_path = define_experimental_config(experimental_params, repository_path)
    shutil.copy(params_file_str, exp_dir_path)
    return exp_dir_path
        
def pull_config_dict(roboid):
    params_file_str = 'experimental_params_' + roboid + '.json'
    with open(params_file_str, 'r') as fp:
        experimental_params = json.load(fp)
    exp_dir_path = define_experimental_config(experimental_params)
    return exp_dir_path