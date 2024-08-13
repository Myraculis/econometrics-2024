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

# Perform the F-test for joint significance of geographic region dummies
f_test = model6.f_test("midwest_1 = 0, south_1 = 0, west_1 = 0")
f_stat = f_test.fvalue
p_value = f_test.pvalue

# Display the F-test results
print(f"F-statistic: {f_stat}")
print(f"P-value: {p_value}")

# Determine critical values
df1 = 3  # Number of restrictions
df2 = model6.df_resid  # Degrees of freedom of residuals

# Critical values from Table 4
critical_value_5_percent = 2.60
critical_value_1_percent = 3.78

# Decision based on F-statistic
if f_stat > critical_value_5_percent:
    print("Reject the null hypothesis at the 5% significance level: geographic regions jointly matter for earnings.")
else:
    print("Fail to reject the null hypothesis at the 5% significance level: geographic regions do not jointly matter for earnings.")

if f_stat > critical_value_1_percent:
    print("Reject the null hypothesis at the 1% significance level: geographic regions jointly matter for earnings.")
else:
    print("Fail to reject the null hypothesis at the 1% significance level: geographic regions do not jointly matter for earnings.")
