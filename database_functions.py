import json

def get_problem_list():
    with open('problem_set.txt', 'r') as f:
        json_data = json.load(f)
    return json_data
