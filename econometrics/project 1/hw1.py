import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (11, 5)  # set default figure size
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col
from linearmodels.iv import IV2SLS
import seaborn as sns
sns.set_theme()

# Load the dataset
file_path = r'C:\Users\esfbb\OneDrive\Desktop\Code\econometrics\County-level dataset.xlsx'
data = pd.read_excel(file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(data.head())

# Display column names
print("\nColumn names in the dataset:")
print(data.columns)

# Generate descriptive statistics
descriptive_stats = data.describe()
print("\nDescriptive Statistics:")
print(descriptive_stats)

# Set the style of the visualization
sns.set(style="whitegrid")

# Create histograms for two variables
plt.figure(figsize=(12, 5))

# Histogram for the percentage of the population that is obese
plt.subplot(1, 2, 1)
sns.histplot(data['Obesity_%'], kde=True)
plt.title('Histogram of Percentage of Population that is Obese')
plt.xlabel('Percentage of Population that is Obese')

# Histogram for median income
plt.subplot(1, 2, 2)
sns.histplot(data['Median Income'], kde=True)
plt.title('Histogram of Median Income')
plt.xlabel('Median Income')

plt.tight_layout()
plt.show()

# Create scatter diagrams for two pairs of variables
plt.figure(figsize=(12, 5))

# Scatter plot: Percentage of the population that is obese vs. Median income
plt.subplot(1, 2, 1)
sns.scatterplot(x=data['Median Income'], y=data['Obesity_%'])
plt.title('Percentage Obese vs. Median Income')
plt.xlabel('Median Income')
plt.ylabel('Percentage Obese')

# Scatter plot: Number of fast-food restaurants per 100,000 people vs. Median income
plt.subplot(1, 2, 2)
sns.scatterplot(x=data['Median Income'], y=data['Fast_Food_per_100000_people'])
plt.title('Fast-food Restaurants per 100k vs. Median Income')
plt.xlabel('Median Income')
plt.ylabel('Fast-food Restaurants per 100k')

plt.tight_layout()
plt.show()

# Create scatter diagrams for two additional pairs of variables
plt.figure(figsize=(12, 5))

# Scatter plot: Percentage of the population that is obese vs. Percentage in poverty
plt.subplot(1, 2, 1)
sns.scatterplot(x=data['Poverty_%'], y=data['Obesity_%'])
plt.title('Percentage Obese vs. Percentage in Poverty')
plt.xlabel('Percentage in Poverty')
plt.ylabel('Percentage Obese')

# Scatter plot: Percentage of the population with diabetes vs. Percentage in poverty
plt.subplot(1, 2, 2)
sns.scatterplot(x=data['Poverty_%'], y=data['Diabetes_%'])
plt.title('Percentage with Diabetes vs. Percentage in Poverty')
plt.xlabel('Percentage in Poverty')
plt.ylabel('Percentage with Diabetes')

plt.tight_layout()
plt.show()

# Save the descriptive statistics to a CSV file
descriptive_stats.to_csv(r'C:\Users\esfbb\OneDrive\Desktop\Code\econometrics\descriptive_statistics.csv')

print("Analysis complete. The descriptive statistics have been saved to 'descriptive_statistics.csv'.")
