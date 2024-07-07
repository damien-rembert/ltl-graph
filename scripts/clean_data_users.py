import pandas as pd


def clean_data(df):
    df = df.drop(columns=["Count", "Amount"])

    df = df.rename(columns={"Value": "User"})

    # Only keep users' first appearance
    df = (
        df.groupby(["User"])
        .agg(
            Start_Date_first=("Start_Date", "first"),
            End_Date_first=("End_Date", "first"),
        )
        .reset_index()
    )
    # Get total number of users of date range
    df = (
        df.groupby(["Start_Date_first", "End_Date_first"])
        .agg(New_Users=("User", "count"))
        .reset_index()
    )
    df = df.rename(
        columns={
            "Start_Date_first": "Start_Date",
            "End_Date_first": "End_Date",
        }
    )
    return df


def get_dates_from_filename(df):
    # Replace all instances of "data/user/|\\.csv" with "" in column: 'Filename'
    df["Filename"] = df["Filename"].str.replace(
        "data/user/|\\.csv", "", case=False, regex=True
    )
    # Split text using string '_to_' in column: 'Filename'
    loc_0 = df.columns.get_loc("Filename")
    df_split = df["Filename"].str.split(pat="_to_", expand=True).add_prefix("Filename_")
    df = pd.concat([df.iloc[:, :loc_0], df_split, df.iloc[:, loc_0:]], axis=1)
    df = df.drop(columns=["Filename"])
    # Rename columns 'Filename_0' to 'Start_Date'
    df = df.rename(columns={"Filename_0": "Start_Date", "Filename_1": "End_Date"})
    return df


df = pd.read_csv(r"data/user_collection.csv", engine="pyarrow")
df = get_dates_from_filename(df)


df_clean = clean_data(df.copy())
df_clean.to_csv(r"src/data/first.csv", index=False)
