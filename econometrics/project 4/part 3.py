import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/cps_2008.xlsx'  # Update the path as needed
data = pd.read_excel(file_path)

# Properly label the variables
data.columns = ['wage', 'educ', 'age', 'exper', 'female', 'black', 'white', 'married', 'union', 'northeast', 'midwest', 'south', 'west', 'fulltime', 'metro']

# Create new variables for ln_wage and ln_educ
data['ln_wage'] = np.log(data['wage'])
data['ln_educ'] = np.log(data['educ'])

# Create a single graph with four scatter plots
fig, axs = plt.subplots(2, 2, figsize=(14, 12))

# Scatter plot: wage vs. educ
axs[0, 0].scatter(data['educ'], data['wage'], alpha=0.5)
axs[0, 0].set_xlabel('Years of Education')
axs[0, 0].set_ylabel('Wage')
axs[0, 0].set_title('Wage vs. Years of Education')

# Scatter plot: wage vs. ln_educ
axs[0, 1].scatter(data['ln_educ'], data['wage'], alpha=0.5)
axs[0, 1].set_xlabel('Log of Years of Education')
axs[0, 1].set_ylabel('Wage')
axs[0, 1].set_title('Wage vs. Log of Years of Education')

# Scatter plot: ln_wage vs. educ
axs[1, 0].scatter(data['educ'], data['ln_wage'], alpha=0.5)
axs[1, 0].set_xlabel('Years of Education')
axs[1, 0].set_ylabel('Log of Wage')
axs[1, 0].set_title('Log of Wage vs. Years of Education')

# Scatter plot: ln_wage vs. ln_educ
axs[1, 1].scatter(data['ln_educ'], data['ln_wage'], alpha=0.5)
axs[1, 1].set_xlabel('Log of Years of Education')
axs[1, 1].set_ylabel('Log of Wage')
axs[1, 1].set_title('Log of Wage vs. Log of Years of Education')

# Adjust layout
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/wage_education_relationships.png', bbox_inches='tight', dpi=300)

# Display the plot
plt.show()
