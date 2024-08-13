import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import norm

# Step 1: Import the data
print("Task (a): Import the data")
data = pd.read_excel('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw2/CAPM.xlsx')
print(data.head())

# Step 2: Construct the variables (Calculating excess returns)
print("Task (b): Construct the variables")
data['ExR_Market'] = data['mkt'] - data['riskfree']
data['ExR_Microsoft'] = data['msft'] - data['riskfree']
data['ExR_GM'] = data['gm'] - data['riskfree']
data['ExR_MobilExxon'] = data['xom'] - data['riskfree']

# Drop the date column for the statistical analysis
data_analysis = data.drop(columns=['date'])

# Step 3: Descriptive statistics
print("Task (c): Construct a table of descriptive statistics")
descriptive_stats = data_analysis.describe().T
descriptive_stats['skewness'] = data_analysis.skew()
descriptive_stats['kurtosis'] = data_analysis.kurtosis()
descriptive_stats = descriptive_stats[['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']]
descriptive_stats.columns = ['mean', 'std dev', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']
descriptive_stats = descriptive_stats.round(2)
descriptive_stats[''] = ''  # Adding an extra blank column at the end
print(descriptive_stats)
descriptive_stats.to_csv('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw2/descriptive_stats.csv')

# Formatting the descriptive statistics table to match the provided example
fig, ax = plt.subplots(figsize=(14, 8))  # set size frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis
ax.set_frame_on(False)  # no visible frame

# Create a table from the DataFrame
table_data = descriptive_stats.reset_index().values.tolist()
column_labels = ["Variable", "mean", "std dev", "min", "25%", "50%", "75%", "max", "skewness", "kurtosis", ""]

table = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

# Add a title
plt.title('Monthly Rates of Return: Jan 1999 to December 2008', fontsize=16)

# Add a footnote
plt.figtext(0.5, 0.01, 'Source: Wharton Data Services', ha='center', fontsize=12, va='bottom')

# Adjust the layout
plt.subplots_adjust(left=0.2, top=0.8, right=0.95, bottom=0.1)
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw2/descriptive_stats.png')
plt.show()

# Step 4: Create histogram for Microsoft
print("Task (d): Create a histogram for Microsoft's excess returns")
plt.hist(data['ExR_Microsoft'], bins=20, edgecolor='black')
plt.title('Histogram of Excess Returns for Microsoft')
plt.xlabel('Excess Return')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw2/histogram_microsoft.png')
plt.show()

# Step 5: OLS Regression for each firm
print("Task (e): OLS Regression for each firm")

def run_regression(excess_return):
    X = data['ExR_Market']
    y = data[excess_return]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit(cov_type='HC3')  # Using heteroscedasticity-robust standard errors
    return model

# Running regressions
model_microsoft = run_regression('ExR_Microsoft')
model_gm = run_regression('ExR_GM')
model_mobil_exxon = run_regression('ExR_MobilExxon')

# Printing the regression results
print("\nMicrosoft Regression Results:")
print(model_microsoft.summary())
print("\nGM Regression Results:")
print(model_gm.summary())
print("\nMobilExxon Regression Results:")
print(model_mobil_exxon.summary())

# Extracting beta values
beta_microsoft = model_microsoft.params['ExR_Market']
beta_gm = model_gm.params['ExR_Market']
beta_mobil_exxon = model_mobil_exxon.params['ExR_Market']

# Printing and commenting on beta values
print("\nEstimated Beta Values:")
print(f"Microsoft Beta: {beta_microsoft:.2f}")
print(f"GM Beta: {beta_gm:.2f}")
print(f"MobilExxon Beta: {beta_mobil_exxon:.2f}")

# Determining which firm is most aggressive and which is most defensive
if beta_microsoft > beta_gm and beta_microsoft > beta_mobil_exxon:
    most_aggressive = "Microsoft"
elif beta_gm > beta_microsoft and beta_gm > beta_mobil_exxon:
    most_aggressive = "GM"
else:
    most_aggressive = "MobilExxon"

if beta_microsoft < beta_gm and beta_microsoft < beta_mobil_exxon:
    most_defensive = "Microsoft"
elif beta_gm < beta_microsoft and beta_gm < beta_mobil_exxon:
    most_defensive = "GM"
else:
    most_defensive = "MobilExxon"

print(f"\nMost Aggressive Firm: {most_aggressive}")
print(f"Most Defensive Firm: {most_defensive}")

# Step 6: Calculate fitted values and residuals for Microsoft
print("Task (f): Calculate fitted values and residuals for Microsoft")
data['fitted_microsoft'] = model_microsoft.fittedvalues
data['residuals_microsoft'] = model_microsoft.resid
data[['fitted_microsoft', 'residuals_microsoft']].to_csv('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw2/fitted_residuals_microsoft.csv')

# Scatter plot of residuals for Microsoft
print("Task (f): Scatter plot of residuals for Microsoft")
plt.scatter(data['ExR_Market'], data['residuals_microsoft'], edgecolor='black')
plt.title('Scatter Diagram of Residuals for Microsoft')
plt.xlabel('Excess Return Market')
plt.ylabel('Residuals')
plt.grid(True)
plt.savefig('C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw2/scatter_residuals_microsoft.png')
plt.show()

# Step 8: Hypothesis testing for beta
print("Task (g): Hypothesis testing for beta")
def test_beta(model):
    beta = model.params['ExR_Market']
    se = model.bse['ExR_Market']
    t_stat = (beta - 1) / se
    p_value = 2 * (1 - norm.cdf(abs(t_stat)))
    return t_stat, p_value

t_stat_microsoft, p_value_microsoft = test_beta(model_microsoft)
t_stat_gm, p_value_gm = test_beta(model_gm)
t_stat_mobil_exxon, p_value_mobil_exxon = test_beta(model_mobil_exxon)

print(f"Microsoft: t-stat={t_stat_microsoft}, p-value={p_value_microsoft}")
print(f"GM: t-stat={t_stat_gm}, p-value={p_value_gm}")
print(f"MobilExxon: t-stat={t_stat_mobil_exxon}, p-value={p_value_mobil_exxon}")
