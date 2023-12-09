from datetime import datetime
import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    
    df = df.pivot(index='id_start', columns='id_end', values='distance')
    distance = df.fillna(0) + df.fillna(0).T
    
    return distance


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here

    distance_df = df.stack().reset_index()
    distance_df.columns = ['id_start', 'id_end', 'distance']
    distance_df = distance_df[distance_df['id_start'] != distance_df['id_end']]
    
    return distance_df




def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

    # threshold values 
    threshold_upper = reference_avg_distance * 1.1
    threshold_lower = reference_avg_distance * 0.9

    within_threshold_df = df.groupby('id_start')['distance'].mean().between(threshold_lower, threshold_upper)
    ids_within_threshold = df[df['id_start'].isin(within_threshold_df.index)]

    return ids_within_threshold



def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    
    for vehicle in rate_coefficients.keys():
        df[vehicle] = 0
    
    return df




def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here


    return df


    #read data from sheet 3
dataset3 = 'datasets/dataset-3.csv'
data = pd.read_csv(dataset3)

    #calling function of question 1
distance_matrix_result = calculate_distance_matrix(data)
print("\n", distance_matrix_result)

#calling function of question 2
unrolled_distance_result = unroll_distance_matrix(distance_matrix_result)
print("\n", unrolled_distance_result)

#calling function of question 3
reference_id = 1001400
ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_distance_result, reference_id)
print("\n",ids_within_threshold)

#calling function of question 4
toll_rate_result = calculate_toll_rate(unrolled_distance_result[['id_start', 'id_end']])
print("\n",toll_rate_result)

#calling function of question 5