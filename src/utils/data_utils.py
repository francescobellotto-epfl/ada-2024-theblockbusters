import numpy as np
import pandas as pd

def merge_movies_cast(pivot_df, cast_df, movies_df, 
                      cast_key_pivot, cast_key_right, movie_key_pivot, 
                      movie_key_right, columns, role_col, role='any'):
    """
    Merge movies dataset with cast datasets exploiting a "pivot"
    dataset connecting the two.

    Args:
        pivot_df: pandas DataFrame connecting the other two by keys
        cast_df: pandas DataFrame of cast members
        movies_df: pandas DataFrame of movies
        cast_key_pivot: name of column of cast members'keys in 
        pivot_df
        cast_key_right: name of column of cast members'keys in 
        cast_df
        movie_key_pivot: name of column of movies'keys in 
        pivot_df
        movie_key_right: name of column of movies'keys in 
        movies_df
        columns: columns to keep in final dataframe
        role_col: name of column specifying role in piovt_df
        role: role to consider ('actor', 'director' or 'any')
        (default 'any')

    Returns:
        merged_df: pandas merged DataFrame

    """
    
    try:
        # Consider only specified roles
        if role == 'any':
            temp = pivot_df.dropna(subset=cast_key_pivot)
        elif role in pivot_df[role_col].unique():
            temp = pivot_df[pivot_df[role_col]==role]. \
            dropna(subset=cast_key_pivot)
        else:
            raise Exception("Please provide a valid role ('actor', 'director' or 'any')")
    except:
        Exception("Verify that role_col is a valid column of pivot_df")
    
    try:
        # Merge actors with movies-actors mapping
        movies_and_actors = pd.merge(temp[[movie_key_pivot, cast_key_pivot]], 
                                cast_df.dropna(subset=cast_key_right). \
                                drop_duplicates(subset=cast_key_right), 
                                left_on=cast_key_pivot, right_on=cast_key_right)
    except:
        raise Exception("Verify that movie_key_pivot and cast_key_pivot are valid columns for",
                        "pivot_df and that cast_key_right is valid for cast_df")
    
    try:
        # Merge this with movies
        movies_and_actors = pd.merge(movies_and_actors, movies_df, 
                                    left_on=movie_key_pivot, right_on=movie_key_right)
    except:
        raise Exception("Verify that movie_key_pivot is a valid column for",
                        "pivot_df and that movie_key_right is valid for movies_df")
    
    try:
        # Consider only relevant columns
        movies_and_actors = movies_and_actors[columns]
    except:
        raise Exception("Verify that all columns exist.")

    # Drop completely duplicated rows based only on selected features
    movies_and_actors = movies_and_actors.drop_duplicates()

    return movies_and_actors

def compute_age(df, birth_year_col, release_year_col, new_col, liminf=18, limsup=70):
    """
    Compute age of actors/directors when a movie they appear 
    in was released.

    Args:
        df: pandas DataFrame
        birth_year_col: name of column indicating the person 
        year of birth
        release_year_col: name of column indicating the release 
        year
        new_col: name of the new column
        liminf/limsup: extreme age values (default 18/85)

    Returns:
        df: modified DataFrame

    """
    new_data = df.copy()

    if birth_year_col not in new_data.columns or release_year_col not in new_data.columns:
        raise Exception("Check the name of columns")
    
    # Compute age at movie release
    new_data[new_col] = new_data[release_year_col] - new_data[birth_year_col]

    # Exclude values that don't make sense
    new_data[new_col] = new_data[new_col].apply(lambda x: x if x>=liminf and x<=limsup else np.nan)

    return new_data

def bootstrap(data1, data2):
    """
    Consider the shortest dataset, and bootstrap random values 
    from it to equal the length of the longest one.

    Args:
        data1: np.array or Pandas series
        data2: np.array or Pandas series

    Returns:
        shortest_data/longest_data: new datasets with equal 
        length

    """
    if len(data1)>len(data2):
        n = len(data1) - len(data2)
        longest_data = data1.copy()
        shortest_data = data2.copy()
    elif len(data2)>len(data1):
        n = len(data2) - len(data1)
        longest_data = data2.copy()
        shortest_data = data1.copy()
    else:
        return data1, data2
    
    samp = shortest_data.sample(n=n, random_state=1, replace=True)
    shortest_data = pd.concat([shortest_data, samp], ignore_index=True)

    return shortest_data, longest_data

def extract_primary_company(df, column, columns, n=0, add_count=True):
    """
    From the movies dataset, extract primary producer company 
    and sort all first n ones.

    Args:
        df: pandas DataFrame
        column: column representing the company
        columns: columns to have in the final dataset
        n: number of most relevant companies (default 0, i.e. 
        all companies)
        add_count: True if in the dataset also the number of 
        movies produced by company must be introduced (default 
        True)

    Returns:
        new_df: new DataFrame

    """
    if column not in df.columns:
        raise Exception(column, "is not in DataFrame columns")
    for col in columns:
        if col not in df.columns:
            raise Exception(col, "is not in DataFrame columns")
    try:
        n = int(n)
    except:
        raise Exception("Input a positive integer value for n")
    
    new_df = df.copy()
    try:
        new_df[column] = new_df[column].fillna('')
        col1_name = 'primary_' + column
        col2_name = 'secondary_' + column
        new_df[col1_name] = new_df[column].apply(lambda x: x.split(',')[0] if x else None)
        new_df[col2_name] = new_df[column].apply(lambda x: ','.join(x.split(',')[1:]) if ',' in x else None)
    except:
        print("Operation was not applied; check that it can be performed on the datatype")
        return new_df
    
    if col1_name not in columns:
        columns.extend([col1_name])

    if n==0:
        new_df['count'] = new_df[col1_name].map(new_df[col1_name].value_counts())
        new_df = new_df.sort_values(by='count', ascending=False)
        if not add_count:
            new_df = new_df[columns]
            return new_df
        else:
            columns.extend(['count'])
            new_df = new_df[columns]
            return new_df

    top_n = new_df[col1_name].value_counts().nlargest(n).index
    new_df = new_df[new_df[col1_name].isin(top_n)]
    counts = pd.DataFrame(new_df[col1_name].value_counts()).reset_index()
    new_df = pd.merge(new_df[columns], counts, left_on=col1_name, right_on=col1_name)
    new_df = new_df.sort_values(by='count', ascending=False)

    return new_df

def compute_roi(df, revenue_col, budget_col):
    """
    Compute ROI (Return On Investments).

    Args:
        df: pandas DataFrame
        revenue_col: valid column name for revenues
        budget_col: valid column name for budget

    Returns:
        new_df: modified DataFrame with ROI(%) column
    """

    if revenue_col not in df.columns or budget_col not in df.columns:
        raise Exception("Please enter valid column names")
    if 'roi_perctg' in df.columns:
        return df
    
    new_df = df
    new_df['roi_perctg'] = df.apply(lambda row: row[revenue_col]/row[budget_col]*100 if not np.isnan(row[revenue_col])
                                        and not np.isnan(row[budget_col])
                                        and row[budget_col]!=0 
                                        else np.nan, axis=1)
    return new_df

def create_quantile_col(dataset, col_name, quantiles):
    """
    Add a coulmn to dataset representing discrimination based 
    on passed quantiles.

    Args:
        dataset: Pandas DataFrame
        col_name: valid column name to discriminate on
        quantiles: list of quantiles to discriminat on

    Returns:
        dataset: updated DataFrama
    """
    
    if col_name not in dataset.columns:
        raise Exception("Please enter a valid column name")
    if 'quantile' in dataset.columns:
        print("Quantile column already present")
    qs = dataset[col_name].quantile(q=quantiles)
    qs = np.insert(qs, 0, np.min(dataset[col_name]))
    qs = np.append(qs, np.max(dataset[col_name]))
    dataset['quantile'] = np.zeros((len(dataset,)))
    dataset['quantile'] = (dataset[col_name]==qs[0])*1 + dataset['quantile']
    for idx in range(0,len(qs)-1):
        dataset['quantile'] = (dataset[col_name]>qs[idx])*(dataset[col_name]<=qs[idx+1])*(idx+1) + dataset['quantile']
    return dataset
   
def agg_bool(group):
    """
    Aggregate a group taking an or if the type is
    bool and taking the first element otherwise
    """
    agg_dict = {}
    for col in group.columns:
        if group[col].dtype == 'bool':
            agg_dict[col] = group[col].any()
        else:
            agg_dict[col] = group[col].iloc[0]
    return pd.Series(agg_dict)

def merge_comma_sep(str1, str2):
    """
    This function merges two sequences of comma separated
    lists, removing duplicates.
    """
    if pd.isna(str1) and pd.isna(str2):
        return pd.NA
    elif pd.isna(str1):
        return str2
    elif pd.isna(str2):
        return str1
    else:
        set1 = set(str1.split(","))
        set2 = set(str2.split(","))
        merged_set = set1.union(set2)
        return ",".join(merged_set)