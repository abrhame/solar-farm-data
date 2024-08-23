import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from pandas.plotting import scatter_matrix


def calc(data, location):
    # Define the logic for summary statistics
    summary_stats = data.describe()  # Example placeholder logic
    return summary_stats


def check_outliers(data, location):
    # Assuming 'data' is a DataFrame and you want to check for outliers in all numerical columns
    outliers = {}
    for column in data.select_dtypes(include=['float64', 'int64']).columns:
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers[column] = data[(data[column] < lower_bound) | (data[column] > upper_bound)].shape[0]
    
    return outliers


def check_negative_values(data, location):
    negative_values = {}
    for column in data.select_dtypes(include=['float64', 'int64']).columns:
        count_negatives = (data[column] < 0).sum()
        if count_negatives > 0:
            negative_values[column] = count_negatives
    
    return negative_values

def check_missing_values(data, location):
    # Get the count of missing values for each column
    missing_values = data.isnull().sum()
    missing_summary = missing_values[missing_values > 0]  # Show only columns with missing values
    return missing_summary


def plot_time_series(data, country_name):
    data = data.head(1000)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    fig, ax = plt.subplots()
    ax.plot(data['Timestamp'], data[data.columns[1]])  # Replace `data.columns[1]` with the column you want to plot
    ax.set_title(f"{country_name} Time Series")
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Values')
    fig.autofmt_xdate()  # Improve date label readability
    return fig


def plot_area(data, title):
    data = data.head(1000).copy()
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data.sort_values('Timestamp', inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.fill_between(data['Timestamp'], data['GHI'], color="lightblue", alpha=0.4, label='GHI')
    ax.fill_between(data['Timestamp'], data['DNI'], color="lightcoral", alpha=0.4, label='DNI')
    ax.fill_between(data['Timestamp'], data['DHI'], color="lightgreen", alpha=0.4, label='DHI')

    ax.plot(data['Timestamp'], data['GHI'], color="blue", alpha=0.8)
    ax.plot(data['Timestamp'], data['DNI'], color="red", alpha=0.8)
    ax.plot(data['Timestamp'], data['DHI'], color="green", alpha=0.8)

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Values')

    # Set xticks and labels
    ticks = ax.get_xticks()
    ax.set_xticks(ticks)  # Ensure ticks are set before labels
    ax.set_xticklabels([pd.to_datetime(tick).strftime('%Y-%m-%d') for tick in ticks], rotation=45)

    fig.tight_layout()
    return fig

def evaluate_cleaning_impact(data, timestamp_col='Timestamp', cleaning_col='Cleaning', modA_col='ModA', modB_col='ModB'):
    data = data.head(1000).copy()  # Avoid modifying slices
    data[timestamp_col] = pd.to_datetime(data[timestamp_col])
    data[cleaning_col] = data[cleaning_col].astype(bool)
    
    # Use infer_objects to ensure future compatibility
    data['Period'] = data[cleaning_col].shift(1).fillna(False).astype(int).cumsum().infer_objects()

    fig, ax = plt.subplots(2, 1, figsize=(14, 10))

    # Plot for ModA
    for key, grp in data.groupby(['Period']):
        ax[0].plot(grp[timestamp_col], grp[modA_col], label=f'Period {key}')
    ax[0].set_title(f'Impact of Cleaning on {modA_col} Readings Over Time')
    ax[0].set_xlabel('Timestamp')
    ax[0].set_ylabel(modA_col)
    ax[0].legend()

    # Plot for ModB
    for key, grp in data.groupby(['Period']):
        ax[1].plot(grp[timestamp_col], grp[modB_col], label=f'Period {key}')
    ax[1].set_title(f'Impact of Cleaning on {modB_col} Readings Over Time')
    ax[1].set_xlabel('Timestamp')
    ax[1].set_ylabel(modB_col)
    ax[1].legend()

    fig.tight_layout()
    return fig

def correlation_analysis(data):
    data = data.head(1000)
    solar_temp_columns = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB']
    wind_columns = ['WS', 'WSgust', 'WD']

    # Create a figure with 1 row and 2 columns
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

    # Plot heatmap of correlations
    solar_temp_corr = data[solar_temp_columns].corr()
    sns.heatmap(solar_temp_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax[0])
    ax[0].set_title('Correlation Heatmap: Solar Radiation and Temperature Measures')

    # Plot pair plot (create as separate figure)
    pair_plot = sns.pairplot(data[solar_temp_columns])
    pair_plot.fig.suptitle('Pair Plot: Solar Radiation and Temperature Measures', y=1.02)
    
    # Use `plt.show()` to display pair plot in Streamlit
    plt.close(pair_plot.fig)  # Prevents it from showing in the output
    return fig



def wind_analysis(data, ws_col='WS', wd_col='WD', title='Wind Speed and Direction Analysis'):
    data = data.head(1000).copy()  # Make a copy to avoid SettingWithCopyWarning
    data['Wind_Direction_Radians'] = np.deg2rad(data[wd_col])
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, polar=True)

    sc = ax.scatter(data['Wind_Direction_Radians'], data[ws_col], 
                    c=data[ws_col], cmap='viridis', alpha=0.75)

    plt.colorbar(sc, label='Wind Speed (m/s)')
    ax.set_title(title, va='bottom')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    fig.tight_layout()
    
    return fig


def temperature_analysis(data):
    data = data.head(1000)
    fig, ax = plt.subplots(2, 2, figsize=(16, 10))

    sns.scatterplot(x=data['RH'], y=data['TModA'], ax=ax[0, 0])
    ax[0, 0].set_title('Relative Humidity vs TModA')
    ax[0, 0].set_xlabel('Relative Humidity (%)')
    ax[0, 0].set_ylabel('Temperature (TModA)')

    sns.scatterplot(x=data['RH'], y=data['TModB'], ax=ax[0, 1])
    ax[0, 1].set_title('Relative Humidity vs TModB')
    ax[0, 1].set_xlabel('Relative Humidity (%)')
    ax[0, 1].set_ylabel('Temperature (TModB)')

    sns.scatterplot(x=data['RH'], y=data['GHI'], ax=ax[1, 0])
    ax[1, 0].set_title('Relative Humidity vs GHI')
    ax[1, 0].set_xlabel('Relative Humidity (%)')
    ax[1, 0].set_ylabel('Global Horizontal Irradiance (GHI)')

    sns.scatterplot(x=data['RH'], y=data['DNI'], ax=ax[1, 1])
    ax[1, 1].set_title('Relative Humidity vs DNI')
    ax[1, 1].set_xlabel('Relative Humidity (%)')
    ax[1, 1].set_ylabel('Direct Normal Irradiance (DNI)')

    fig.tight_layout()
    return fig



def plot_histograms(data):
    data = data.head(1000)  # Limit data to 1000 rows
    variables = ['GHI', 'DNI', 'DHI', 'WS', 'TModA', 'TModB']

    fig, ax = plt.subplots(2, 3, figsize=(15, 10))

    for i, var in enumerate(variables, start=1):
        sns.histplot(data[var], kde=True, bins=30, color='skyblue', ax=ax[(i-1)//3, (i-1)%3])
        ax[(i-1)//3, (i-1)%3].set_title(f'Histogram of {var}')
        ax[(i-1)//3, (i-1)%3].set_xlabel(var)
        ax[(i-1)//3, (i-1)%3].set_ylabel('Frequency')

    fig.tight_layout()
    return fig
