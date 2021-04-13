import json
import gmpy2
import phe as paillier


def storeKeys():
	public_key, private_key = paillier.generate_paillier_keypair()
	keys={}
	keys['public_key'] = {'n': public_key.n}
	keys['private_key'] = {'p': private_key.p, 'q': private_key.q}
	with open('custkeys.json', "w") as file:
		json.dump(keys, file)

def getkeys():
	with open('custkeys.json', "r") as file:
		keys = json.load(file)
		pub_key = paillier.PaillierPublicKey(n = int(keys['public_key']['n']))
		priv_key = paillier.PaillierPrivateKey(pub_key, keys['private_key']['p'], keys['private_key']['q'])
		return pub_key, priv_key

def serializeData(public_key, data):
	encrypted_data_list = [public_key.encrypt(x, precision = None) for x in data]
	encrypted_data = {}
	encrypted_data['public_key'] = {'n':public_key.n}
	encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
	with open('message.json', "w") as file:
		json.dump(encrypted_data, file)
	return serializeData

def conversion(message) :
	message = message.lower()
	data = '' 
	liste = list(message)
	for y in range(len(message)) :
		a = ord(liste[y])
		data = data + str(a)
	return data

def dechiffrement(reponse) :
	donnee = '' 
	liste = list(reponse)
	for y in range(len(reponse)) :
		a = ord(liste[y])
		donnee = donnee + str(a)
	return donnee


storeKeys()
pub_key, priv_key = getkeys()
message = 'coucou'
data = conversion(message)
envoie = [int(data)]
print(envoie)
datafile = serializeData(pub_key, envoie)
print(datafile)

'''
def loadAnswer():
    with open('answer.json', "r") as file:
	encrypted_data = json.load(file)
	reponse = json.load(encrypted_data)
    return reponse


answer_file = loadAnswer()
answer_key = paillier.PaillierPublicKey(n=int(answer_file['pubkey']['n']))
answer = paillier.EncryptedNumber(answer_key, int(answer_file['values'][0]), int(answer_file['values'][1]))
if (answer_key == pub_key):
    print(priv_key.decrypt(answer))
'''
