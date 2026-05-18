import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import numpy as np

# --- Data Loading & Pre-processing ---
file_path = r'动物传染病学\data.csv'
df = pd.read_csv(file_path, sep='\t')
days = ['Day0', 'Day1', 'Day2', 'Day3', 'Day4']

def get_event_data(row):
    durations = []
    events = []
    initial = int(row['Day0'])
    current = initial
    for i in range(1, len(days)):
        deaths = int(row[days[i-1]] - row[days[i]])
        for _ in range(deaths):
            durations.append(i-1)
            events.append(1)
        current -= deaths
    for _ in range(current):
        durations.append(4)
        events.append(0)
    return durations, events

# --- Analysis ---
summary_data = []

# Process Controls first for comparison
crl_rows = df[df['group'].str.contains('CRL')]
crl_durations = []
crl_events = []
for _, row in crl_rows.iterrows():
    d, e = get_event_data(row)
    crl_durations.extend(d)
    crl_events.extend(e)

kmf_control = KaplanMeierFitter()
kmf_control.fit(crl_durations, crl_events)
mst_control = kmf_control.median_survival_time_
mortality_control = (sum(crl_events) / len(crl_events)) * 100

summary_data.append({
    'Group': 'Control (Merged)',
    'n': len(crl_events),
    'Mortality (%)': f"{mortality_control:.1f}%",
    'MST (Days)': 'Undefined' if np.isinf(mst_control) else f"{mst_control:.1f}",
    'P-value (vs. Control)': '-'
})

# Process Experimental Groups
exp_df = df[~df['group'].str.contains('CRL')]
for _, row in exp_df.iterrows():
    group = row['group']
    durations, events = get_event_data(row)
    
    kmf = KaplanMeierFitter()
    kmf.fit(durations, events)
    mst = kmf.median_survival_time_
    mortality = (sum(events) / len(events)) * 100
    
    # Stat test vs Control
    results = logrank_test(durations, crl_durations, event_observed_A=events, event_observed_B=crl_events)
    p_val = f"{results.p_value:.4f}" if results.p_value >= 0.0001 else "<0.0001"
    
    summary_data.append({
        'Group': group,
        'n': len(events),
        'Mortality (%)': f"{mortality:.1f}%",
        'MST (Days)': 'Undefined' if np.isinf(mst) else f"{mst:.1f}",
        'P-value (vs. Control)': p_val
    })

summary_df = pd.DataFrame(summary_data)

# Output as Simple Table
print("\n### 📊 沙门氏菌感染实验生存数据汇总表 (Salmonella Infection Summary)")
print("Group | n | Mortality (%) | MST (Days) | P-value (vs. Control)")
print("--- | --- | --- | --- | ---")
for _, row in summary_df.iterrows():
    print(f"{row['Group']} | {row['n']} | {row['Mortality (%)']} | {row['MST (Days)']} | {row['P-value (vs. Control)']}")

# Also save to a file for the user
summary_df.to_csv('survival_summary_table.csv', index=False)
print("\nSummary saved to survival_summary_table.csv")
