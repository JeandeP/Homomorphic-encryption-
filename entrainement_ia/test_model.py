#text = ["Once you know all the elements, it's not difficult to pull together a sentence."]
#text = ["När du väl känner till alla element är det inte svårt att ta ihop en mening."] #swedish
text = ["Als je eenmaal alle elementen kent, is het niet moeilijk om een zin samen te stellen."] # Dutch
#text =["Une fois que vous connaissez tous les éléments, il n'est pas difficile de rassembler une phrase."] #French


from tensorflow import keras
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np
import nltk
import tensorflow as tf
import keras
import seaborn as sns
from nltk.corpus import stopwords
import json
import pickle
max_words = 50000
max_len = 100

le = preprocessing.LabelEncoder()
model = keras.models.load_model('model.h5')


with open('tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(data)

with open('labelEncodeur', 'rb') as f1:
    le=pickle.load(f1)

## test
text = ["En clair, si pour une raison quelconque, dans un script Python, vous avez besoin de sauvegarder, temporairement ou même de façon plus pérenne, le contenu d'un objet Python comme une liste,"] # Dutch
test_text = tokenizer.texts_to_sequences(text)
print(test_text)
test_text = tf.keras.preprocessing.sequence.pad_sequences(test_text, maxlen=max_len)
print(test_text)
predictions = model.predict(test_text)
out = predictions.argmax()
print(le.inverse_transform([out]))
print(predictions)