import pandas as pd
import matplotlib.pyplot as plt

# Step (a): Import the data
print("Task (a): Import the data")
data = pd.read_excel('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/crime - 1987.xlsx')
data.columns = [
    'county', 'year', 'crmrte', 'prbarr', 'prbconv', 'prbpris', 'avgsen', 'polpc',
    'density', 'taxpc', 'west', 'central', 'east', 'urban', 'pctmin80', 'pctymle',
    'wcon', 'wtuc', 'wtrd', 'wfir', 'wser', 'wmfg', 'wfed', 'wsta', 'wloc'
]
print(data.head())

# Step (b): Calculate a table of descriptive statistics excluding 'county' and 'year'
print("Task (b): Calculate a table of descriptive statistics")
descriptive_stats = data.drop(columns=['county', 'year']).describe().T
descriptive_stats['skewness'] = data.drop(columns=['county', 'year']).skew()
descriptive_stats['kurtosis'] = data.drop(columns=['county', 'year']).kurtosis()
descriptive_stats = descriptive_stats[['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']]
descriptive_stats.columns = ['mean', 'std dev', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']
descriptive_stats = descriptive_stats.round(2)
descriptive_stats[''] = ''  # Adding an extra blank column at the end
print(descriptive_stats)

# Save the descriptive statistics to a CSV file
descriptive_stats.to_csv('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/descriptive_stats_crime.csv')

# Formatting the descriptive statistics table to make it visually pleasant and readable
fig, ax = plt.subplots(figsize=(14, 8))  # set size frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis
ax.set_frame_on(False)  # no visible frame

# Create a table from the DataFrame
table_data = descriptive_stats.reset_index().values.tolist()
column_labels = ["Variable", "mean", "std dev", "min", "25%", "50%", "75%", "max", "skewness", "kurtosis", ""]

table = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

# Add a title
plt.title('Descriptive Statistics for Crime Data by County (1987 North Carolina)', fontsize=16)

# Add a footnote
plt.figtext(0.5, 0.01, 'Source: North Carolina Crime Data, 1987', ha='center', fontsize=12, va='bottom')

# Adjust the layout
plt.subplots_adjust(left=0.2, top=0.8, right=0.95, bottom=0.1)
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/descriptive_stats_crime.png')
plt.show()

# Create a histogram for the variable crmrte
print("Task: Create a histogram for the variable crmrte")
plt.figure(figsize=(10, 6))
plt.hist(data['crmrte'], bins=20, edgecolor='black')
plt.title('Histogram of Crime Rate (crmrte) in North Carolina Counties (1987)', fontsize=14)
plt.xlabel('Crime Rate')
plt.ylabel('Frequency')
plt.grid(True)
plt.figtext(0.5, 0.01, f'Number of Observations: {len(data)}\nSource: North Carolina Crime Data, 1987', ha='center', fontsize=12, va='bottom')
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/histogram_crmrte.png')
plt.show()

# Create a histogram for the variable prbarr
print("Task: Create a histogram for the variable prbarr")
plt.figure(figsize=(10, 6))
plt.hist(data['prbarr'], bins=20, edgecolor='black')
plt.title('Histogram of Probability of Arrest (prbarr) in North Carolina Counties (1987)', fontsize=14)
plt.xlabel('Probability of Arrest')
plt.ylabel('Frequency')
plt.grid(True)
plt.figtext(0.5, 0.01, f'Number of Observations: {len(data)}\nSource: North Carolina Crime Data, 1987', ha='center', fontsize=12, va='bottom')
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/histogram_prbarr.png')
plt.show()
