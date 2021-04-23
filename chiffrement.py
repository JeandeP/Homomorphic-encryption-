import json
import gmpy2
import phe as paillier
import time
import pickle
from tensorflow import keras
from sklearn import preprocessing

'''
Fonction permettant de transformer notre chaine de caractère en vecteur selon une méthode de préprocessing
'''
def ia(text):

	with open('tokenizer.json') as f:
		data = json.load(f)
		tokenizer = keras.preprocessing.text.tokenizer_from_json(data)

	test_text = tokenizer.texts_to_sequences(text)
	data = keras.preprocessing.sequence.pad_sequences(test_text, maxlen=100)
	data.tolist()

	return data


'''
Fonction permettant de créer et de sauvegarder en mémoire les clés publiques et privés dans le json custkeys
'''
def storeKeys():
	public_key, private_key = paillier.generate_paillier_keypair()
	keys={}
	keys['public_key'] = {'n': public_key.n}
	keys['private_key'] = {'p': private_key.p, 'q': private_key.q}
	with open('custkeys.json', "w") as file:
		json.dump(keys, file)

'''
Fonction retournant les clés publiques et privés extraite du json custkeys
'''
def getkeys():
	with open('custkeys.json', "r") as file:
		keys = json.load(file)
		pub_key = paillier.PaillierPublicKey(n = int(keys['public_key']['n']))
		priv_key = paillier.PaillierPrivateKey(pub_key, keys['private_key']['p'], keys['private_key']['q'])
		return pub_key, priv_key

'''
Fonction permettant le chiffrement de nos données selon la méthode de Paillier
'''
def serializeData(public_key, data):
	encrypted_data_list = [public_key.encrypt(x, precision = None) for x in data]
	encrypted_data = {}
	encrypted_data['public_key'] = {'n':public_key.n}
	encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
	with open('message.json', "w") as file:
		json.dump(encrypted_data, file)			# On sauvegarde nos données chiffré dans le json message
	return serializeData

'''
Fonction permettant de stocker les informations du fichier message servant à l'envoie du message vers le serveur
'''
def loadAnswer():
	with open('answer.json', "r") as file:
		data = json.load(file)
	return data

'''
Fonction permettant de charger les informations du message envoyé par le client
'''
def getkeys2():
	with open('message.json', "r") as file:
		keys = json.load(file)
		value = {}
		pub_key = paillier.PaillierPublicKey(n = int(keys['public_key']['n']))
		value = [[int(x[0], int(x[1])) for x in keys['values']]]
		return pub_key, value
'''
Fonction permettant de prédire le langage des données analysées
'''
def predict(data):
	data = keras.preprocessing.sequence.pad_sequences(data, maxlen=1000)
	model = keras.models.load_model('model.h5')
	print(data)
	predictions = model.predict(data)
	out = predictions.argmax()
	return out

'''
Fonction permettant de stocker la réponse de l'IA afin de l'envoyer au client
'''
def sendData(data):
    encrypted_data_list = [public_key.encrypt(x, precision = 1) for x in data]
    encrypted_data = {}
    encrypted_data['public_key'] = {'n':public_key.n}
    encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
    with open('answer.json', "w") as file:
        json.dump(encrypted_data, file)
    return serializeData


storeKeys()
pub_key, priv_key = getkeys()
message = ["Le vent et le soleil se regarde et pendant un court instant, rien ne se passe"]
print(message)
ecrit = ia(message)
envoie = ecrit[0].tolist()
print(envoie)
serializeData(pub_key, envoie)

public_key, data = getkeys2()
print(data)
for x in range(len(data)) :
	out = predict((data[0][x]))
sendData(out)

answer_file = loadAnswer()
answer_key = paillier.PaillierPublicKey(n=int(answer_file['public_key']['n']))
if (answer_key == pub_key):
	for u in range(len(envoie)) :
		answer = paillier.EncryptedNumber(answer_key, int(str(answer_file['values'][u][0])))  # Récupère les données réenvoyé par le serveur
		reponse = priv_key.decrypt(answer)		# Déchiffrement des données avec l'utilisation de la clé privé
		print(reponse)
		#fin = dechiffrement(reponse)			# Conversion des données par la fonction dechiffrement
		#print('message recu :', fin)
else :
	print("La cle public est inconnu")		# Affiche un message d'erreur si la clé publique reçu est différente de celle sauvegarder en mémoire
