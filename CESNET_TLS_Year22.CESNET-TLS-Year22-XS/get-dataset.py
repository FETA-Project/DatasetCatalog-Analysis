
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cesnet_datazoo.datasets import CESNET_TLS_Year22, CESNET_QUIC22
from cesnet_datazoo.config import DatasetConfig, AppSelection
from datetime import datetime, timedelta

from xgboost import XGBClassifier
import sklearn.metrics as metrics
#from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report,confusion_matrix,f1_score
#from sklearn.model_selection import train_test_split

#data = CESNET_TLS_Year22("/katoda/TLS/", size="XS")
data = CESNET_TLS_Year22("../../../TLS22_2/", size="XS")
common_params = {
    "dataset": data,
    "train_period_name": "W-2022-44",
    "apps_selection": AppSelection.ALL_KNOWN,
    "use_packet_histograms": True,
}

hist_df = pd.DataFrame()
current_date = datetime(2022, 1, 1)
while current_date <= datetime(2022, 1, 7):
    print("testing date ->", current_date)
    try:
        dataset_config = DatasetConfig(**common_params, test_period_name=current_date.strftime("M-%Y-%m"), test_dates=[current_date.strftime("%Y%m%d")])
        data.set_dataset_config_and_initialize(dataset_config)
    except Exception as e:
        print("missing date -> ",current_date)
    curr_df = data.get_test_df(flatten_ppi=True)
    curr_sample = curr_df.sample(25000, random_state = 42, replace=True)
    curr_sample["date"] = current_date
    hist_df = pd.concat([hist_df,curr_sample])
    current_date += timedelta(days=1)
#hist_df = hist_df.drop(columns=["date"])
#hist_df.to_csv("tls-evalution-date.csv", sep=',', index=False, encoding='utf-8')
hist_df.to_csv("tls-evalution-date-training-one-week.csv", sep=',', index=False, encoding='utf-8')

#Xdata = hist_df.drop(columns=["APP","date"])
#ydata = hist_df.APP


