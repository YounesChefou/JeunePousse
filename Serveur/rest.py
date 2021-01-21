# curl -X GET http://localhost:8888/Logement
# curl -X POST http://localhost:8888/Logement/\?Nom\=Cionaire\&Prenom\=Dick\&idAd\=2

import http.server, urllib.parse, sqlite3, requests, threading,  socketserver

class MyHandler(http.server.BaseHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		self.mysql = MySQL('../BDD/jeunepousse.db')
		self.user = 'user' #Mis à jour quand l'utilisateur s'identifie, pour afficher seulement ses plantes
		super(MyHandler, self).__init__(*args, **kwargs)

	def do_GET(self):
		"""Respond to a GET request."""
		res = urllib.parse.urlparse(self.path)
		if self.path.lower() == "/favicon.ico" : #Icone dans la barre d'accueil
			return
		elif self.path.lower() == "/accueil": #Page d'accueil, accueil comme
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()

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

		elif self.path.lower() == "/mesplantes"

		#TODO : Remplacer par une requete recuperant les noms de tables
		tables = ['/utilisateurs', '/logement', '/pieces', '/references', '/plantes_utilisateur']
		elif self.path.lower() in tables: #Selection de table dans la BDD
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			rep = self.mysql.select(res.path)
			self.wfile.write(bytes(str(rep)+'\n', 'UTF-8'))

	else:
		self.send_response(404)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_POST(self):
		"""Respond to a POST request."""
		print(self.path)
		res = urllib.parse.urlparse(self.path)
		print(res)

		if res.query != '':
			query = urllib.parse.parse_qs(res.query)
		else:
			q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
			print(q)
			query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
		print(query)
		rep = self.mysql.insert(res.path,query)
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def pieChart(self, rep):
		codeHTML = """
		<html>
		  <head>
			<!--Load the AJAX API-->
			<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
			<script type="text/javascript">

			  // Load the Visualization API and the corechart package.
			  google.charts.load('current', {'packages':['corechart']});

			  // Set a callback to run when the Google Visualization API is loaded.
			  google.charts.setOnLoadCallback(drawChart);

			  // Callback that creates and populates a data table,
			  // instantiates the pie chart, passes in the data and
			  // draws it.
			  function drawChart() {

				// Create the data table.
				var data = new google.visualization.DataTable();
				data.addColumn('string', 'Type de facture');
				data.addColumn('number', 'Montant à payer');
				data.addRows([
		"""
		data = {'Electricite': 0, 'Internet': 0, 'Eau':0}
		for rangee in rep:
			print(rangee)
			data[rangee[0]] += rangee[3]

		stringData = "['Electricite',"+str(data['Electricite'])+"],"
		stringData += "['Internet', "+str(data['Internet'])+"],"
		stringData += "['Eau', "+str(data['Eau'])+"],"

		finHTML = """]);
				// Set chart options
				var options = {'title':'Montant à payer par type de facture',
							   'width':400,
							   'height':300};

				// Instantiate and draw our chart, passing in some options.
				var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
				chart.draw(data, options);
			  }
			</script>
		  </head>

		  <body>
			<!--Div that will hold the pie chart-->
			<div id="chart_div"></div>
		  </body>
		</html>
		"""
		codeHTML += stringData + finHTML
		return codeHTML

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

	def pageConso(self, annee):
		codeHTML = """
			<!--Load the AJAX API-->
			<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
			<script type="text/javascript">

			  // Load the Visualization API and the corechart package.
			  google.charts.load('current', {'packages':['corechart']});

			  // Set a callback to run when the Google Visualization API is loaded.
			  google.charts.setOnLoadCallback(drawChart);

			  // On fait quatre
			  function drawChart() {

				// Create the data table.
				var dataElec = new google.visualization.DataTable();
				dataElec.addColumn('string', 'Date');
				dataElec.addColumn('number', 'Consommation electrique (kWh)');

				var dataGaz = new google.visualization.DataTable();
				dataGaz.addColumn('string', 'Date');
				dataGaz.addColumn('number', 'Consommation Gaz (kWh)');

				var dataEau = new google.visualization.DataTable();
				dataEau.addColumn('string', 'Date');
				dataEau.addColumn('number', 'Consommation Eau (m3)');

		"""

		#On ajoute les rangées pour chaque graphique

		req = "select * from facture where datePaiement >= \"%d-01-01\" AND datePaiement < \"%d-01-01\" AND typeFacture = \"Electricite\" " %(annee, annee+1)
		tabElem = self.mysql.c.execute(req).fetchall()

		stringData = "dataElec.addRows(["

		for rangee in tabElem:
			#print(rangee)
			stringData += "[\'"+str(rangee[2])+"\', "+str(rangee[4])+"],\n"

		stringData += "]);\n"

		req = "select * from facture where datePaiement >= \"%d-01-01\" AND datePaiement < \"%d-01-01\" AND typeFacture = \"Gaz\" " %(annee, annee+1)
		tabElem = self.mysql.c.execute(req).fetchall()

		stringData += "dataGaz.addRows(["

		for rangee in tabElem:
			#print(rangee)
			stringData += "['"+str(rangee[2])+"\', "+str(rangee[4])+"],\n"

		stringData += "]);\n"

		req = "select * from facture where datePaiement >= \"%d-01-01\" AND datePaiement < \"%d-01-01\" AND typeFacture = \"Eau\" " %(annee, annee+1)
		tabElem = self.mysql.c.execute(req).fetchall()

		stringData += "dataEau.addRows(["

		for rangee in tabElem:
			#print(rangee)
			stringData += "['"+str(rangee[2])+"\', "+str(rangee[4])+"],\n"

		stringData += "]);\n"

		finHTML = """
				// Set chart options
				var optionsElec = {
							   title :'Consommation electricite en """+str(annee)+"""',
          					   legend: { position: 'bottom' },
							   is3D : true
							   };

				// Instantiate and draw our chart, passing in some options.
				var chartElec = new google.visualization.LineChart(document.getElementById('curve_chart_elec'));
				chartElec.draw(dataElec, optionsElec);

				var optionsGaz = {
							   title :'Consommation Gaz en """+str(annee)+"""',
          					   legend: { position: 'bottom' },
							   is3D : true
							   };

				// Instantiate and draw our chart, passing in some options.
				var chartGaz = new google.visualization.LineChart(document.getElementById('curve_chart_gaz'));
				chartGaz.draw(dataGaz, optionsGaz);

				var optionsEau = {
								title:'Consommation Eau en """+str(annee)+"""',
				 				legend: { position: 'bottom' },
								is3D : true
								};

				// Instantiate and draw our chart, passing in some options.
				var chartEau = new google.visualization.LineChart(document.getElementById('curve_chart_eau'));
				chartEau.draw(dataEau, optionsEau);
			  }

			  $(window).resize(function(){
			  	drawChart();
			  });
			</script>
		  </head>
		"""
		codeHTML += stringData + finHTML
		return codeHTML

	def pageCapteurs(self):

		req = "select * from capteur;"
		tabElem = self.mysql.c.execute(req).fetchall()

		codeHTML = """
		<div class="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
		   <h1 class="display-4">Statut des capteurs</h1>
		</div>
		"""

		codeHTML += '<div class="container">\n'
		codeHTML += '<div class="card-deck mb-3 text-center">\n'

		for rangee in tabElem:
			nom = rangee[2]
			statut = rangee[4]

			codeHTML +='<div class="card mb-4 box-shadow" style="min-width: 200px;">\n'
			codeHTML += '<div class="card-header">\n'
			codeHTML += '<h5 class="my-0 font-weight-normal text-nowrap">'+nom+'</h5>\n'
			codeHTML += '</div>\n'
			codeHTML += '<div class="card-body">\n'
			codeHTML += '<h4 class="card-title pricing-card-title titreStatut">'
			if(statut == 1):
				codeHTML += "Actif </h4>\n"
			else:
				codeHTML += "Inactif </h4>\n"

            # <button type="button" class="btn btn-lg btn-block btn-primary">Get started</button>
			codeHTML += '</div>\n'
			codeHTML += '</div>\n'

		codeHTML += '</div>\n'
		codeHTML += '</div>\n'
		return codeHTML;

	def pageEconomie(self):

		req = 'select sum(montant) from facture where datePaiement >= "2020-01-01" and typeFacture="Electricite";'
		consoElec2020 = self.mysql.c.execute(req).fetchall()[0][0]
		req = 'select sum(montant) from facture where datePaiement < "2020-01-01" and typeFacture="Electricite";'
		consoElec2019 = self.mysql.c.execute(req).fetchall()[0][0]

		req = 'select sum(montant) from facture where datePaiement >= "2020-01-01" and typeFacture="Gaz";'
		consoGaz2020 = self.mysql.c.execute(req).fetchall()[0][0]
		req = 'select sum(montant) from facture where datePaiement < "2020-01-01" and typeFacture="Gaz";'
		consoGaz2019 = self.mysql.c.execute(req).fetchall()[0][0]

		req = 'select sum(montant) from facture where datePaiement >= "2020-01-01" and typeFacture="Eau";'
		consoEau2020 = self.mysql.c.execute(req).fetchall()[0][0]
		req = 'select sum(montant) from facture where datePaiement < "2020-01-01" and typeFacture="Eau";'
		consoEau2019 = self.mysql.c.execute(req).fetchall()[0][0]

		progElec = 100 - (consoElec2020/consoElec2019 * 100);
		progGaz = 100 - (consoGaz2020/consoGaz2019 * 100);
		progEau = 100 - (consoEau2020/consoEau2019 * 100);

		codeHTML = """
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
	    <script type="text/javascript">
	      google.charts.load('current', {'packages':['bar']});
	      google.charts.setOnLoadCallback(drawChart);

	      function drawChart() {
	        var data = google.visualization.arrayToDataTable([
	          ['Type de facture', '2019', '2020'],
		"""
		codeHTML += "['Electricite',"+str(consoElec2019)+","+str(consoElec2020)+"],"
		codeHTML += "['Gaz',"+str(consoGaz2019)+","+str(consoGaz2020)+"],"
		codeHTML += "['Eau',"+str(consoEau2019)+","+str(consoEau2020)+"],"
		codeHTML += """
	        ]);

	        var options = {
	          chart: {
	            title: 'Economies réalisées',
	            subtitle: 'Comparaison factures payées : 2019-2020',
	          }
	        };

	        var chart = new google.charts.Bar(document.getElementById('column_chart'));

	        chart.draw(data, google.charts.Bar.convertOptions(options));
	      }

		  $(window).resize(function(){
		  	drawChart();
		  });

		  $(window). load(function commentaire(){
		  	$("#commentaire").append('<li>Economies éléctricité : """+"{:.2f}".format(progElec)+"""%</li>');
			$("#commentaire").append('<li>Economies gaz : """+"{:.2f}".format(progGaz)+"""%</li>');
			$("#commentaire").append('<li>Economies eau : """+"{:.2f}".format(progEau)+"""%</li>');
		  });
	    </script>
		</head>
		"""

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

#Recupere les ports de communication des capteurs et demarre les threads associés
def start_capteur_threads():
	base = MySQL('logement.db')
	rep = base.select('/capteur') #On recupere la table Capteur
	for rangee in rep:
		port = rangee[3];
		print(rangee[2]," : ",str(port))
		threading.Thread(target=serve_on_port, args=[port]).start()


if __name__ == '__main__':
	start_capteur_threads()
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
