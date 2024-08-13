import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

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

# Step (c): Calculate the fitted values and residuals
data['fitted_values'] = model.fittedvalues
data['residuals'] = model.resid

# Step (d): Plot the residuals against prbarr
plt.figure(figsize=(10, 6))
plt.scatter(data['prbarr'], data['residuals'], edgecolor='black')
plt.title('Residuals vs. Probability of Arrest (prbarr)')
plt.xlabel('Probability of Arrest (prbarr)')
plt.ylabel('Residuals')
plt.grid(True)
plt.axhline(0, color='red', linestyle='--')
plt.figtext(0.5, -0.05, 'Source: North Carolina Crime Data, 1987', ha='center', fontsize=12, va='bottom')
plt.subplots_adjust(bottom=0.2)
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/residuals_vs_prbarr.png')
plt.show()

# Print the regression results for reference
print(model.summary())
