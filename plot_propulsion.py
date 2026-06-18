import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. Data Preparation
data = {
    "Control": [58.62, 54.24, 63.16, 33.96],
    "Zengye Chengqi": [57.50, 57.19],
    "Dachengqi": [63.64, 71.67, 17.82],
    "Compound Dachengqi": [62.73, 56.67]
}

# Convert to DataFrame for easier handling
df_list = []
for group, values in data.items():
    for val in values:
        df_list.append({"Group": group, "Propulsion": val})
df = pd.DataFrame(df_list)

# 2. Outlier Detection and Removal (Robust for small samples)
def remove_outliers(df, group_col, val_col):
    filtered_df = pd.DataFrame()
    for group in df[group_col].unique():
        group_data = df[df[group_col] == group].copy()
        vals = group_data[val_col].values
        if len(vals) >= 3:
            # Use Median Absolute Deviation (MAD) for robust outlier detection
            median = np.median(vals)
            mad = np.median(np.abs(vals - median))
            if mad > 0:
                # Modified Z-score: 0.6745 * (x - median) / MAD
                mod_z = 0.6745 * (vals - median) / mad
                group_data = group_data[np.abs(mod_z) < 3.0] # Threshold of 3.0 is standard
            else:
                # If all values are same, mad=0, keep all
                pass
        filtered_df = pd.concat([filtered_df, group_data])
    return filtered_df

df_clean = remove_outliers(df, "Group", "Propulsion")

# 3. Statistical Analysis (Compare each group to Control)
# Using independent t-test (two-tailed)
results = {}
control_vals = df_clean[df_clean["Group"] == "Control"]["Propulsion"].values
groups = [g for g in df_clean["Group"].unique() if g != "Control"]

print(f"Control (n={len(control_vals)}): Mean={np.mean(control_vals):.2f}, SD={np.std(control_vals, ddof=1):.2f}")

for g in groups:
    group_vals = df_clean[df_clean["Group"] == g]["Propulsion"].values
    t_stat, p_val = stats.ttest_ind(control_vals, group_vals, equal_var=False)
    results[g] = p_val
    print(f"{g} (n={len(group_vals)}): Mean={np.mean(group_vals):.2f}, SD={np.std(group_vals, ddof=1):.2f}, p={p_val:.4f}")

# 4. Visualization (Nature Style)
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "savefig.dpi": 600,
})

fig, ax = plt.subplots(figsize=(3.5, 3))

# Colors
colors = ["#BDC3C7", "#3498DB", "#E67E22", "#2ECC71"]

# Barplot with individual points
sns.barplot(data=df_clean, x="Group", y="Propulsion", hue="Group", palette=colors, 
            errorbar="sd", capsize=0.1, err_kws={'linewidth': 1}, legend=False, ax=ax)
sns.stripplot(data=df_clean, x="Group", y="Propulsion", color=".3", alpha=0.6, jitter=0.1, ax=ax)

# Significance markers
def add_sig_marker(p_val, x_idx, group_vals):
    if p_val < 0.001:
        marker = "***"
    elif p_val < 0.01:
        marker = "**"
    elif p_val < 0.05:
        marker = "*"
    else:
        # If not significant, we could optionally add 'ns'
        # ax.text(x_idx, y_pos, "ns", ha='center', va='bottom', fontsize=6)
        return
    
    y_pos = np.max(group_vals) + (np.max(df_clean["Propulsion"]) * 0.05)
    ax.text(x_idx, y_pos, marker, ha='center', va='bottom', fontsize=8, fontweight='bold')

group_order = df_clean["Group"].unique()
for i, g in enumerate(group_order):
    if g in results:
        add_sig_marker(results[g], i, df_clean[df_clean["Group"] == g]["Propulsion"])

ax.set_ylabel("Charcoal Propulsion Rate (%)")
ax.set_xlabel("")
ax.set_xticks(range(len(group_order)))
ax.set_xticklabels(["Control", "Zengye\nChengqi", "Dachengqi", "Compound\nDachengqi"])
ax.set_ylim(0, max(df_clean["Propulsion"]) * 1.2)

plt.tight_layout()

# Save
fig.savefig("propulsion_results.png")
fig.savefig("propulsion_results.pdf")
fig.savefig("propulsion_results.svg")

print("Figure generated successfully.")
print("P-values compared to Control:")
for g, p in results.items():
    print(f"{g}: {p:.4f}")
