import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col

# Load the dataset
file_path = 'C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/cps_2008.xlsx'  # Update the path as needed
data = pd.read_excel(file_path)

# Properly label the variables
data.columns = ['wage', 'educ', 'age', 'exper', 'female', 'black', 'white', 'married', 'union', 'northeast', 'midwest', 'south', 'west', 'fulltime', 'metro']

# Create new variables for ln_wage and ln_educ
data['ln_wage'] = np.log(data['wage'])
data['ln_educ'] = np.log(data['educ'])
data['female_educ'] = data['female'] * data['educ']

# Define the models
model1 = sm.OLS(data['ln_wage'], sm.add_constant(data['ln_educ'])).fit(cov_type='HC3')
model2 = sm.OLS(data['ln_wage'], sm.add_constant(data['educ'])).fit(cov_type='HC3')
model3 = sm.OLS(data['ln_wage'], sm.add_constant(data[['educ', 'exper']])).fit(cov_type='HC3')
model4 = sm.OLS(data['ln_wage'], sm.add_constant(data[['educ', 'exper', 'female']])).fit(cov_type='HC3')
model5 = sm.OLS(data['ln_wage'], sm.add_constant(data[['educ', 'exper', 'female', 'female_educ']])).fit(cov_type='HC3')

# Display side-by-side regression results
results_table = summary_col([model1, model2, model3, model4, model5], stars=True, float_format='%0.3f',
                            model_names=['Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5'],
                            info_dict={'N': lambda x: "{0:d}".format(int(x.nobs)),
                                       'R2': lambda x: "{:.3f}".format(x.rsquared),
                                       'Adj. R2': lambda x: "{:.3f}".format(x.rsquared_adj)})

# Display the results
print(results_table)

# Save the results to an HTML file
html_content = results_table.as_html()
with open('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/regression_results.html', 'w') as f:
    f.write(html_content)
