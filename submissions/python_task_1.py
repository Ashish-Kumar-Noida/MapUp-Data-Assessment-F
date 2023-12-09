import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    for l in range(min(matrix.shape)):
        matrix.iloc[l, l] = 0
    
    return matrix


def get_type_count(df)->dict:

    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    count_df=df
    count_df['car_type'] = pd.cut(count_df['car'], bins=[-float('inf'), 15, 25, float('inf')],labels=['low', 'medium', 'high'], right=False)
    
    type = count_df['car_type'].value_counts().to_dict()
    sort = dict(sorted(type.items()))
    
    return sort



def get_bus_indices(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

    bus_mean = df['bus'].mean()
    bus_indices = df[df['bus'] > 2 * bus_mean].index.tolist()

    return bus_indices.sort()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    
    route_average = df.groupby('route')['truck'].mean()
    filtered_routes = route_average[route_average > 7].index.tolist()

    return filter_routes.sort()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    matrix1 = matrix.copy()
    matrix1[matrix > 20] = matrix1[matrix > 20] * 0.75
    matrix1[matrix <= 20] = matrix1[matrix <= 20] * 1.25
    
    return matrix1.round(1)


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start_time'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')
    df['end_time'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')
    df['time_duration'] = df['end_time'] - df['start_time']
    time_periods = df.groupby(['id', 'id_2'])['time_duration'].agg(['min', 'max'])
    
    full_week_duration = pd.Timedelta(days=7)
    incomplete_time = (time_periods['max'] - time_periods['min'] < full_week_duration)
    
    return incomplete_time



    #reading of data 1
dataset = 'datasets/dataset-1.csv'
data = pd.read_csv(dataset)

    #reading of data 2
dataset2 = 'datasets/dataset-2.csv'
data2 = pd.read_csv(dataset2)

    #Calling function of question 1
result_ques1=generate_car_matrix(data)
print(result_ques1)

    #Calling function of question 2
car_type_counts = get_type_count(data)
print("get_type_count : \n", car_type_counts)

    #Calling function of question 3
bus_indices = get_bus_indices(data)
print("get_bus_indices : \n", bus_indices)


    #Calling function of question 4
filtered_route_list = filter_routes(data)
print("filter_routes : \n",  filtered_route_list)

    #Calling function of question 5
modified_result_matrix = multiply_matrix(result_ques1)
print("multiply_matrix : \n",  modified_result_matrix)

    #Calling function of question 6
time_check_result = time_check(data2)
print("time_check : \n", time_check_result)