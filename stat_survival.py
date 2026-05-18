import pandas as pd
from lifelines.statistics import logrank_test, multivariate_logrank_test
import numpy as np

# --- Data Loading ---
file_path = r'动物传染病学\data.csv'
df = pd.read_csv(file_path, sep='\t')
days = ['Day0', 'Day1', 'Day2', 'Day3', 'Day4']

def convert_to_lifelines_format(df, group_filter=None):
    """Converts the wide format counts to long format event data."""
    if group_filter:
        target_df = df[df['group'].str.contains(group_filter)]
    else:
        target_df = df
    
    all_durations = []
    all_events = []
    all_groups = []
    
    for _, row in target_df.iterrows():
        group_name = row['group']
        # Map CRL_1, CRL_2 to Control for simplified comparison
        if 'CRL' in group_name:
            clean_group = 'Control'
        else:
            clean_group = group_name
            
        initial_count = int(row['Day0'])
        current_count = initial_count
        
        # Track individual deaths
        for i in range(1, len(days)):
            prev_day = days[i-1]
            curr_day = days[i]
            deaths = int(row[prev_day] - row[curr_day])
            
            for _ in range(deaths):
                all_durations.append(i-1) # Died at the interval
                all_events.append(1)      # Observed event (death)
                all_groups.append(clean_group)
            
            current_count -= deaths
        
        # Remaining are censored at Day 4
        for _ in range(int(current_count)):
            all_durations.append(4)
            all_events.append(0) # Censored (survived)
            all_groups.append(clean_group)
            
    return pd.DataFrame({
        'group': all_groups,
        'T': all_durations,
        'E': all_events
    })

# Convert all data
full_event_df = convert_to_lifelines_format(df)

# 1. Multivariate Log-rank (Global)
results_global = multivariate_logrank_test(full_event_df['T'], full_event_df['group'], full_event_df['E'])
print(f"Global Log-rank P-value: {results_global.p_value:.4e}")

# 2. Specific: Control vs IP_high
control_events = full_event_df[full_event_df['group'] == 'Control']
ip_high_events = full_event_df[full_event_df['group'] == 'IP_high']
results_ip_high = logrank_test(control_events['T'], ip_high_events['T'], 
                               event_observed_A=control_events['E'], 
                               event_observed_B=ip_high_events['E'])
print(f"Control vs IP_high P-value: {results_ip_high.p_value:.4e}")

# 3. Specific: IP_high vs PO_high
po_high_events = full_event_df[full_event_df['group'] == 'PO_high']
results_route = logrank_test(ip_high_events['T'], po_high_events['T'], 
                             event_observed_A=ip_high_events['E'], 
                             event_observed_B=po_high_events['E'])
print(f"IP_high vs PO_high P-value: {results_route.p_value:.4e}")
