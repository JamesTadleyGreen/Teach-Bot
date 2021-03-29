import json

def get_problem_list():
    with open('problem_set.txt', 'r') as f:
        json_data = json.load(f)
    return json_data

def solve_problem(problem_number: int):
    with open('problem_set.txt', 'r+') as f:
        json_data = json.load(f)
        json_data['problems'][problem_number]["solved"] = "True"
        print(json_data['problems'][problem_number])
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(json_data, indent=4))
        return "Done." 
