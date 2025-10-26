import tensorflow as tf
import pandas as pd
import numpy as np
import keras

csv_files = [
    "../data/andre_confused.csv",
    "../data/andre_freaky.csv",
    "../data/andre_happy.csv",
    "../data/andre_mad.csv",
    "../data/andre_relaxed.csv",
    "../data/andre_sad.csv",
    "../data/andre_shocked.csv"
]

confused = pd.read_csv(csv_files[0])
sil_confused = pd.DataFrame(confused.iloc[400:])
confused = confused.iloc[:400]

freaky = pd.read_csv(csv_files[1])
sil_freaky = pd.DataFrame(freaky.iloc[135:])
freaky = freaky.iloc[:135]

happy = pd.read_csv(csv_files[2])
sli_happy = pd.DataFrame(happy.iloc[400:])
happy = happy.iloc[:400]

mad = pd.read_csv(csv_files[3])
sli_mad = pd.DataFrame(mad.iloc[450:])
mad = mad.iloc[:450]

relaxed = pd.read_csv(csv_files[4])
sli_relaxed = pd.DataFrame(relaxed.iloc[630:])
relaxed = relaxed.iloc[:630]

sad = pd.read_csv(csv_files[5])
sli_sad = pd.DataFrame(sad.iloc[430:])
sad = sad.iloc[:430]

shocked = pd.read_csv(csv_files[6])
sli_shocked = pd.DataFrame(shocked.iloc[450:])
shocked = shocked.iloc[:450]


df_train = pd.concat([confused, freaky, happy, mad, relaxed, sad, shocked])
df_test = pd.concat([sil_confused, sil_freaky, sli_happy, sli_mad, sli_relaxed, sli_sad, sli_shocked])

print(df_train.shape)

images_train = pd.DataFrame(df_train.iloc[:, 1:2])
images_train.to_numpy()
print(images_train.shape)
print(df_train)

