import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load the dataset
file_path = 'C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/cps_2008.xlsx'  # Update the path as needed
data = pd.read_excel(file_path)

# Properly label the variables
data.columns = ['wage', 'educ', 'age', 'exper', 'female', 'black', 'white', 'married', 'union', 'northeast', 'midwest', 'south', 'west', 'fulltime', 'metro']

# Create new variables for ln_wage and ln_educ
data['ln_wage'] = np.log(data['wage'])
data['ln_educ'] = np.log(data['educ'])
data['female_educ'] = data['female'] * data['educ']

# Create geographic region dummies
data = pd.get_dummies(data, columns=['northeast', 'midwest', 'south', 'west'], drop_first=True)

# Define the extended model with geographic region dummies
X = sm.add_constant(data[['educ', 'exper', 'female', 'female_educ', 'midwest_1', 'south_1', 'west_1']])
y = data['ln_wage']

model6 = sm.OLS(y, X).fit(cov_type='HC3')

# Display the regression results
print(model6.summary())

# Save the results to an HTML file
html_content = model6.summary().as_html()
with open('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/extended_regression_results.html', 'w') as f:
    f.write(html_content)
