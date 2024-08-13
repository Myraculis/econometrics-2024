import pandas as pd
import numpy as np
from scipy.stats import skew
import matplotlib.pyplot as plt
from tabulate import tabulate

# Load the dataset
file_path = r'C:\Users\esfbb\OneDrive\Desktop\Code\econometrics\County-level dataset.xlsx'
data = pd.read_excel(file_path)

# Select only numeric columns for descriptive statistics
numeric_cols = data.select_dtypes(include=[np.number]).columns

# Calculate descriptive statistics
descriptive_stats = data[numeric_cols].describe(percentiles=[.05, .25, .5, .75, .95]).T
descriptive_stats['skewness'] = data[numeric_cols].skew()

# Format the statistics to two decimal places
descriptive_stats = descriptive_stats[['mean', 'std', 'skewness', 'min', '5%', '25%', '50%', '75%', '95%', 'max']]
descriptive_stats = descriptive_stats.round(2)

# Rename columns
descriptive_stats.columns = ['Mean', 'Std Dev', 'Skewness', 'Min', '5th Pctl', '25th Pctl', 'Median', '75th Pctl', '95th Pctl', 'Max']

# Split the columns into two parts
columns_part1 = descriptive_stats.columns[:len(descriptive_stats.columns) // 2]
columns_part2 = descriptive_stats.columns[len(descriptive_stats.columns) // 2:]

part1 = descriptive_stats[columns_part1]
part2 = descriptive_stats[columns_part2]

# Add an informative title and footnote
title = "Summary Statistics for County-level Data (2012)"
footnote = ("Source: County-level dataset for the year 2012. Calculations include mean, standard deviation, skewness, minimum, "
            "percentiles, and maximum for each variable. Data compiled from the following sources: U.S. Census Bureau, "
            "U.S. Centers for Disease Control and Prevention (CDC), U.S. Bureau of Economic Analysis (BEA), "
            "U.S. Department of Agriculture (DOA), U.S. Department of Health and Human Services (DHHS), "
            "FBI Uniform Crime Reporting.")

def create_table_plot(df, title, footnote, part):
    fig, ax = plt.subplots(figsize=(10, 12))  # Adjust the size to fit your table
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     rowLabels=df.index,
                     cellLoc='center',
                     loc='center')

    # Set the font size and scale
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Adjust the column widths
    for key, cell in table.get_celld().items():
        cell.set_edgecolor('black')
        if key[1] == -1:  # Row labels
            cell.set_text_props(ha='right', weight='bold')
            cell.set_width(0.2)
        elif key[0] == 0:  # Column headers
            cell.set_text_props(weight='bold')
            cell.set_width(0.1)
        else:
            cell.set_width(0.1)

    # Add title
    plt.title(f"{title} (Part {part})", fontsize=16, pad=20)

    # Add footnote
    plt.figtext(0.5, 0.01, footnote, ha="center", fontsize=12, wrap=True)

    plt.tight_layout()
    plt.show()

# Create plots for each part
create_table_plot(part1, title, footnote, 1)
create_table_plot(part2, title, footnote, 2)
