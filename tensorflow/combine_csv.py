import pandas as pd

def combine_csv():

    csv_files = [
    "../data/confused.csv",
    "../data/freaky.csv",
    "../data/happy.csv",
    "../data/mad.csv",
    "../data/relaxed.csv",
    "../data/sad.csv",
    "../data/shocked.csv"]

    dfs = []
    for index in csv_files:
        df = pd.read_csv(index, index_col=[0])
        dfs.append(df)

    df = pd.DataFrame(pd.concat(dfs))
    df.to_csv('../data/combined_data.csv', index=False)


if __name__ == "__main__":
    combine_csv()