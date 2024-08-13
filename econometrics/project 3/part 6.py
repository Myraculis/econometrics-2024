import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Step (a): Import the data
print("Task (a): Import the data")
data = pd.read_excel('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/crime - 1987.xlsx')
data.columns = [
    'county', 'year', 'crmrte', 'prbarr', 'prbconv', 'prbpris', 'avgsen', 'polpc',
    'density', 'taxpc', 'west', 'central', 'east', 'urban', 'pctmin80', 'pctymle',
    'wcon', 'wtuc', 'wtrd', 'wfir', 'wser', 'wmfg', 'wfed', 'wsta', 'wloc'
]
print(data.head())

# Step (b): Regress crmrte on prbarr, density, east, and west (omitting central)
print("Task (b): Regress crmrte on prbarr, density, east, and west")
model_new = smf.ols('crmrte ~ prbarr + density + east + west', data=data).fit(cov_type='HC3')

# Print the summary of the regression model
print(model_new.summary())
