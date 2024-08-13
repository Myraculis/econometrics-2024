import pandas as pd
import statsmodels.api as sm

# Step (a): Import the data
print("Task (a): Import the data")
data = pd.read_excel('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/crime - 1987.xlsx')
data.columns = [
    'county', 'year', 'crmrte', 'prbarr', 'prbconv', 'prbpris', 'avgsen', 'polpc',
    'density', 'taxpc', 'west', 'central', 'east', 'urban', 'pctmin80', 'pctymle',
    'wcon', 'wtuc', 'wtrd', 'wfir', 'wser', 'wmfg', 'wfed', 'wsta', 'wloc'
]
print(data.head())

# Step (b): Perform OLS regression of crmrte on prbarr
print("Task (b): Perform OLS regression of crmrte on prbarr")
X = data['prbarr']
y = data['crmrte']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit(cov_type='HC3')  # Heteroskedasticity-robust standard errors

# Print the regression results
print(model.summary())

# Extract the coefficient for prbarr
prbarr_coefficient = model.params['prbarr']
prbarr_std_err = model.bse['prbarr']
print(f"Coefficient for prbarr: {prbarr_coefficient}")
print(f"Standard Error for prbarr: {prbarr_std_err}")