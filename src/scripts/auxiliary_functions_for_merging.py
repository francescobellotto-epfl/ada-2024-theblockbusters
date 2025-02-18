# Function to print missing statistics for each column in the DataFrame
def print_missing_stats(df):
    print("total len:", len(df))
    for col in df.columns:
        print("missing " + col + ":", sum(df[col].isna()))

# Function to convert text to ASCII, removing any special characters or accents
def make_text_ASCII(text):    
    normalized_text = unicodedata.normalize('NFKD', text)
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return ascii_text

# List of characters to remove from strings
chars_to_remove = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
# Function to clean a string by removing specified characters and converting to lowercase
def clean_string(input_str):
    return make_text_ASCII(''.join([char for char in input_str if char not in chars_to_remove]).lower())

# Function to ensure the input is iterable (list or tuple)
def ensure_iterable(l):
    if isinstance(l, tuple) or isinstance(l, list):
        return l
    else:
        return [l]

# Function to create a unique key from a list of elements
def create_key(elements):
    elements = ensure_iterable(elements)
    output_list = []
    for el in elements:
        if pd.isna(el):
            return pd.NA
        else:
            output_list.append(clean_string(str(el)))
    key = "_".join(output_list)
    return key

# Function to create a series of keys based on specified columns in a DataFrame
def create_key_series(df, columns):
    columns = ensure_iterable(columns)
    return df.apply(lambda row: create_key([row[col] for col in columns]), axis=1)

# Function to extract the year from a string
def extract_year(text):
    try:
        x = int(text[:4])
        if 1750 <= x <= 2024:
            return x
        else:
            return pd.NA
    except:
        return pd.NA

# Function to check if a date string is in the format "YYYY-MM-DD"
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

# Function to merge two comma-separated strings, removing duplicates
def merge_comma_sep(str1, str2):
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

# Function to extract values from a JSON string (assumed to be a tuple-like dictionary)
def extract_from_tuple(text):
    try:
        text_dict = json.loads(text)
        output = ",".join(text_dict.values())
        if output == "":
            return pd.NA
        else:
            return output
    except:
        return pd.NA

# Function to convert a string to lowercase
def lowercase(x):
    try:
        return x.lower()
    except:
        return pd.NA

# Function to remove the word " language" from a string
def remove_language(x):
    try:
        return x.replace(" language", "")
    except:
        return pd.NA

# Function to select a release date from a comma-separated list, prioritizing dates that are not the first of the year
def select_date(dates):
    if pd.isna(dates) or dates == "":
        return pd.NA
    parts = dates.split(",")
    for part in parts:
        if not part[:10].endswith("-01-01"):
            return part[:10]
    return parts[0][:4]

# Function to map gender strings to codes ("M" for male, "F" for female)
def select_gender(x):
    if x == "male":
        return "M"
    elif x == "female":
        return "F"
    else:
        return pd.NA