import pandas as pd

def clean_data(df):
    # Drop column: 'Amount'
    df = df.drop(columns=['Amount'])
    # Performed 1 aggregation grouped on column: 'Filename'
    df = df.groupby(['Filename']).agg(Count_sum=('Count', 'sum')).reset_index()
    # Rename column 'Count_sum' to 'Total_Loans'
    df = df.rename(columns={'Count_sum': 'Total_Loans'})
    # Replace all instances of "data/|\\.csv" with "" in column: 'Filename'
    df['Filename'] = df['Filename'].str.replace("data/|\\.csv", "", case=False, regex=True)
    # Split text using string '-to-' in column: 'Filename'
    loc_0 = df.columns.get_loc('Filename')
    df_split = df['Filename'].str.split(pat='-to-', expand=True).add_prefix('Filename_')
    df = pd.concat([df.iloc[:, :loc_0], df_split, df.iloc[:, loc_0:]], axis=1)
    df = df.drop(columns=['Filename'])
    # Rename column 'Filename_0' to 'Start_Date'
    df = df.rename(columns={'Filename_0': 'Start_Date'})
    # Rename column 'Filename_1' to 'End_Date'
    df = df.rename(columns={'Filename_1': 'End_Date'})
    # Replace all instances of "(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)" with "\\3/\\2/\\1" in columns: 'End_Date', 'Start_Date'
    df['End_Date'] = df['End_Date'].str.replace("(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)", "\\3/\\2/\\1", case=False, regex=True)
    df['Start_Date'] = df['Start_Date'].str.replace("(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)", "\\3/\\2/\\1", case=False, regex=True)
    return df

# Loaded variable 'df' from URI: /home/damien/projects/ltl-usage-graph/data/collection.csv
df = pd.read_csv(r'/home/damien/projects/ltl-usage-graph/data/collection.csv', engine='pyarrow')

df_clean = clean_data(df.copy())
df_clean.to_csv(r'src/data/usage.csv', index=False)