import pandas as pd
from lifelines.statistics import logrank_test

df = pd.read_csv(r'动物传染病学\data.csv', sep='\t')
days_cols = ['Day0', 'Day1', 'Day2', 'Day3', 'Day4']

def get_event_data(row):
    durations, events = [], []
    initial = int(row['Day0'])
    current = initial
    for i in range(1, len(days_cols)):
        deaths = int(row[days_cols[i-1]] - row[days_cols[i]])
        for _ in range(deaths):
            durations.append(i-1)
            events.append(1)
        current -= deaths
    for _ in range(current):
        durations.append(4)
        events.append(0)
    return durations, events

# PO comparisons (vs CRL_1)
c1_dur, c1_evt = get_event_data(df[df['group'] == 'CRL_1'].iloc[0])
for g in ['PO_low', 'PO_medium', 'PO_high']:
    dur, evt = get_event_data(df[df['group'] == g].iloc[0])
    res = logrank_test(dur, c1_dur, event_observed_A=evt, event_observed_B=c1_evt)
    print(f"{g} vs CRL_1: P={res.p_value:.6f}")

# IP comparisons (vs CRL_2)
c2_dur, c2_evt = get_event_data(df[df['group'] == 'CRL_2'].iloc[0])
for g in ['IP_low', 'IP_medium', 'IP_high']:
    dur, evt = get_event_data(df[df['group'] == g].iloc[0])
    res = logrank_test(dur, c2_dur, event_observed_A=evt, event_observed_B=c2_evt)
    print(f"{g} vs CRL_2: P={res.p_value:.6f}")
