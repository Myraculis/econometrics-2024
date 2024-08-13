import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load the dataset
file_path = 'C:/Users/esfbb/OneDrive/Desktop/Code/econometrics/hw4/cps_2008.xlsx'  # Update the path as needed
data = pd.read_excel(file_path)

# Properly label the variables
data.columns = ['wage', 'educ', 'age', 'exper', 'female', 'black', 'white', 'married', 'union', 'northeast', 'midwest', 'south', 'west', 'fulltime', 'metro']

# Run the regression of wage on educ
X = data['educ']
y = data['wage']
X = sm.add_constant(X)  # Adds a constant term to the predictor

model = sm.OLS(y, X).fit()
predictions = model.predict(X)

# Print the regression results
print(model.summary())

# Plot the data and the fitted regression line
plt.figure(figsize=(10, 6))
plt.scatter(data['educ'], data['wage'], alpha=0.5, label='Data points')
plt.plot(data['educ'], predictions, color='red', label='Fitted regression line')
plt.xlabel('Years of Education')
plt.ylabel('Wage')
plt.title('Wage vs. Years of Education')
plt.legend()
plt.grid(True)
plt.show()
