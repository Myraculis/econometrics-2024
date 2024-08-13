import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import skew, kurtosis
import os

# Set the file path for input and output
folder_path = "C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw5/"
data_file = os.path.join(folder_path, "Panel data - slum population.xlsx")

# Load the dataset
data = pd.read_excel(data_file)

# Strip any leading or trailing spaces from column names
data.columns = data.columns.str.strip()

# Ensure the dataset has all necessary columns
data.columns = data.columns.str.lower().str.replace(' ', '_')

# Check the column names to ensure they match
print("Column names in dataset:", data.columns)

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

# Calculate descriptive statistics for all numeric variables
desc_stats = data[numeric_cols].describe().transpose()

# Add skewness and kurtosis
desc_stats['skewness'] = data[numeric_cols].apply(lambda x: skew(x.dropna()))
desc_stats['kurtosis'] = data[numeric_cols].apply(lambda x: kurtosis(x.dropna()))

# Round all numbers to the nearest hundredth
desc_stats = desc_stats.round(2)

# Create the descriptive statistics table
desc_stats_table = desc_stats[['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']]

# Add title and footnote to the table
title = "Descriptive Statistics for All Variables"
footnote = """
Sources:
1. UN MDG Indicators: http://mdgs.un.org/unsd/mdg/Metadata.aspx
2. World Bank national accounts data: http://databank.worldbank.org/data/views/reports/metadataview.aspx
3. International Labour Organization Key Indicators: http://www.ilo.org/global/statistics-and-databases/lang--en/index.htm
4. United Nations World Urbanization Prospects: https://population.un.org/wup/
5. Food and Agriculture Organization and World Bank population estimates: http://www.fao.org/faostat/en/
6. United Nations High Commissioner for Refugees (UNHCR): www.unhcr.org/statistics/populationdatabase
7. United Nations Development Program: http://hdr.undp.org/en/data
8. Kaufmann, Daniel, Aart Kraay, and Massimo Mastruzzi. "The Worldwide Governance Indicators: Methodology and Analytical Issues." World Bank Policy Research Working Paper No. 5430 (2010).
9. UN Inter-agency Group for Child Mortality Estimation: www.childmortality.org
10. International Telecommunication Union World Telecommunication/ICT Development Report: https://www.itu.int/en/ITU-D/Statistics/Pages/stat/default.aspx
11. World Health Organization National Health Account database: http://apps.who.int/nha/database/DataExplorerRegime.aspx
"""

# Save descriptive statistics table as a PNG
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('tight')
ax.axis('off')
table_data = ax.table(cellText=desc_stats_table.values,
                      colLabels=desc_stats_table.columns,
                      rowLabels=desc_stats_table.index,
                      cellLoc='center',
                      loc='center')
table_data.auto_set_font_size(False)
table_data.set_fontsize(10)
plt.title(title)
plt.figtext(0.5, 0.01, footnote, wrap=True, horizontalalignment='center', fontsize=8)
plt.savefig(os.path.join(folder_path, 'descriptive_statistics_all.png'), bbox_inches='tight', dpi=300)
plt.show()

# Create histograms for key variables
relevant_vars = ['proportion_of_urban_population_living_in_slums', 'gdp_per_capita_us_dollars', 'unemployment_rate', 'urban_poverty_rate']

for var in relevant_vars:
    if var in data.columns:
        plt.figure(figsize=(10, 6))

        # Ensure data is numeric and drop NaN values
        numeric_data = pd.to_numeric(data[var], errors='coerce').dropna()

        ax = sns.histplot(numeric_data, kde=False, bins=15)
        plt.title(f'Histogram of {var.replace("_", " ").title()}')
        plt.xlabel(var.replace('_', ' ').title())
        plt.ylabel('Frequency')
        
        # Add labels above each bar
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height:.0f}', xy=(p.get_x() + p.get_width() / 2, height),
                        xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

        plt.savefig(os.path.join(folder_path, f'histogram_{var}.png'), bbox_inches='tight', dpi=300)
        plt.show()
    else:
        print(f"Variable '{var}' not found in the dataset.")

# Drop rows with missing values in the dependent or independent variable
data_clean = data.dropna(subset=['proportion_of_urban_population_living_in_slums', 'gdp_per_capita_us_dollars'])

# Define dependent and independent variables for regression
y = data_clean['proportion_of_urban_population_living_in_slums']
X = data_clean[['gdp_per_capita_us_dollars']]  # Main independent variable

# Add a constant to the independent variable
X = sm.add_constant(X)

# Pooled OLS regression with a single independent variable
pooled_ols_model = sm.OLS(y, X).fit()

# Print regression results for Pooled OLS
print("\nPooled OLS Regression Results:")
print(pooled_ols_model.summary())

# Fixed effects regression with a single independent variable
fixed_effects_model = smf.ols('proportion_of_urban_population_living_in_slums ~ gdp_per_capita_us_dollars + C(country) + C(year)', data=data_clean).fit()

# Print regression results for Fixed Effects
print("\nFixed Effects Regression Results:")
print(fixed_effects_model.summary())

# Create tables for comparison
pooled_ols_results = {
    'coef': pooled_ols_model.params,
    'std err': pooled_ols_model.bse,
    't': pooled_ols_model.tvalues,
    'P>|t|': pooled_ols_model.pvalues
}

fixed_effects_results = {
    'coef': fixed_effects_model.params,
    'std err': fixed_effects_model.bse,
    't': fixed_effects_model.tvalues,
    'P>|t|': fixed_effects_model.pvalues
}

# Convert to DataFrame for better display
pooled_ols_df = pd.DataFrame(pooled_ols_results)
fixed_effects_df = pd.DataFrame(fixed_effects_results)

# Combine the two DataFrames for side-by-side comparison
combined_results = pd.concat([pooled_ols_df, fixed_effects_df], axis=1, keys=['Pooled OLS', 'Fixed Effects'])

# Print the combined table
print("\nCombined Regression Results:")
print(combined_results)



