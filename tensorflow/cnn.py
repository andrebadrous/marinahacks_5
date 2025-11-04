# import tensorflow as tf
import pandas as pd
import numpy as np
# import keras
import csv


"""
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

images_train = pd.DataFrame(df_train.iloc[:, 1:2])
coord_train = pd.DataFrame(df_train.iloc[:, 5:])
y_train = pd.DataFrame(df_train.iloc[:, 4:5])
print(images_train.dtypes())
images_train.to_numpy()
y_train.to_numpy()
coord_train.to_numpy()

images_test = pd.DataFrame(df_test.iloc[:, 1:2])
coord_test = pd.DataFrame(df_test.iloc[:, 5:])
y_test = pd.DataFrame(df_test.iloc[:, 4:5])

# model 
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(6)
])

print(model.summary())

# loss 
loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optim = keras.optimizers.Adam(learning_rate=0.001)
metrics = ["accuracy"]


model.compile(loss=loss, optimizer=optim, metrics=metrics)

#training 
batch_size = 64
epochs = 5
model.fit(images_train, y_train, batch_size=batch_size, epochs=epochs, shuffle=True, verbose=2)

# evaluate model
model.evaluate(images_test, y_test, batch_size=batch_size, verbose=2)

# predictions
probability_model = keras.models.Sequential([
    model,
    keras.layers.Softmax()
])

predictions = probability_model(images_test)
pred0 = predictions[0]
print(pred0)
label0 = np.argmax(pred0)
print(label0)

# model + softmax
predictions = model(images_test)
predictions = tf.nn.softmax(predictions)
pred0 = predictions[0]
print(pred0)
label0 = np.argmax(pred0)
print(label0)

pred05s = predictions[0:5]
print(pred05s.shape)
label05s = np.argmax(pred05s, axis=1)
print(label05s)"""