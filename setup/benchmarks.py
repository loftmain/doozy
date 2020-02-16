import pandas as pd
from trading_calendars import get_calendar


def get_benchmark_returns(symbol, first_date, last_date):
    cal = get_calendar('NYSE')

    dates = cal.sessions_in_range(first_date, last_date)

    data = pd.DataFrame(0.0, index=dates, columns=['close'])
    data = data['close']

    return data.sort_index().iloc[1:]
