import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
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

# Step (b): Estimate the four models
print("Task (b): Estimate the four models")

# Model (1): Regress crmrte on prbarr
model1 = smf.ols('crmrte ~ prbarr', data=data).fit(cov_type='HC3')

# Model (2): Regress crmrte on prbarr and density
model2 = smf.ols('crmrte ~ prbarr + density', data=data).fit(cov_type='HC3')

# Model (3): Regress crmrte on prbarr, density, and urban
model3 = smf.ols('crmrte ~ prbarr + density + urban', data=data).fit(cov_type='HC3')

# Model (4): Regress crmrte on prbarr and urban
model4 = smf.ols('crmrte ~ prbarr + urban', data=data).fit(cov_type='HC3')

# Step (c): Create a function to format coefficients with significance stars
def format_coef(pval, coef):
    if pval < 0.01:
        return f"{coef:.3f}***"
    elif pval < 0.05:
        return f"{coef:.3f}**"
    elif pval < 0.1:
        return f"{coef:.3f}*"
    else:
        return f"{coef:.3f}"

# Step (d): Extract results into a DataFrame
results = {
    'Variable': ['Intercept', 'prbarr', 'density', 'urban'],
    'Model 1 Coef (SE)': [
        format_coef(model1.pvalues['Intercept'], model1.params['Intercept']) + f" ({model1.bse['Intercept']:.3f})",
        format_coef(model1.pvalues['prbarr'], model1.params['prbarr']) + f" ({model1.bse['prbarr']:.3f})",
        '', ''
    ],
    'Model 2 Coef (SE)': [
        format_coef(model2.pvalues['Intercept'], model2.params['Intercept']) + f" ({model2.bse['Intercept']:.3f})",
        format_coef(model2.pvalues['prbarr'], model2.params['prbarr']) + f" ({model2.bse['prbarr']:.3f})",
        format_coef(model2.pvalues['density'], model2.params['density']) + f" ({model2.bse['density']:.3f})",
        ''
    ],
    'Model 3 Coef (SE)': [
        format_coef(model3.pvalues['Intercept'], model3.params['Intercept']) + f" ({model3.bse['Intercept']:.3f})",
        format_coef(model3.pvalues['prbarr'], model3.params['prbarr']) + f" ({model3.bse['prbarr']:.3f})",
        format_coef(model3.pvalues['density'], model3.params['density']) + f" ({model3.bse['density']:.3f})",
        format_coef(model3.pvalues['urban'], model3.params['urban']) + f" ({model3.bse['urban']:.3f})"
    ],
    'Model 4 Coef (SE)': [
        format_coef(model4.pvalues['Intercept'], model4.params['Intercept']) + f" ({model4.bse['Intercept']:.3f})",
        format_coef(model4.pvalues['prbarr'], model4.params['prbarr']) + f" ({model4.bse['prbarr']:.3f})",
        '',
        format_coef(model4.pvalues['urban'], model4.params['urban']) + f" ({model4.bse['urban']:.3f})"
    ]
}

summary_df = pd.DataFrame(results)

# Add additional statistics to the summary DataFrame
additional_stats = {
    'Variable': ['R-squared', 'Adj. R-squared', 'N'],
    'Model 1 Coef (SE)': [f"{model1.rsquared:.3f}", f"{model1.rsquared_adj:.3f}", f"{int(model1.nobs)}"],
    'Model 2 Coef (SE)': [f"{model2.rsquared:.3f}", f"{model2.rsquared_adj:.3f}", f"{int(model2.nobs)}"],
    'Model 3 Coef (SE)': [f"{model3.rsquared:.3f}", f"{model3.rsquared_adj:.3f}", f"{int(model3.nobs)}"],
    'Model 4 Coef (SE)': [f"{model4.rsquared:.3f}", f"{model4.rsquared_adj:.3f}", f"{int(model4.nobs)}"]
}

additional_stats_df = pd.DataFrame(additional_stats)

# Combine both DataFrames
final_df = pd.concat([summary_df, additional_stats_df], ignore_index=True)

# Step (e): Display the table as an image
fig, ax = plt.subplots(figsize=(12, 6))  # set size frame
ax.xaxis.set_visible(False)  # hide the x-axis
ax.yaxis.set_visible(False)  # hide the y-axis
ax.set_frame_on(False)  # no visible frame

# Create a table
table_data = final_df.values.tolist()
column_labels = final_df.columns.tolist()
table = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

# Add a title
plt.title('Regression Results Summary', fontsize=16)

# Save the table as an image
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw3/regression_results_summary.png')
plt.show()

print("Regression results have been saved to regression_results_summary.png")
