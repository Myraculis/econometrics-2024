import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import skew, kurtosis
import os
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Set the file path for input and output
folder_path = "C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw5/"
data_file = os.path.join(folder_path, "Panel data - slum population.xlsx")

# Load the dataset
data = pd.read_excel(data_file)

# Strip any leading or trailing spaces from column names
data.columns = data.columns.str.strip()

# Ensure the dataset has all necessary columns
data.columns = data.columns.str.lower().str.replace(' ', '_')

# Convert relevant columns to numeric, coercing errors to NaN
numeric_cols = [
    'proportion_of_urban_population_living_in_slums', 
    'gdp_per_capita_us_dollars', 
    'gdp_growth', 
    'unemployment_rate', 
    'refugees_number', 
    'total_population', 
    'percent_urban', 
    'urbangrowth', 
    'popdensity', 
    'income_share_of_poorest_20_percent', 
    'gini', 
    'income_share_of_richest_10%', 
    'urban_poverty_rate', 
    'phones', 
    'internet', 
    'healthcare_spending_as_percent_of_gdp', 
    'infant_mortality_rate', 
    'hdi', 
    'government_effectiveness', 
    'political_stability'
]

data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values in the dependent or independent variable
data_clean = data.dropna(subset=['proportion_of_urban_population_living_in_slums', 'gdp_per_capita_us_dollars'])

# Define dependent and independent variables for regression
y = data_clean['proportion_of_urban_population_living_in_slums']
X = data_clean[['gdp_per_capita_us_dollars']]  # Main independent variable

# Standardize the independent variable
scaler = StandardScaler()
data_clean['gdp_per_capita_us_dollars_std'] = scaler.fit_transform(data_clean[['gdp_per_capita_us_dollars']])

# Use standardized variable for regression
X_std = sm.add_constant(data_clean['gdp_per_capita_us_dollars_std'])

# Pooled OLS regression with a single independent variable
pooled_ols_model_std = sm.OLS(y, X_std).fit()

# Print regression results for Pooled OLS
print("\nPooled OLS Regression Results (Standardized):")
print(pooled_ols_model_std.summary())

# Fixed effects regression with standardized variable
fixed_effects_model_std = smf.ols('proportion_of_urban_population_living_in_slums ~ gdp_per_capita_us_dollars_std + C(country) + C(year)', data=data_clean).fit()

# Print regression results for Fixed Effects
print("\nFixed Effects Regression Results (Standardized):")
print(fixed_effects_model_std.summary())

# Calculate VIF for standardized variables
X_vif = data_clean[['gdp_per_capita_us_dollars_std']]
X_vif = sm.add_constant(X_vif)

vif_data = pd.DataFrame()
vif_data["feature"] = X_vif.columns
vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]

print("\nVariance Inflation Factors:")
print(vif_data)

# Examine for outliers
sns.boxplot(x=data_clean['gdp_per_capita_us_dollars_std'])
plt.title('Boxplot of Standardized GDP Per Capita')
plt.show()
