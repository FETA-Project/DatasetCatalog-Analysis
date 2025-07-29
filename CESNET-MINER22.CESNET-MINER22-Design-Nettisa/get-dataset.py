import numpy as np
import csv
import json
import os
import pandas as pd
from  datetime import datetime, timedelta
import itertools
PPI_MAX_LEN = 30

class NettisaConvertor:
    def __init__(self):
        pass

    def get_nettisa(self, ppi: np.ndarray):
        PPI_IPT = 0
        PPI_DIR = 1
        PPI_SIZE = 2
        PPI_PUSH_FLAG = 3

        ppi_len = 30 - np.count_nonzero(ppi[PPI_DIR] == 0)
        nts_mean = np.mean(ppi[PPI_SIZE][:ppi_len])
        nts_min = ppi[PPI_SIZE][:ppi_len].min()
        nts_max = ppi[PPI_SIZE][:ppi_len].max()
        nts_std = np.std(ppi[PPI_SIZE][:ppi_len])
        nts_rts = np.sqrt(np.mean(ppi[PPI_SIZE][:ppi_len]**2))
        nts_avg_dis = np.mean(np.abs(ppi[PPI_SIZE][:ppi_len] - nts_mean))
        nts_kurtosis = np.sum((ppi[PPI_SIZE][:ppi_len] - nts_mean)**4) / (ppi_len * nts_std**4)
        relative_times = np.cumsum(ppi[PPI_IPT][:ppi_len])
        nts_mean_relative_time = np.mean(relative_times)
        nts_mean_time_differences = np.mean(ppi[PPI_IPT][:ppi_len])
        nts_min_time_differences = ppi[PPI_IPT][:ppi_len].min()
        nts_max_time_differences = ppi[PPI_IPT][:ppi_len].max()
        nts_time_distribution = ((np.sum(np.abs(nts_mean_time_differences - ppi[PPI_IPT][:ppi_len]))) / (ppi_len-1)) / ((nts_max_time_differences - nts_min_time_differences) / 2)
        n_swiches = np.count_nonzero(np.diff(ppi[PPI_DIR][:ppi_len]))
        nts_switching_ratio = n_swiches / ( (ppi_len - 1) / 2)
        nts_max_minus_min = nts_max - nts_min
        nts_percent_deviation = nts_avg_dis / nts_mean
        nts_variance = nts_std**2
        nts_burstiness = (nts_std - nts_mean) / (nts_std + nts_mean)
        nts_coef_variation = nts_std / nts_mean
        return  nts_mean, nts_min, nts_max, nts_std, nts_rts, nts_avg_dis, nts_kurtosis, nts_mean_relative_time, nts_mean_time_differences, nts_min_time_differences, nts_max_time_differences, nts_time_distribution, nts_switching_ratio, nts_max_minus_min, nts_percent_deviation, nts_variance, nts_burstiness, nts_coef_variation

    def update_df_with_nettisa_features(self,df):
        results = df['PPI'].apply(lambda x: self.get_nettisa(x))
        df_results = pd.DataFrame(results.tolist(), columns=['nts_mean', 'nts_min', 'nts_max', 'nts_std', 'nts_rts', 'nts_avg_dis', 'nts_kurtosis', 'nts_mean_relative_time', 'nts_mean_time_differences', 'nts_min_time_differences', 'nts_max_time_differences', 'nts_time_distribution', 'nts_switching_ratio', 'nts_max_minus_min', 'nts_percent_deviation', 'nts_variance', 'nts_burstiness', 'nts_coef_variation'])
        df = pd.concat([df, df_results], axis=1)
        df['nts_directions'] = df.PACKETS / (df.PACKETS + df.PACKETS_REV)
        df = df.drop(columns=["PPI"])
        #print("returning",df)
        return df

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
    packets = row.PACKETS
    packets_rev = row.PACKETS_REV
    label = row.LABEL
    return ppi, ppi_len, ppi_duration, ppi_roundtrips, packets, packets_rev, label

def load_csv_dataset(path: str):
    df = pd.read_csv(path, parse_dates=["time TIME_FIRST", "time TIME_LAST"])
    df = df.rename(columns=lambda x: x.split()[1] if len(x.split()) > 1 else x)
    df[["PPI", "PPI_LEN", "PPI_DURATION", "PPI_ROUNDTRIPS", "PACKETS", "PACKETS_REV", "LABEL"]] = df.apply(process_ppi, axis=1, result_type="expand")
    df = df[df.PPI_LEN > 0]
    keep_columns = ["PPI", "PACKETS", "PACKETS_REV","LABEL"]
    df = df[keep_columns]
    ntc = NettisaConvertor()
    df = ntc.update_df_with_nettisa_features(df)
    df.to_csv("miners_design.csv", sep=',', index=False, encoding='utf-8',quoting=csv.QUOTE_NONE, escapechar=' ', mode = "w")

load_csv_dataset("../cesnet-miners22/decrypto_dataset_design.csv")
