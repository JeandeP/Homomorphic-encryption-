# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('dataset'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

import numpy as np
import nltk
import tensorflow as tf
import keras
import seaborn as sns
from nltk.corpus import stopwords
import io
import json
df = pd.read_csv("dataset/dataset.csv")
df.head()
df.info()

df["Text"] = df["Text"].str.lower()
df.head()

#NLP Preprocessing : Tokenization and Embeddings
max_words = 50000
max_len = 100
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words = max_words)
tokenizer.fit_on_texts(list(df['Text']))
train_df = tokenizer.texts_to_sequences(list(df['Text']))

tokenizer_json = tokenizer.to_json()
with io.open('tokenizer.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_json, ensure_ascii=False))
train_df = tf.keras.preprocessing.sequence.pad_sequences(train_df,maxlen = max_len)
df.head()
len(tokenizer.word_index)
Y = df['language']
print(Y)


from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pickle
le = preprocessing.LabelEncoder()
le.fit(Y)
list(le.classes_)
with open('labelEncodeur', 'wb') as f1:
    pickle.dump(le, f1)

Y2 = le.fit_transform(Y)
total_languages = df['language'].nunique()
Y2 = keras.utils.to_categorical(Y2,num_classes=total_languages)
np.shape(Y2)
X_train,X_test,Y_train,Y_test = train_test_split(train_df,Y2)
embedding_dims = 500
vocab_size = len(tokenizer.word_index)+1

tf.test.is_gpu_available(cuda_only=True) 
# Build the neural network model
model = tf.keras.Sequential([tf.keras.layers.Embedding(input_dim = vocab_size,output_dim = embedding_dims,input_length = max_len),
                            tf.keras.layers.Flatten(),
                            tf.keras.layers.Dense(total_languages,activation=tf.nn.softmax)
                            ])
model.summary()


checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,save_weights_only=True,verbose=1)


model.compile(optimizer ='adam',loss = 'categorical_crossentropy',metrics=['accuracy'])

model.fit(np.array(X_train),np.array(Y_train),epochs=3,callbacks=[cp_callback])

model.evaluate(np.array(X_test),np.array(Y_test))

print("English ",le.transform(['English']))
print("French ",le.transform(['French']))
print("Dutch ",le.transform(['Dutch']))
print("Swedish ",le.transform(['Swedish']))

model.save('model.h5')
