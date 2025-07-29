import numpy as np
import csv
import json
import os
import pandas as pd
from  datetime import datetime, timedelta
import itertools
PPI_MAX_LEN = 30

# Convert array column to comma-separated strings and add label
def format_row(row):
    array_1d = row[0].flatten()  # Flattens 2D to 1D
    array_str = ','.join(map(str, array_1d))
    return f"{array_str},{row[1]}"  # Append the label (Miner)

def process_ppi(row):
    if row.PPI_PKT_LENGTHS == "[]":
        return [], 0, 0, 0
    sizes = list(map(int, row.PPI_PKT_LENGTHS[1:-1].split("|")))
    directions = list(map(int, row.PPI_PKT_DIRECTIONS[1:-1].split("|")))
    times = list(map(datetime.fromisoformat, row.PPI_PKT_TIMES[1:-1].split("|")))
    time_differences = [int((e - s) / timedelta(milliseconds=1)) for s, e in zip(times, times[1:])]
    time_differences.insert(0, 0)
    ppi_roundtrips = len(list(itertools.groupby(itertools.dropwhile(lambda x: x < 0, directions), key=lambda i: i > 0))) // 2
    ppi_len = len(sizes)
    ppi_duration = (times[-1] - times[0]).total_seconds()
    ppi = time_differences, directions, sizes
    ppi = np.array(ppi)[:, :PPI_MAX_LEN]
    ppi = np.pad(ppi, pad_width=((0, 0), (0, PPI_MAX_LEN - len(ppi[0]))))
    return ppi, ppi_len, ppi_duration, ppi_roundtrips

def load_csv_dataset(path: str):
    df = pd.read_csv(path, parse_dates=["time TIME_FIRST", "time TIME_LAST"])
    df = df.rename(columns=lambda x: x.split()[1] if len(x.split()) > 1 else x)
    df[["PPI", "PPI_LEN", "PPI_DURATION", "PPI_ROUNDTRIPS"]] = df.apply(process_ppi, axis=1, result_type="expand")
    df = df[df.PPI_LEN > 0]

    keep_columns = ["PPI", "LABEL"]
    df = df[keep_columns]
    # Convert array column to comma-separated strings and add label

    # Apply to each row
    formatted_df = df.apply(format_row, axis=1)

    num_features = 90 
    header = ['IPT_1', 'IPT_2', 'IPT_3', 'IPT_4', 'IPT_5', 'IPT_6', 'IPT_7', 'IPT_8', 'IPT_9', 'IPT_10', 'IPT_11', 'IPT_12', 'IPT_13', 'IPT_14', 'IPT_15', 'IPT_16', 'IPT_17', 'IPT_18', 'IPT_19', 'IPT_20', 'IPT_21', 'IPT_22', 'IPT_23', 'IPT_24', 'IPT_25', 'IPT_26', 'IPT_27', 'IPT_28', 'IPT_29', 'IPT_30', 'DIR_1', 'DIR_2', 'DIR_3', 'DIR_4', 'DIR_5', 'DIR_6', 'DIR_7', 'DIR_8', 'DIR_9', 'DIR_10', 'DIR_11', 'DIR_12', 'DIR_13', 'DIR_14', 'DIR_15', 'DIR_16', 'DIR_17', 'DIR_18', 'DIR_19', 'DIR_20', 'DIR_21', 'DIR_22', 'DIR_23', 'DIR_24', 'DIR_25', 'DIR_26', 'DIR_27', 'DIR_28', 'DIR_29', 'DIR_30', 'SIZE_1', 'SIZE_2', 'SIZE_3', 'SIZE_4', 'SIZE_5', 'SIZE_6', 'SIZE_7', 'SIZE_8', 'SIZE_9', 'SIZE_10', 'SIZE_11', 'SIZE_12', 'SIZE_13', 'SIZE_14', 'SIZE_15', 'SIZE_16', 'SIZE_17', 'SIZE_18', 'SIZE_19', 'SIZE_20', 'SIZE_21', 'SIZE_22', 'SIZE_23', 'SIZE_24', 'SIZE_25', 'SIZE_26', 'SIZE_27', 'SIZE_28', 'SIZE_29', 'SIZE_30']
    #header = [f'f{i+1}' for i in range(num_features)]
    header.append('label')

    with open('miners-evaluation.csv',mode="w") as file:
        file.write(str(",".join(header))+"\n")

    formatted_df.to_csv("miners-evaluation.csv", sep=',', index=False, encoding='utf-8',quoting=csv.QUOTE_NONE, escapechar=' ', header=False, mode = "a")

load_csv_dataset("decrypto_dataset_evaluation.csv")
