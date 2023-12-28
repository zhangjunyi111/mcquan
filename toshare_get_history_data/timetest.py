import time
import pandas as pd
from datetime import datetime

now = datetime.now()
now = now.strftime("%Y%m%d")
start_date = now
trade_dates = pd.date_range(start=start_date, periods=1).strftime(
    "%Y%m%d").tolist()
print(trade_dates)