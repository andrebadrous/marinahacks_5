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

    df_train = []
    df_test = []
    for index in csv_files:
        df = pd.read_csv(index, index_col=[0])
        split_point = int(len(df) * 0.8)
        df_train.append(df.iloc[:split_point])
        df_test.append(df.iloc[split_point:])

    df_test = pd.DataFrame(pd.concat(df_test))
    df_train = pd.DataFrame(pd.concat(df_train))
    df_train.to_csv('../data/combined_training_data.csv', index=False)
    df_test.to_csv('../data/combined_test_data.csv', index=False)


if __name__ == "__main__":
    combine_csv()