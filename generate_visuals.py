import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

# Scenario Results Data
scenarios = {
    'Mode': ['TODAY']*6 + ['FUTURE']*6,
    'Scenario': [
        'Valid Route (Operational)',
        'Invalid Route (Maintenance)',
        'Valid Route (Normal Ops)',
        'Inconsistent Advisory',
        'Valid Advisory (Complete)',
        'Invalid (Peak + Reduced)',
        'Valid (T5 Complete)',
        'Invalid (T5 Missing TEL)',
        'Consistent (Integration)',
        'Inconsistent (Integration Error)',
        'Invalid (Dual Line Ops)',
        'Invalid (T5 Missing CRL)'
    ],
    'Result': ['VALID', 'INVALID', 'VALID', 'INCONSISTENT', 'CONSISTENT', 'INVALID',
               'VALID', 'INVALID', 'CONSISTENT', 'INCONSISTENT', 'INVALID', 'INVALID'],
    'Violated_Rule': [None, 'RULE-3a', None, 'RULE-5a', None, 'RULE-11',
                      None, 'RULE-7a', None, 'RULE-4a', 'RULE-8', 'RULE-9b']
}

df = pd.DataFrame(scenarios)

# Figure 1: Results Summary by Mode
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# TODAY Mode
today_counts = df[df['Mode'] == 'TODAY']['Result'].value_counts()
colors_today = ['#4CAF50', '#F44336', '#FF9800']
ax1.pie(today_counts.values, labels=today_counts.index, autopct='%1.0f%%',
        colors=colors_today, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
ax1.set_title('TODAY Mode Results (6 scenarios)', fontsize=14, weight='bold')

# FUTURE Mode
future_counts = df[df['Mode'] == 'FUTURE']['Result'].value_counts()
colors_future = ['#4CAF50', '#F44336', '#FF9800']
ax2.pie(future_counts.values, labels=future_counts.index, autopct='%1.0f%%',
        colors=colors_future, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
ax2.set_title('FUTURE Mode Results (6 scenarios)', fontsize=14, weight='bold')

plt.tight_layout()
plt.savefig('scenario_results_summary.png', dpi=300, bbox_inches='tight')
print("✓ Created: scenario_results_summary.png")

# Figure 2: All Scenarios Overview
fig, ax = plt.subplots(figsize=(12, 8))

# Create color mapping
result_colors = {'VALID': '#4CAF50', 'INVALID': '#F44336', 'CONSISTENT': '#2196F3', 'INCONSISTENT': '#FF9800'}
colors = [result_colors[r] for r in df['Result']]

# Horizontal bar chart
y_pos = range(len(df))
ax.barh(y_pos, [1]*len(df), color=colors, height=0.8)

# Add scenario labels
for i, (idx, row) in enumerate(df.iterrows()):
    label = f"{row['Scenario']}"
    if row['Violated_Rule']:
        label += f" ({row['Violated_Rule']})"
    ax.text(0.5, i, label, va='center', ha='center', fontsize=10, weight='bold', color='white')

# Mode separators
ax.axhline(5.5, color='black', linewidth=2, linestyle='--')
ax.text(0.05, 2.5, 'TODAY MODE', fontsize=12, weight='bold', rotation=90, va='center')
ax.text(0.05, 8.5, 'FUTURE MODE', fontsize=12, weight='bold', rotation=90, va='center')

ax.set_yticks([])
ax.set_xlim(0, 1)
ax.set_xticks([])
ax.set_title('All 12 Test Scenarios - Complete Results', fontsize=16, weight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#4CAF50', label='VALID'),
                   Patch(facecolor='#F44336', label='INVALID'),
                   Patch(facecolor='#2196F3', label='CONSISTENT'),
                   Patch(facecolor='#FF9800', label='INCONSISTENT')]
ax.legend(handles=legend_elements, loc='upper right', fontsize=11)

plt.tight_layout()
plt.savefig('all_scenarios_overview.png', dpi=300, bbox_inches='tight')
print("✓ Created: all_scenarios_overview.png")

# Figure 3: Rule Violations Breakdown
violations_data = df[df['Violated_Rule'].notna()]['Violated_Rule'].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(range(len(violations_data)), violations_data.values, color='#F44336', edgecolor='black', linewidth=1.5)

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, violations_data.values)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, str(val),
            ha='center', va='bottom', fontsize=12, weight='bold')

ax.set_xticks(range(len(violations_data)))
ax.set_xticklabels(violations_data.index, rotation=0, fontsize=11, weight='bold')
ax.set_ylabel('Number of Violations', fontsize=12, weight='bold')
ax.set_title('Rule Violations Detected Across All Scenarios', fontsize=14, weight='bold', pad=15)
ax.set_ylim(0, max(violations_data.values) + 0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('rule_violations_breakdown.png', dpi=300, bbox_inches='tight')
print("✓ Created: rule_violations_breakdown.png")

print("\n📊 Generated 3 visualizations:")
print("1. scenario_results_summary.png → Use in Slide 7 (Test Results)")
print("2. all_scenarios_overview.png → Use in Slide 7 (Test Results)")
print("3. rule_violations_breakdown.png → Use in Slide 8 (Key Finding #1)")
