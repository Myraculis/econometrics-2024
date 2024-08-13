import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step (a): Import the data
print("Task (a): Import the data")
data = pd.read_excel('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/crime - 1987.xlsx')
data.columns = [
    'county', 'year', 'crmrte', 'prbarr', 'prbconv', 'prbpris', 'avgsen', 'polpc',
    'density', 'taxpc', 'west', 'central', 'east', 'urban', 'pctmin80', 'pctymle',
    'wcon', 'wtuc', 'wtrd', 'wfir', 'wser', 'wmfg', 'wfed', 'wsta', 'wloc'
]
print(data.head())

# Select relevant columns for the correlation matrix
selected_columns = ['crmrte', 'prbarr', 'prbconv', 'prbpris', 'avgsen', 'polpc']

# Calculate the correlation matrix
correlation_matrix = data[selected_columns].corr()

# Create a heatmap for the correlation matrix
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, cbar_kws={'label': 'Correlation Coefficient'})
plt.title('Correlation Matrix of Crime Rate and Explanatory Variables', fontsize=16)
plt.xlabel('Variables')
plt.ylabel('Variables')

# Add a footnote with the source
plt.figtext(0.5, -0.1, 'Source: North Carolina Crime Data, 1987', ha='center', fontsize=12, va='bottom')

# Adjust the layout to make room for the footnote
plt.subplots_adjust(bottom=0.2)

# Save the heatmap as a PNG file
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/correlation_matrix.png', bbox_inches='tight')
plt.show()

# Print the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)
