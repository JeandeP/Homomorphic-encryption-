import json
import gmpy2
import phe as paillier
import time

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
Fonction permettant la conversion de la chaine de caractère vers un entier
'''
def conversion(message) :
	message = message.lower()
	data = '' 
	liste = list(message)
	for y in range(len(message)) :
		a = ord(liste[y])
		data = data + str(a)
	return data

'''
Fonction permettant de convertir les données du message d'un entier vers une chaine de caractère
'''
def dechiffrement(reponse) :
	x = 0
	donnee = ''
	liste = [str(reponse)]
	while (x < len(str(reponse))) :
		b = liste[0][x]
		c = liste[0][x+1]
		d = b+c
		if (int(d) < 30) :
			f = liste[0][x+2]
			d = d + f
			donnee = donnee + chr(int(d))
			x = x + 3     # Permet de décaler l'indice x de 3 caractères
		else :
			donnee = donnee + chr(int(d))
			x = x + 2	  # Permet de décaler l'indice x de 2 caractères
	return donnee

'''
Fonction permettant de charger les informations du fichier message servant à l'envoie du message vers le serveur
'''
def loadAnswer():
	with open('message.json', "r") as file:
		data = json.load(file)
	return data

'''
Fontion principale permettant l'envoie et la réception de donnée tant que l'utilisateur le souhaite
'''
def main():
	a = 1
	storeKeys()
	pub_key, priv_key = getkeys()
	print("Vos clés de sécurité pour cette session sont : \n", pub_key, "\n", priv_key)
	while a < 2 :
		tap = input("Souhaitez vous envoyer un message ? Tapez x pour continuez ou tapez n'importe quel autre touche pour quittez \n")
		if (tap == 'x'):
			message = input("Votre message : ")
			data = conversion(message)
			envoie = [int(data)]
			print(envoie)
			serializeData(pub_key, envoie)
			print("Envoie du message ...   ...")

			time.sleep(10)

			answer_file = loadAnswer()
			answer_key = paillier.PaillierPublicKey(n=int(answer_file['public_key']['n']))
			if (answer_key == pub_key):
				answer = paillier.EncryptedNumber(answer_key, int(str(answer_file['values'][0][0])))  # Récupère les données réenvoyé par le serveur
				reponse = priv_key.decrypt(answer)		# Déchiffrement des données avec l'utilisation de la clé privé
				print(reponse)
				fin = dechiffrement(reponse)			# Conversion des données par la fonction dechiffrement
				print('message recu :', fin)
			else :
				print("La cle public est inconnu")		# Affiche un message d'erreur si la clé publique reçu est différente de celle sauvegarder en mémoire

		else :
			a = 3
			print("Au revoir")

main()