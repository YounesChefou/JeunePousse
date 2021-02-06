# curl -X GET http://localhost:8888/Logement
# curl -X POST http://localhost:8888/Logement/\?Nom\=Cionaire\&Prenom\=Dick\&idAd\=2

import http.server, urllib.parse, sqlite3, requests, threading,  socketserver
import json

class MyHandler(http.server.BaseHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		print("Initialisation")
		self.mysql = MySQL('../BDD/jeunepousse.db')
		self.user = 'user' #Mis à jour quand l'utilisateur s'identifie, pour afficher seulement ses plantes
		self.id_user = 0 #Id de l'utilisateur
		super(MyHandler, self).__init__(*args, **kwargs)



	def do_GET(self):
		"""Respond to a GET request."""
		res = urllib.parse.urlparse(self.path)
		#TODO : Remplacer par les noms de tables
		tables = ['/utilisateurs', '/logement', '/pieces', '/references', '/plantes_utilisateur']

		print("Path : {}".format(self.path.lower()))
		print("ID : {}".format(self.id_user))
		if self.path.lower() == "/favicon.ico" : #Icone dans la barre d'accueil
			return
		elif self.path.lower() == "/" and self.id_user == 0: #Page d'identification
			print("Identification")
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			f = open("identification.html")
			codeHTML = f.read()
			self.wfile.write(bytes(str(codeHTML), 'UTF-8'))

		# elif self.id_user == 0: #Redirection vers la page d'identification si utilisateur non identifié
		# 	self.send_response(301)
		# 	self.send_header('Location','/')
		# 	self.end_headers()

		elif self.path.lower() == "/accueil": #Page d'accueil, accueil comme
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				print("Accueil")
				codeHTML = """
				<!DOCTYPE html>
				<html lang="fr">
				    <head>

				        <title>Page d'accueil</title>
						<meta charset="utf-8">
				        <meta name="viewport" content="width=device-width, initial-scale=1">
				        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
				        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
				        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
				        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
						<style>
						#div_img{
						 	position:fixed;
			 				padding:0;
							margin:0;
							top:0;
							left:0;
							width:100%;
							height:100%;
							background-image: url('https://elemental.green/wp-content/uploads/2017/06/Depositphotos_10522904_m-2015-999x640.jpg');
							background-size: cover;
							z-index: -1;
							opacity:0.4;
						}
						</style>
					</head>
				"""
				f = open("barre_navigation.html")
				codeHTML += f.read()
				f = open("accueil.html")
				codeHTML += f.read()
				self.wfile.write(bytes(str(codeHTML), 'UTF-8'))

		elif self.path.lower() == "/mesplantes":
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()

			codeHTML = """
			<!DOCTYPE html>
			<html lang="fr">
			    <head>

			        <title>Mes plantes</title>
					<meta charset="utf-8">
			        <meta name="viewport" content="width=device-width, initial-scale=1">
			        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
			        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
			        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
			        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
					<style>
					#div_img{
						position:fixed;
						padding:0;
						margin:0;
						top:0;
						left:0;
						width:100%;
						height:100%;
						background-image: url('https://elemental.green/wp-content/uploads/2017/06/Depositphotos_10522904_m-2015-999x640.jpg');
						background-size: cover;
						z-index: -1;
						opacity:0.4;
					}
					</style>
			"""

			f = open("barre_navigation.html")
			codeHTML += f.read()
			# codeHTML += self.mesplantes() #TODO: A voir si des parametres sont necessaires, normalement non
			f = open("mesplantes.html")
			codeHTML += f.read()
			self.wfile.write(bytes(str(codeHTML), 'UTF-8'))

		elif self.path.lower() == "/guide_plante":
			pass

		elif self.path.lower() == "/configuration":
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()

			codeHTML = """
			<!DOCTYPE html>
			<html lang="fr">
				<head>

					<title>Configuration</title>
					<meta charset="utf-8">
					<meta name="viewport" content="width=device-width, initial-scale=1">
					<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
					<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
					<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
					<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
					<style>
					#div_img{
						position:fixed;
						padding:0;
						margin:0;
						top:0;
						left:0;
						width:100%;
						height:100%;
						background-image: url('https://elemental.green/wp-content/uploads/2017/06/Depositphotos_10522904_m-2015-999x640.jpg');
						background-size: cover;
						z-index: -1;
						opacity:0.4;
					}
					</style>
				</head>
			"""
			f = open("barre_navigation.html")
			codeHTML = f.read()
			# codeHTML += self.pageConfiguration()
			f = open("configuration.html")
			codeHTML += f.read()
			self.wfile.write(bytes(str(codeHTML), 'UTF-8'))


		elif self.path.lower() in tables: #Selection de table dans la BDD
			#Ici, renvoyer un fichier de type JSON à l'utilisateur
			#Exemple :
			# 0 : {
			#	'nom':'plante'
			#	'espece': 'cactus'
			#}
			# 1 : {
			#	'nom':'fleur'
			#	'espece': 'rose'
			#}
			elem = path.split('/')
			if len(elem) > 1:
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				rep = self.mysql.toJSON(elem[1])
				self.wfile.write(bytes(str(rep)+'\n', 'UTF-8'))
			else:
				self.send_response(404)
				self.send_header("Content-type", "text/html")
				self.end_headers()

		else:
			self.send_response(404)
			self.send_header("Content-type", "text/html")
			self.end_headers()

	def do_POST(self):
		"""Respond to a POST request."""
		print(self.path)
		res = urllib.parse.urlparse(self.path)

		#Verification des données
		if res.query != '':
			query = urllib.parse.parse_qs(res.query)

		elif self.path.lower() == "/accueil":
			print(res)
			q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
			query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
			print('query :')
			print(q)
			print(query)
			print(query['email'])
			email = query['email'][0]
			print(query['password'])
			req = "SELECT id FROM user where Email=\""+str(query['email'][0])+"\" and Password=\""+str(query['password'][0])+"\";";
			print(req)
			id_user = self.mysql.c.execute(req).fetchall()
			print(id_user)

			if id_user == list(): #Mauvais identifiant ou mot de passe, renvoyer vers page identification
				self.send_response(301)
				self.send_header('Location','/')
				self.end_headers()
			else:
				id_user = id_user[0][0]
				self.id_user = id_user
				print("id_user :")
				print(self.id_user)
				# self.path = "/accueil"
				# self.do_GET()
				self.send_response(301)
				self.send_header('Location','/accueil')
				self.end_headers()
		elif self.path.lower() == "/ajoutPiece":
			print(res)
			q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
			query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
			nomPiece = query['nomPiece'][0]
			refLogement = 1 #TODO : getLogement
			req = 'INSERT INTO ROOM(Name, HomeReference) VALUES(\" '+nomPiece+'\",'+str(refLogement)+');'
			print(req)
			self.mysql.c.execute(req)
			#Ajout réussi, on renvoie l'utilisateur sur cette page avec les données mises à jour
			self.send_response(301)
			self.send_header('Location', '/configuration')
			self.end_headers()

		elif self.path.lower() == "/ajoutPlante":
			print(res)
			q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
			query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
			plantRef = query['plantRef'][0]
			roomRef = query['roomRef'][0]
			kitRef = query['kitRef'][0]

			refLogement = 1 #TODO : getLogement
			req = "INSERT INTO PLANT(PlantReference, RoomReference, KitReference) VALUES("++ ")"
			print(req)
			self.mysql.c.execute(req)
			#Ajout réussi, on renvoie l'utilisateur sur cette page avec les données mises à jour
			self.send_response(301)
			self.send_header('Location', '/configuration')
			self.end_headers()

		else:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
			print(q)
			query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
			print(query)
			rep = self.mysql.insert(res.path,query)

	def meteo(self):
		#Lien vers JSON, renvoyant prévision
		apiOpenWeather = "https://api.openweathermap.org/data/2.5/forecast?q=Paris,fr&appid=3580473b9e19cbcdc40adf28d04c2fec"
		resp = requests.get(apiOpenWeather)

		if resp.status_code != 200:
		    raise ApiError('GET /meteo/ {}'.format(resp.status_code))

		listeForecast = resp.json()['list']
		jour = 0;
		jours =  ['Aujourd\'hui', 'Demain', 'Après-demain', 'Jour 4', 'Jour 5']

		strForecast = ''
		for prediction in listeForecast[0:len(listeForecast):8]:
			strForecast += '\n'+jours[jour]+':'
			strForecast += '\n{}'.format(prediction['dt_txt'])
			tempKelvin = prediction['main']['temp']
			tempCelsius = tempKelvin - 273.15
			strForecast += '\nTemperature : {0:.2f}'.format(tempCelsius)
			tempKelvin = prediction['main']['feels_like']
			tempCelsius = tempKelvin - 273.15
			strForecast += '\nRessenti : {0:.2f}'.format(tempCelsius)
			strForecast += '\nHumidite : {}'.format(prediction['main']['humidity'])
			strForecast += '\nTemps prévu : {}\n'.format(prediction['weather'][0]['main'])
			jour += 1

		return strForecast

	#Recupere les informations
	def mesplantes(self):
		# req = "select * from capteur;"
		# tabElem = self.mysql.c.execute(req).fetchall()
		conn = self.mysql.conn
		c = conn.cursor()

		codeHTML ="""
		"""
		#On recupere l'id max pour les chambres existantes
		req = "SELECT MAX(id) FROM room;"
		nbChambres = c.execute(req).fetchall()[0][0]

		print("Nombre de chambres :")
		print(nbChambres)

		#On boucle maintenant pour recuperer chaque plante et les informations associés
		# for id_room in range (1, nbChambres+1):
		#
		# 	req = "SELECT * FROM PLANTE WHERE RoomReference="+str(id_room)+";"
		# 	donnees = self.toJSON('PLANTE', req).json()
		#
		# 	#Liste pour chaque plante
		# 	codeHTML += "<ul>"
		# 	for plante in donnees:
		# 		pass
		#
		# 	codeHTML += "</ul>"
		codeHTML +=
		codeHTML += "<ul>"
		codeHTML += "</ul>"
		# f = open("dash.html")
		# codeHTML = f.read()
		return codeHTML



	#Affiche les informations sur le logement et permet d'ajouter des capteurs
	def pageConfiguration(self):
		req = "select * from logement;"
		infosLogement = self.mysql.c.execute(req).fetchall()

		req = "select * from piece;"
		infosPiece = self.mysql.c.execute(req).fetchall()

		req = "select * from TYPE_CAPTEUR;"
		infosTypeCapteur = self.mysql.c.execute(req).fetchall()

		codeHTML = """
		<div class="mx-3">
		<h3>Logement principal</h3>
		<br>
		<dl class="row">
  			<dt class="col-sm-3">Adresse</dt>
  			<dd class="col-sm-9">"""+infosLogement[0][1]+"""</dd>

			<dt class="col-sm-3">Numéro de téléphone</dt>
  			<dd class="col-sm-9">"""+infosLogement[0][2]+"""</dd>

			<dt class="col-sm-3">Date de création du compte</dt>
  			<dd class="col-sm-9">"""+infosLogement[0][3]+"""</dd>
		</dl>

		<br>
		<h3>Ajouter un capteur</h3>
		<br>
		<form action="/capteur" method="post" target="_blank">

			<!-- Selection de la piece -->
			<label for="selectPiece">Selection piece</label>
		  	<select class="custom-select form-control" id="selectPiece" name="idPiece">
			"""

		for rangee in infosPiece:
			codeHTML += "<option value=\""+str(rangee[1])+"\" >"+rangee[2]+"</option>\n"

		codeHTML += """
			</select>
			<br>
			<br>
			<!-- Selection du type de capteur -->
			<label for="selectCapteur">Selection type de capteur</label>
			<select class="custom-select form-control" id="selectCapteur" name="typeCapteur">
			"""
		for rangee in infosTypeCapteur:
			codeHTML += "<option value=\""+rangee[0]+"\" >"+rangee[0]+"</option>\n"

		codeHTML +=	"""
			</select>
			<br>
			<br>
			<!-- Selection du port -->
			<label for="selectPort">Selection port</label>
		  	<select class="custom-select form-control" id="selectPort" name="portCommunication">
			"""
		for rangee in infosTypeCapteur:
			codeHTML += "<option value=\""+str(rangee[2])+"\" >"+str(rangee[2])+"</option>\n"

		codeHTML += """
			</select>
			<br>
			<br>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="statut" id="radioActif" value="1">
				<label class="form-check-label" for="radioActif">Actif</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="statut" id="radioInactif" value="0">
				<label class="form-check-label" for="radioInactif">Inactif</label>
			</div>
			<br>
			<br>
		  <button type="submit" class="btn btn-light">Submit</button>
		</form>
		<br>
		</div>
		"""
		return codeHTML;

	def toJSON(self, table, req=None):
		reqColumn = "PRAGMA table_info("+table+");"

		conn = self.mysql.conn
		c = conn.cursor()
		columns = c.execute(reqColumn).fetchall()
		donnees = c.execute(req).fetchall()

		if req is None:
			req = "SELECT * FROM "+table+";"

		fichierJSON = """
		[
		"""
		cpt = 0;
		for rangee in donnees:
		    print(rangee)
		    fichierJSON += '\t\"'+str(cpt)+'\": {\n'
		    for i in range (0, len(columns)):
		        fichierJSON += '\t\"'+str(columns[i][1])+'\":\"'+str(rangee[i])+'\",'
		        fichierJSON += '\n'
		    fichierJSON += '\t}'
		    fichierJSON += '\n\n'
		    cpt += 1

		fichierJSON += """
		]
		"""

		return fichierJSON


class MySQL():
	def __init__(self, name):
		self.c = None
		self.req = None
		self.conn = sqlite3.connect(name)
		self.c = self.conn.cursor()

	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.close()

	def select(self,path):
		elem = path.split('/')
		if len(elem) == 2:
			req = "select * from %s" %(elem[1])
		else:
			req = "select %s from %s where id=%s" %(elem[3],elem[1],elem[2])
		return self.c.execute(req).fetchall()

	def insert(self,path,query):
		print(query)
		attr = ', '.join(query.keys())
		val = ', '.join('"%s"' %v[0] for v in query.values())
		print(attr,val)
		req = "insert into %s (%s) values (%s)" %(path.split('/')[1], attr, val)
		print(req)
		self.c.execute(req)
		self.conn.commit()

class ThreadingHTTPServer (socketserver . ThreadingMixIn ,http . server . HTTPServer):
	pass

def serve_on_port(port) :
	server = ThreadingHTTPServer (("localhost", port) , MyHandler)
	server.serve_forever()

#TODO : modifier cette fonction une fois les capteurs ajoutés
#Recupere les ports de communication des capteurs et demarre les threads associés
def start_capteur_threads():
	base = MySQL('logement.db')
	rep = base.select('/capteur') #On recupere la table Capteur
	for rangee in rep:
		port = rangee[3];
		print(rangee[2]," : ",str(port))
		threading.Thread(target=serve_on_port, args=[port]).start()


if __name__ == '__main__':
	# start_capteur_threads()
	#On ouvre un 4e thread pour toutes les autres requêtes
	threading.Thread(target=serve_on_port, args=[8888]).start()
	print("Divers : 8888");
	# threading.Thread(target=serve_on_port, args=[7777]).start()
	# threading.Thread(target=serve_on_port, args=[8888]).start()
	# threading.Thread(target=serve_on_port, args=[9999]).start()

	# server_class = http.server.HTTPServer
	# httpd = server_class(("localhost", 8888), MyHandler)
	# try:
	# 	httpd.serve_forever()
	# except KeyboardInterrupt:
	# 	pass
	# httpd.server_close()
