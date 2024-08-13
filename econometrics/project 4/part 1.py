import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = 'C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/cps_2008.xlsx'  # Update the path as needed
data = pd.read_excel(file_path)

# Properly label the variables
data.columns = ['wage', 'educ', 'age', 'exper', 'female', 'black', 'white', 'married', 'union', 'northeast', 'midwest', 'south', 'west', 'fulltime', 'metro']

# Calculate descriptive statistics and round to three decimal places
descriptive_stats = data.describe().round(3)

# Calculate skewness and kurtosis
descriptive_stats.loc['skewness'] = data.skew().round(3)
descriptive_stats.loc['kurtosis'] = data.kurt().round(3)

# Reorder the index to place skewness and kurtosis after max
descriptive_stats = descriptive_stats.reindex(['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis'])

# Export the descriptive statistics to an Excel file
output_file = 'C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/descriptive_statistics.xlsx'
descriptive_stats.to_excel(output_file)

# Create a table of statistics and save as a PNG file
fig, ax = plt.subplots(figsize=(12, 6))  # set size frame
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=descriptive_stats.values, colLabels=descriptive_stats.columns, rowLabels=descriptive_stats.index, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

# Add footnote
plt.figtext(0.5, 0.02, '4733 observations\nData source: Dr. Kang Sun Lee, Louisiana Department of Health and Human Services', wrap=True, horizontalalignment='center', fontsize=10)

plt.title('Descriptive Statistics for CPS 2008')
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/descriptive_statistics.png', bbox_inches='tight', dpi=300)

# Display the descriptive statistics
print(descriptive_stats)
