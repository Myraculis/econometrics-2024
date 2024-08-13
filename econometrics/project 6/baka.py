import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
from sklearn.preprocessing import StandardScaler
from scipy.stats import skew, kurtosis

# Load the dataset from the specified file path
file_path = "C:\\Users\\esfbb\\OneDrive\\Desktop\\Code\\econometrics\\hw5.5\\Data - Extramarital affair.xlsx"
data = pd.read_excel(file_path)

# Display the first few rows of the dataset to understand its structure
print(data.head())

# Strip and lowercase the column names for consistency
data.columns = data.columns.str.strip().str.lower()

# Descriptive statistics for the dataset
desc_stats = data.describe().transpose()

# Calculate skewness and kurtosis
desc_stats['skewness'] = data.apply(lambda x: skew(x.dropna()), axis=0)
desc_stats['kurtosis'] = data.apply(lambda x: kurtosis(x.dropna()), axis=0)

# Drop the 'count' row from the descriptive statistics table
desc_stats = desc_stats.drop(columns=['count'])

# Round all values to the nearest thousandth
desc_stats = desc_stats.round(3)

print("\nDescriptive Statistics with Skewness and Kurtosis:")
print(desc_stats)

# Save descriptive statistics table as a PNG
fig, ax = plt.subplots(figsize=(12, 8))  # Set size for better readability
ax.axis('off')  # Hide axes
ax.axis('tight')  # Remove excess whitespace
table_data = ax.table(cellText=desc_stats.values,
                      colLabels=desc_stats.columns,
                      rowLabels=desc_stats.index,
                      cellLoc='center',
                      loc='center')
table_data.auto_set_font_size(False)
table_data.set_fontsize(8)
plt.title("Descriptive Statistics of Extramarital Affairs Dataset", fontsize=12)
plt.savefig("C:\\Users\\esfbb\\OneDrive\\Desktop\\Code\\econometrics\\hw5.5\\descriptive_statistics.png", bbox_inches='tight', dpi=300)
plt.show()

# Convert the dependent variable 'affair' to integer type
data['affair'] = data['affair'].astype(int)

# List the independent variables for the logit model
independent_vars = ['age', 'yrs_married', 'children', 'religious', 'educ', 'occupation', 'rate_marriage']

# Standardize continuous variables for better interpretation
scaler = StandardScaler()
data[['age', 'yrs_married', 'educ']] = scaler.fit_transform(data[['age', 'yrs_married', 'educ']])

# Define the formula for the logit model
formula = 'affair ~ age + yrs_married + children + religious + educ + occupation + rate_marriage'

# Estimate the logit model
logit_model = smf.logit(formula=formula, data=data).fit()

# Additional logit models for comparison (e.g., excluding some variables)
logit_model_2 = smf.logit('affair ~ age + yrs_married + religious + educ + rate_marriage', data=data).fit()
logit_model_3 = smf.logit('affair ~ age + yrs_married + children + religious', data=data).fit()

# Gather the results of these models in a side-by-side table
logit_results = summary_col([logit_model, logit_model_2, logit_model_3], 
                      model_names=["Full Model", "Reduced Model 1", "Reduced Model 2"],
                      stars=True, 
                      info_dict={'N': lambda x: f"{int(x.nobs)}",
                                 'Log-Lik': lambda x: f"{x.llf:.2f}",
                                 'Pseudo R-squared': lambda x: f"{x.prsquared:.2f}"})

print("\nSide-by-Side Logit Regression Results:")
print(logit_results)

# Calculate and store AME for all models
ame_model_1 = logit_model.get_margeff(at='overall')
ame_model_2 = logit_model_2.get_margeff(at='overall')
ame_model_3 = logit_model_3.get_margeff(at='overall')

# Extract AME results
ame_summary_1 = ame_model_1.summary_frame().round(4)
ame_summary_2 = ame_model_2.summary_frame().round(4)
ame_summary_3 = ame_model_3.summary_frame().round(4)

# Create a side-by-side table for AME results
ame_results_df = pd.concat([ame_summary_1['dy/dx'], ame_summary_2['dy/dx'], ame_summary_3['dy/dx']], axis=1)
ame_results_df.columns = ['Full Model AME', 'Reduced Model 1 AME', 'Reduced Model 2 AME']

print("\nAverage Marginal Effects (AME) for Different Models:")
print(ame_results_df)
