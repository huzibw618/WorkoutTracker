import json
import os
from datetime import datetime


def parseMD(file_path):
    exercises_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'exercises.json')
    muscles_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'muscles.json')
    with open(exercises_path, 'r') as f:
        exercise_names = json.load(f)

    with open(muscles_path, 'r') as f:
        muscle_names = json.load(f)

    with open(file_path, 'r') as file:
        content = file.read()

    content = "\n".join(line.rstrip() for line in content.split("\n"))
    content = content.replace("# Workouts", "").strip()
    workouts = content.split("\n\n")
    parsed_workouts = []
    year = datetime.now().year

    for w in workouts:
        data = w.split('\n')
        date = datetime.strptime(f"{data.pop(0)} {year}", "%B %d %Y").strftime("%Y-%m-%d")
        wtype = data.pop(0).strip()
        while data:
            line = data.pop(0).strip()
            if ':' not in line:
                continue
            exer_data = line.split(':')
            exercise, weights_unit_reps = exer_data[0], exer_data[1].split(';')
            units = weights_unit_reps[1]
            weights = [float(x) for x in weights_unit_reps[0].split(',')]
            reps = [int(x) for x in weights_unit_reps[2].split(',')]
            for i, (weight, rep) in enumerate(zip(weights, reps), 1):
                e_name=exercise_names[exercise]
                m_name=muscle_names[e_name]
                parsed_workouts.append({
                    'date': date,
                    'exercise': e_name,
                    'muscle': m_name,
                    'set_number': i,
                    'weight': weight,
                    'reps': rep,
                    'unit': units
                })

    return parsed_workouts

def parseWeightMD(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    year = datetime.now().year
    results = []

    for line in content.splitlines():
        line = line.strip()
        if not line.startswith('|') or '---' in line:
            continue
        parts = [p.strip() for p in line.strip('|').split('|')]
        if len(parts) < 2 or not parts[0] or not parts[1]:
            continue
        date_str, weight_str = parts[0], parts[1]
        date = datetime.strptime(f"{date_str} {year}", "%B %d %Y").strftime("%Y-%m-%d")
        weight_val = ''.join(c for c in weight_str if c.isdigit() or c == '.')
        unit = ''.join(c for c in weight_str if c.isalpha())
        results.append({'date': date, 'weight': float(weight_val), 'unit': unit})

    return results



