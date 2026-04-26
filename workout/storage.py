import csv
import os

import pandas as pd


def writeCSV(parsed_workouts, csv_path="Workouts.csv", cols=['date', 'exercise','muscle', 'set_number', 'weight', 'reps', 'unit']):
    existing_dates = set()
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_dates.add(row['date'])

    new_rows = [row for row in parsed_workouts if row['date'] not in existing_dates]

    if not new_rows:
        print("No new workouts to add.")
        return

    with open(csv_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        if os.path.getsize(csv_path) == 0:
            writer.writeheader()
        writer.writerows(new_rows)

    print(f"Added {len(new_rows)} rows for dates: {set(r['date'] for r in new_rows)}")


def loadCSV(csv_path="Workouts.csv"):
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], format='ISO8601')
    
    if csv_path == "Workouts.csv":
        df['weight_kg'] = df.apply(
            lambda r: r['weight'] * 0.453592 if r['unit'].strip().lower() == 'lbs' else r['weight'], axis=1
        )
        df['volume'] = df['weight_kg'] * df['reps']
        df['e1rm'] = df['weight_kg'] * (1 + df['reps'] / 30)
    
    return df
