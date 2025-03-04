# -*- coding: utf-8 -*-
"""Preferably.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1beEHmsoM2_EFOe91OQeXwmQsCxXl7Yw5
"""

# Kasibhatla Shamily Jennymoor_MLC70
# Supress Warnings

import warnings
warnings.filterwarnings('ignore')

# Import necessary libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
from sklearn.metrics import r2_score

# Read the data from csv file

df = pd.read_csv('day.csv')

# Check the head of the dataset

df.head()

# checking the shape of dataframe

df.shape

# describing the columns of dataframe

df.describe()

# get the info about columns

df.info()

# checking for the null values in column data

df.isnull().sum()

# renaming few columns for better readibility

df.rename(columns={'yr':'year','mnth':'month','hum':'humidity'}, inplace=True)

# Check the head of the dataset

df.head()

# Check the head of the dataset

df.head()

# Copying the dataframe into new

df_copy = df.copy()

# checking the shape of new dataframe

df_copy.shape

# dropping the duplicates

df_copy.drop_duplicates(inplace=True)

# re-verifying the shape of new dataframe

df_copy.shape

"""#### As the shape is same after dropping duplicates, that means there are no duplicates in the original dataframe as well."""

# dropping the unwanted columns
# instant has only index for the row, dteday has date which can be compensated by year and month column,
# casual and registered seems to be the breakup by category for cnt column.

df.drop(['instant','dteday','casual','registered'],axis=1,inplace=True)

# Encoding/mapping the season column

df.season = df.season.map({1:'spring', 2:'summer', 3:'fall', 4:'winter'})

# Encoding/mapping the month column

df.month = df.month.map({1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'june',7:'july',8:'aug',9:'sep',10:'oct',11:'nov',12:'dec'})

# Encoding/mapping the weekday column

df.weekday = df.weekday.map({0:'sun',1:'mon',2:'tue',3:'wed',4:'thu',5:'fri',6:'sat'})

# Encoding/mapping the weathersit column

df.weathersit = df.weathersit.map({1:'Clear',2:'Misty',3:'Light_snowrain',4:'Heavy_snowrain'})

# check the head of the dataset

df.head()

df.info()

"""## Step 2: Visualising the Data"""

# Analysing/visualizing the categorical columns
# to see how predictor variable stands against the target variable

plt.figure(figsize=(20, 12))
plt.subplot(2,4,1)
sns.boxplot(x = 'season', y = 'cnt', data = df)
plt.subplot(2,4,2)
sns.boxplot(x = 'month', y = 'cnt', data = df)
plt.subplot(2,4,3)
sns.boxplot(x = 'weekday', y = 'cnt', data = df)
plt.subplot(2,4,4)
sns.boxplot(x = 'weathersit', y = 'cnt', data = df)
plt.subplot(2,4,5)
sns.boxplot(x = 'holiday', y = 'cnt', data = df)
plt.subplot(2,4,6)
sns.boxplot(x = 'workingday', y = 'cnt', data = df)
plt.subplot(2,4,7)
sns.boxplot(x = 'year', y = 'cnt', data = df)
plt.show()

def plot_cat_columns(column):
    plt.figure(figsize = (12,6))
    plt.subplot(1,2,1)
    sns.barplot(x=column, y='cnt', data=df) # Pass column and 'cnt' as x and y
    plt.subplot(1,2,2)
    sns.barplot(x=column, y='cnt', data=df, hue='year',palette='Set1') # Pass column and 'cnt' as x and y
    plt.legend(labels=['2018', '2019'])
    plt.show()

# plotting visualization for season column

plot_cat_columns('season')

"""Fall season seems to have attracted more booking. And, in each season the booking count has increased drastically from 2018 to 2019."""

# plotting visualization for month column

plot_cat_columns('month')

"""Most of the bookings has been done during the month of may, june, july, aug, sep and oct.Trend increased starting of the year tillmid of the year and then it started decreasing as we approached the end of year.
Number of booking for each month seems to have increased from 2018 to 2019.
"""

# plotting visualization for weathersit column

plot_cat_columns('weathersit')

"""Clear weather attracted more booking which seems obvious. And in comparison to previous year, i.e 2018, booking increased for each weather situation in 2019."""

# plotting visualization for weekday column

plot_cat_columns('weekday')

"""Thu, Fir, Sat and Sun have more number of bookings as compared to the start of the week."""

# plotting visualization for holiday column

plot_cat_columns('holiday')

"""When its not holiday, booking seems to be less in number which seems reasonable as on holidays, people may want to spend time at home and enjoy with family."""

# plotting visualization for workingday column

plot_cat_columns('workingday')

"""Booking seemed to be almost equal either on working day or non-working day. But, the count increased from 2018 to 2019."""

# plotting visualization for year column

plot_cat_columns('year')

"""2019 attracted more number of booking from the previous year, which shows good progress in terms of business."""

# Analysing/visualizing the numerical columns

sns.pairplot(data=df,vars=['temp','atemp','humidity','windspeed','cnt'])
plt.show()

# Checking the correlation between the numerical variables

plt.figure(figsize = (6,6))
matrix = np.triu(df[['temp','atemp','humidity','windspeed','cnt']].corr())
sns.heatmap(df[['temp','atemp','humidity','windspeed','cnt']].corr(), annot = True, cmap="RdYlGn", mask=matrix)
plt.title("Correlation between Numerical Variables")
plt.show()

"""#### There is linear relationship between temp and atemp. Both of the parameters cannot be used in the model due to multicolinearity. We will decide which parameters to keep based on VIF and p-value w.r.t other variables

## Step 3: Data Preparation
"""

# Dummy variable creation for month, weekday, weathersit and season variables.

months_df=pd.get_dummies(df.month,drop_first=True)
weekdays_df=pd.get_dummies(df.weekday,drop_first=True)
weathersit_df=pd.get_dummies(df.weathersit,drop_first=True)
seasons_df=pd.get_dummies(df.season,drop_first=True)

df.head()

# Merging  the dataframe, with the dummy variable dataset.

df_new = pd.concat([df,months_df,weekdays_df,weathersit_df,seasons_df],axis=1)

df_new.head()

df_new.info()

# dropping unnecessary columns as we have already created dummy variable out of it.

df_new.drop(['season','month','weekday','weathersit'], axis = 1, inplace = True)

# check the head of new dataframe

df_new.head()

# check the shape of new dataframe

df_new.shape

# check the column info of new dataframe

df_new.info()

"""## Step 4: Splitting the Data into Training and Testing Sets"""

# splitting the dataframe into Train and Test

np.random.seed(0)
df_train, df_test = train_test_split(df_new, train_size = 0.7, random_state = 100)

# check the shape of training datatset

df_train.shape

# check the shape of testing datatset

df_test.shape

# Using MinMaxScaler to Rescaling the features

scaler = MinMaxScaler()

# verifying the head of dataset before scaling.

df_train.head()

# Apply scaler() to all the columns except the 'yes-no' and 'dummy' variables

num_vars = ['temp','atemp','humidity','windspeed','cnt']
df_train[num_vars] = scaler.fit_transform(df_train[num_vars])

# verifying the head after appying scaling.

df_train.head()

# describing the dataset

df_train.describe()

# check the correlation coefficients to see which variables are highly correlated

plt.figure(figsize = (25,25))
matrix = np.triu(df_train.corr())
sns.heatmap(df_train.corr(), annot = True, cmap="RdYlGn", mask=matrix)
plt.show()

"""#### cnt seems to have correlation with year variable and temp. Similarly, Misty and humidity show correlation. Spring season with Jan and Feb month, Summer season with may month and Winter season with oct and nov month show good correlation."""

# Visualizing one of the correlation to see the trends via Scatter plot.

plt.figure(figsize=[3,3])
plt.scatter(df_train.temp, df_train.cnt)
plt.show()

"""# Visualizing one of the correlation to see the trends via Scatter plot.

"""

# Building the Linear Model

y_train = df_train.pop('cnt')
X_train = df_train

# Recursive feature elimination

lm = LinearRegression()
lm.fit(X_train, y_train)

rfe = RFE(lm, n_features_to_select=15)
rfe = rfe.fit(X_train, y_train)

#List of variables selected in top 15 list

list(zip(X_train.columns,rfe.support_,rfe.ranking_))

# selecting the selected variable via RFE in col list

col = X_train.columns[rfe.support_]
print(col)

# checking which columns has been rejected

X_train.columns[~rfe.support_]

# Generic function to calculate VIF of variables

def calculateVIF(df):
    vif = pd.DataFrame()
    vif['Features'] = df.columns
    vif['VIF'] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    vif['VIF'] = round(vif['VIF'], 2)
    vif = vif.sort_values(by = "VIF", ascending = False)
    return vif

# dataframe with RFE selected variables

X_train_rfe = X_train[col]

# Generic function to calculate VIF of variables
def calculateVIF(df):
    vif = pd.DataFrame()

    # Convert the DataFrame to numeric types before calculating VIF
    df_numeric = df.select_dtypes(include=np.number)

    # Exclude features representing categorical information
    categorical_features = ['year', 'holiday', 'workingday']
    df_numeric = df_numeric.drop(columns=categorical_features, errors='ignore')

    # Initialize 'Features' with the correct columns after filtering
    vif['Features'] = df_numeric.columns

    vif['VIF'] = [variance_inflation_factor(df_numeric.values, i) for i in range(df_numeric.shape[1])]
    vif['VIF'] = round(vif['VIF'], 2)
    vif = vif.sort_values(by="VIF", ascending=False)
    return vif

# Calculate VIF and display the result
vif_result = calculateVIF(X_train_rfe)
print(vif_result)
display(vif_result)

"""humidity shows high VIF value.

## Step 5: Building a linear model
"""

import statsmodels.api as sm
import pandas as pd
import numpy as np

# Convert categorical columns
X_train_rfe = pd.get_dummies(X_train_rfe, drop_first=True)

# Handle missing values
X_train_rfe = X_train_rfe.fillna(X_train_rfe.mean())

# Ensure all data is numeric
X_train_rfe = X_train_rfe.astype(float)

# Add constant
X_train_lm_1 = sm.add_constant(X_train_rfe)

# Fit Linear Regression Model
lr_1 = sm.OLS(y_train, X_train_lm_1).fit()

print(lr_1.summary())

import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Ensure X_train_new is initialized
X_train_new = X_train.copy()

# Drop the 'jan' column if it exists
if 'jan' in X_train_new.columns:
    X_train_new = X_train_new.drop(['jan'], axis=1)
else:
    print("Column 'jan' not found in X_train_new")

# Convert categorical variables to numeric
X_train_new = pd.get_dummies(X_train_new, drop_first=True)

# Handle missing values (if any)
X_train_new = X_train_new.fillna(X_train_new.mean())

# Convert all columns to float to ensure numerical computations
X_train_new = X_train_new.astype(float)

# Function to calculate VIF
def calculateVIF(df):
    vif_data = pd.DataFrame()
    vif_data["Feature"] = df.columns
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    return vif_data

# Calculate and print VIF
print(calculateVIF(X_train_new))

# Building 5th linear regression model

X_train_lm_5 = sm.add_constant(X_train_new)
lr_5 = sm.OLS(y_train,X_train_lm_5).fit()
print(lr_5.summary())

# We can drop july variable as it has high p-value
X_train_new = X_train_new.drop(['july'], axis = 1)

# Run the function to calculate VIF for the new model
calculateVIF(X_train_new)

"""VIF value now seems to be good as it came below 5."""

# Building 6th linear regression model

X_train_lm_6 = sm.add_constant(X_train_new)
lr_6 = sm.OLS(y_train,X_train_lm_6).fit()
print(lr_6.summary())

"""#### We can cosider the above model i.e lr_6, as it seems to have very low multicolinearity between the predictors and the p-values for all the predictors seems to be significant.

#### F-Statistics value of 248.4 (which is greater than 1) and the p-value of 1.47e-186 i.e almost equals to zero, states that the overall model is significant
"""

# Checking the parameters and their coefficient values
lr_6.params

"""## Step 6: Residual Analysis of the train data and validation"""

X_train_lm_6

y_train_pred = lr_6.predict(X_train_lm_6)

# Plot the histogram of the error terms

fig = plt.figure()
sns.distplot((y_train - y_train_pred), bins = 20)
fig.suptitle('Error Terms', fontsize = 20)
plt.xlabel('Errors', fontsize = 18)

"""Error terms are following normal distribution

#### Multi Colinearity
"""

calculateVIF(X_train_new)

plt.figure(figsize=(15,8))
sns.heatmap(X_train_new.corr(),annot = True, cmap="RdYlGn")
plt.show()

#### Linearity

# Linear relationship validation using CCPR plot
# Component and component plus residual plot

sm.graphics.plot_ccpr(lr_6, 'temp')
plt.show()

sm.graphics.plot_ccpr(lr_6, 'sep')
plt.show()

sm.graphics.plot_ccpr(lr_6, 'windspeed')
plt.show()

"""Linearity can be observed from above visualizations.

#### Homoscedasticity
"""

import seaborn as sns
import matplotlib.pyplot as plt

y_train_pred = lr_6.predict(X_train_lm_6)
residual = y_train - y_train_pred

# Corrected scatter plot
sns.scatterplot(x=y_train, y=residual)

# Corrected residual line plot
plt.plot(y_train, [0] * len(y_train), '-r')

plt.xlabel('Count')
plt.ylabel('Residual')
plt.title('Residual Plot')
plt.show()

"""No visible pattern observed from above plot for residuals.

#### Independence of residuals

Durbin-Watson value of final model lr_6 is 2.085, which signifies there is no autocorrelation.

## Step 7: Making Predictions Using the Final Model

Now that we have fitted the model and checked the normality of error terms, it's time to go ahead and make predictions using the final, i.e. 6th model.
"""

# Applying scaling on the test dataset

num_vars = ['temp', 'atemp', 'humidity', 'windspeed','cnt']
df_test[num_vars] = scaler.transform(df_test[num_vars])
df_test.head()

df_test.describe()

y_test = df_test.pop('cnt')
X_test = df_test

col1 = X_train_new.columns

X_test = X_test[col1]

# Adding constant variable to test dataframe
X_test_lm_6 = sm.add_constant(X_test)

y_pred = lr_6.predict(X_test_lm_6)

r2 = r2_score(y_test, y_pred)
round(r2,4)

"""## Step 8: Model Evaluation

Let's now plot the graph for actual versus predicted values.
"""

# Plotting y_test and y_pred to understand the spread

fig = plt.figure()
plt.scatter(y_test, y_pred)
fig.suptitle('y_test vs y_pred', fontsize = 20)
plt.xlabel('y_test', fontsize = 18)
plt.ylabel('y_pred', fontsize = 16)

round(lr_6.params,4)

"""We can see that the equation of our best fitted line is:

$ cnt = 0.1909 + 0.2341  \times  year - 0.0963  \times  holiday + 0.4777 \times temp - 0.1481 \times windspeed + 0.0910 \times sep - 0.2850 \times Light_snowrain - 0.0787 \times Misty - 0.0554 \times spring + 0.0621 \times summer + 0.0945 \times winter $
"""

# Calculating Adjusted-R^2 value for the test dataset

adjusted_r2 = round(1-(1-r2)*(X_test.shape[0]-1)/(X_test.shape[0]-X_test.shape[1]-1),4)
print(adjusted_r2)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Convert to numeric
y_test = pd.to_numeric(y_test, errors='coerce')
y_pred = np.array(y_pred, dtype=np.float64)

# Remove NaN and infinite values
valid_indices = ~np.isnan(y_test) & ~np.isnan(y_pred) & np.isfinite(y_pred)
y_test = y_test[valid_indices]
y_pred = y_pred[valid_indices]

# Plot regression plot
plt.figure()
sns.regplot(x=y_test, y=y_pred, ci=68, scatter_kws={"color": "blue"}, line_kws={"color": "red"})
plt.title('y_test vs y_pred', fontsize=20)
plt.xlabel('y_test', fontsize=18)
plt.ylabel('y_pred', fontsize=16)
plt.show()

"""# Comparision between Training and Testing dataset:
    - Train dataset R^2          : 0.833
    - Test dataset R^2           : 0.8038
    - Train dataset Adjusted R^2 : 0.829    
    - Test dataset Adjusted R^2  : 0.7944

#### Demand of bikes depend on year, holiday, temp, windspeed, sep, Light_snowrain, Misty, spring, summer and winter.
"""