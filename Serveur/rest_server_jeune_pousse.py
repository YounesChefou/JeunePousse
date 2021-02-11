import http.server, urllib.parse, sqlite3, requests, threading,  socketserver, datetime, cgi
from urllib.parse import urlparse
from math import *

email_root = "root@root.root"
password_root = "root@root.root"

OK = 200
KO = 404
REDIRECTION = 301

#Donnee temporaire le temps de la configuration d'un compte
#home
AddNumber_t = ""
Street_t = ""
City_t = ""
PostalCode_t = ""
Country_t = ""
NumberOfRooms_t = ""
ip_t = ""
#user
Name_t = ""
Email_t = ""
Password_t = ""
#room
room_t = []
piece_type = ["salon", "salle à manger", "chambre", "salle de bain", "cuisine", "garage"]
############################################################
html_start = '<!DOCTYPE html><html lang="fr"><head><title>Jeune Pousse</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><style type="text/css" media="screen"></head>'
html_body = '<body>'
html_end = '</body>\n</html>'
no_data = 1000000

temp_email = ''
temp_password = ''

icone_3_traits = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-border-width" viewBox="0 0 16 16"><path d="M0 3.5A.5.5 0 0 1 .5 3h15a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5H.5a.5.5 0 0 1-.5-.5v-2zm0 5A.5.5 0 0 1 .5 8h15a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H.5a.5.5 0 0 1-.5-.5v-1zm0 4a.5.5 0 0 1 .5-.5h15a.5.5 0 0 1 0 1H.5a.5.5 0 0 1-.5-.5z"/></svg>'

bdd_home_fields = ["id", "Location", "Ip", "Number Of Rooms", "Insertion Date", ""]
bdd_room_fields = ["", "id", "Name", "Home Reference", "Insertion Date", ""]
bdd_user_fields = ["id", "Name", "Email", "Password", "Home Reference", "Insertion Date"]
bdd_plant_fields = ["Name", "Origin", "Temperature", "Humidity", "Luminosity", "GroundQuality"]
bdd_kit_fields = ["Name", "SensoractionNames", "SensoractionUnits", "Insertion Date"]

def add_nav_bar(activ_num):
    content = '<nav class="navbar navbar-inverse"><div class="container-fluid"><div class="navbar-header"><a class="navbar-brand">Jeune Pousse</a></div><ul class="nav navbar-nav">'
    if activ_num == 1:
        content += '<li class="active"><a href="http://localhost:8888/dashboard>Dashboard</a></li>'
    else :
        content += '<li><a href="http://localhost:8888/dashboard>Dashboard</a></li>'
    if activ_num == 2:
        content += '<li class="active"><a href="http://localhost:8888/option>Configure</a></li>'
    else :
        content += '<li><a href="http://localhost:8888/option>Configure</a></li>'
    if activ_num == 3:
        content += '<li class="active"><a href="http://localhost:8888/action>Automatisation</a></li>'
    else :
        content += '<li><a href="http://localhost:8888/action>Automatisation</a></li>'
    content += '</ul>\n</div>\n</nav>'
    return content


def construct_dashboard(room_list, user_plant_list, sensor_list, measure_list, reference_plant_list):
    content = html_start #ajout DOCTYPE html lang title meta head
    content += html_body
    content += add_nav_bar(1) #ajout de la navbar

    for r in room_list:
        content += ''#A COMPLETER
        #AJOUTER DEBUT CODE HTML POUR UNE PIECE
        #nom de la piece est r[1]
        for p in user_plant_list:
            if p[2] == r[0]: #si la plant est dans la room => referencepiece = id de la piece
                for p_r in reference_plant_list:
                    if p[1] == p_r[0]: #si la plant est la meme que la reference de plante => donnees de reference
                        content += ''#A COMPLETER
                        #AJOUTER CODE HTML POUR UNE PLANTE DANS LA PIECE
                        #nom de la plante p_r[1]
                        #origine de la plante p_r[2]
                        for s in sensor_list:
                            if s[3] == p[0]: #si le sensor est lie a cette plante*
                                reference_value = 0
                                current_value = no_data
                                if s[1] == 'Temperature':
                                    reference_value = p_r[3]
                                elif s[1] == 'Humidity':
                                    reference_value = p_r[4]
                                elif s[1] == 'Luminosity':
                                    reference_value = p_r[5]
                                elif s[1] == 'GroundQuality':
                                    reference_value = p_r[6]
                                for m in measure_list:
                                    if m[2] == s[0]: #si la mesure est liee a la plante => on prend la derniere mesure
                                        current_value = m[1]
                                content += ''#A COMPLETER
                                #AJOUTER CODE HTML POUR UNE DONNEE DE LA PLANTE
                                #nom du capteur/actionneur s[1]
                                #valeur actuelle du capteur/actionneur :
                                #   - tester si current_value == no_data alors afficher NO DATA comme valeur
                                #   - sinon afficher current_value (Code Couleur VERT si reference_value +- 5% ; ORANGE si reference_value +- 15% ; ROUGE sinon)
                                #unite de cette value s[2]
                                #valeur de reference reference_value
                                #unite de cette value s[2]
    content += html_end #fin de la page html
    return content

def construct_option_page(home, room_list, user_plant_list, kitreference_list, reference_plant_list):
    content = html_start #ajout DOCTYPE html lang title meta head
    content += html_body
    content += add_nav_bar(2) #ajout de la navbar

    for h in home:
        content += ''#A COMPLETER
        #AJOUTER CODE HTML AFFICHANT LES DONNEES DE LA MAISON
        #numero addresse h[1]
        #rue h[2]
        #ville h[3]
        #code postal h[4]
        #pays h[5]
        #IP h[6]
    for r in room_list:
        content += ''#A COMPLETER
        #AJOUTER CODE HTML AFFICHANT LA LISTE DES PIECES
        #Nom r[1]
    #CODE HTML POUR PROPOSER D'AJOUTER UNE PIECE => besoin de demander au user que le nom de la piece (reference logement par defaut a 0)
    for p in user_plant_list:
        content += ''#A COMPLETER
        #AJOUTER CODE HTML AFFICHANT LA LISTE DES PLANTES DANS LE LOGEMENT
        for p_r in reference_plant_list:
            if p[1] == p_r[0]: #on recupere le nom de la plante
                content += ''
                #INFO SUR UNE PLANTE => POUR CODE html
                #nom de la plante p_r[1]
                #origine de la plante p_r[2] (optionnel)
    #CODE HTML POUR PROPOSER D'AJOUTER UNE PIECE
    #step 1 selectionner nom de la plante => faire menu deroulant ou user clique sur le nom qui lui convient
    for p_r in reference_plant_list:
        content += ''
        #nom de la plante p_r[1]
        #origine de la plante p_r[2]
    #step 2 selectionner kit achete par l'utilisateur => faire menu deroulant ou user clique sur le nom du kit achete
    for k in kitreference_list:
        content += ''
        #nom du kit k[1]
    #step 3 selectionner la piece ou est placee la plante => faire menu deroulant ou user clique sur la piece ou ajouter la plante
    for r in room_list:
        content +=''
        #nom r[1]

    content += html_end
    return content
#permet d'ajouter une piece lors de la creation d'un compte
def create_account_add_rooms():
    global room_t
    global NumberOfRooms_t
    content = ''
    destination_final = ''
    f = open('site/header_create_account.html', 'r')
    content = f.read()
    f.close()

#room_img = '\n<div class="container-fluid text-center" id="mve"">\n<div class="row content">\n<div id="icone" class="col-sm-2 sidenav">\n<img src="'
#room_body = '" alt="" class="img-responsive img-center">\n</div>\n<div id="liste" class="col-sm-8 text-left">\n<h1 id="texte_liste">     '
#room_body_inter = '</div>\n</div>\n</div>'


    content += '<div class="col-sm-12">'
    content += '<h1 class="h3 mb-3 font-weight-normal">Indiquez les pièces du logement</h1>'
    if len(room_t) != 0:
        for p in room_t:
            content += '<div class="container-fluid text-center"><div class="row content">'
            content += '<div class="col-sm-2 sidenav">'
            content += icone_3_traits
            content += '</div>'
            content += '<div class="col-sm-8 text-left">'
            content += '<h4>{}</h4>'.format(p)
            content += '</div></div></div>'

    for p in piece_type :
        content += '<div class="row text-center">\n'
        content += '<div class="col-sm-4">'
        content += '</div>'
        content += '<div id = "icone"  class="col-sm-4">'
        content += '<div class="dropdown">\n'
        content += '<button id = "icone" class="btn btn-default dropdown-toggle input-block-level" type="button" data-toggle="dropdown">'
        content += '<h4>{}</h4>'.format(p)
        content += '\n<span class="caret"></span></button>'
        content += '<iframe id="invisible" name="invisible" style="display:none;"></iframe>'
        content += '<div class="dropdown-menu center">'
        if len(room_t) == int(NumberOfRooms_t) - 1:
            content += '<form class="form-signin" action="/end_config" method="post">'
        else :
            content += '<form class="form-signin" action="/add_next_room_config" method="post">'
        content += '<div><input name="Nom" id="Nom" value="{}" readonly="readonly" class="form-control" hidden></div>'.format(p)
        content += '<div><input name="Nomf" id="Nomf" class="form-control" placeholder="Nommer cette pièce" required autofocus></div>'
        content += '<div> <button type="submit" class="btn btn-secondary ">Ajouter une pièce</button></div></form>'
        content += '</div></div></div></div>'
        content += '<div class="col-sm-4">'
        content += '</div>'
    content += '</div>'
    content += '<div class="col-sm-12">'
    content += '<progress id="prog" max="100" value="100"> 100% </progress>'
    pourcentage = 100 * (len(room_t) + 1) / int(NumberOfRooms_t)
    content += '<progress id="prog" max="100" value="{}"> {}% </progress>'.format(str(pourcentage), str(pourcentage))
    content += '</div>'
    content += '<footer class="container-fluid text-center">'
    content += '<p class="mt-5 mb-3 text-muted">&copy; 2021 JeunePousse</p>'
    content += '</footer>'
    content += '</div>'
    content += html_end
    return content
#ajoute toutes les donnees temporaires de la creation d'un compte a la base de donnees
def create_account():
    #donnees temporaires recueillies
    global AddNumber_t
    global Street_t
    global City_t
    global PostalCode_t
    global Country_t

    global Name_t
    global Email_t
    global Password_t

    global NumberOfRooms_t
    global room_t

def add_nav_bar_root(activ_num):
    content = '<nav class="navbar navbar-inverse"><div class="container-fluid"><div class="navbar-header"><a class="navbar-brand">Jeune Pousse Root</a></div><ul class="nav navbar-nav">'
    if activ_num == 1:
        content += '<li class="active"><a href="http://localhost:8888/root_home">homes</a></li>'
    else :
        content += '<li><a href="http://localhost:8888/root_home">homes</a></li>'
    if activ_num == 2:
        content += '<li class="active"><a href="http://localhost:8888/root_room">rooms</a></li>'
    else :
        content += '<li><a href="http://localhost:8888/root_room">rooms</a></li>'
    if activ_num == 3:
        content += '<li class="active"><a href="http://localhost:8888/root_user">users</a></li>'
    else :
        content += '<li><a href="http://localhost:8888/root_user">users</a></li>'
    if activ_num == 4:
        content += '<li class="active"><a href="http://localhost:8888/root_plant">plants</a></li>'
    else :
        content += '<li><a href="http://localhost:8888/root_plant">plants</a></li>'
    if activ_num == 5:
        content += '<li class="active"><a href="http://localhost:8888/root_kit">kits</a></li>'
    else :
        content += '<li><a href="http://localhost:8888/root_kit">kits</a></li>'
    content += '</ul>'
    content += '<ul class="nav navbar-nav navbar-right"><li><a href="http://localhost:8888/home"><span class="glyphicon glyphicon-user"></span> Root Log Out</a></li></ul>'
    content += '</div>\n</nav>'
    return content

def root_access(type_to_display, home_list, user_list, room_list, plant_list, kit_list):

    #content = html_start #ajout DOCTYPE html lang title meta head
    #content += html_body
    f = open('site/root_header.html', 'r')
    content = f.read()
    f.close()
    legend = []
    data = []

    if(type_to_display == '/root_home'):
        content += add_nav_bar_root(1)
        legend = bdd_home_fields
        for d in home_list:
            data.append([d[0], d[1] + " " + d[2] + ", " + d[3] + ", " + d[4] + ", " + d[5], d[6], str(d[7]), d[8], ""])
    elif type_to_display == '/root_room':
        content += add_nav_bar_root(2)
        legend = bdd_room_fields
        for d in room_list:
            data.append(["", d[0], d[1], d[2], d[3], ""])
    elif type_to_display == '/root_user':
        content += add_nav_bar_root(3)
        legend = bdd_user_fields
        for d in user_list:
            data.append([d[0], d[1], d[2], d[3], d[4], d[6]])
    elif type_to_display == '/root_plant':
        content += add_nav_bar_root(4)
        legend = bdd_plant_fields
        for d in plant_list:
            data.append([d[1], d[2], d[3], d[4], d[5], d[6]])
    elif type_to_display == '/root_kit':
        content += add_nav_bar_root(5)
        legend = bdd_kit_fields
        for d in kit_list:
            data.append([d[1], d[2], d[3], d[4]])


    if(type_to_display == '/root_kit'):
        content += '<div class="row">'
        content += '<div class="col-sm-12">'
        content += '<form class="form-signin" action="http://localhost:8888/root_add_kit" method="post">'
        content += '<h1 class="h3 mb-3 font-weight-normal">ROOT ACCESS : ajouter un kit</h1>'
        content += '<label for="Name" class="sr-only">Name</label>'
        content += '<input id="Name" name="Name" class="form-control" placeholder="Name" required autofocus>'
        content += '<h4>Rensigner la liste des capteurs et actionneurs composants le kit de la sorte : \'capteur,capteur,....\'</h4>'
        content += '<label for="SensorAction" class="sr-only">Capteurs & Actionneurs</label>'
        content += '<input id="SensorAction" name="SensorAction" class="form-control" placeholder="Capteurs & Actionneurs" required autofocus>'
        content += '<h4>Rensigner la liste des unités de chaque capteur/actionneur (attention à l\'ordre) de la sorte : \'unite,unite,....\'</h4>'
        content += '<label for="Units" class="sr-only">Units</label>'
        content += '<input id="Units" name="Units" class="form-control" placeholder="Units" required autofocus>'
        content += '<button class="btn btn-secondary btn-lg btn-block" type="submit">Ajouter le kit</button>'
        content += '</form>'
        content += '</div>'
        content += '</div>'
    if type_to_display == '/root_plant':
        content += '<div class="row">'
        content += '<div class="col-sm-12">'
        content += '<form class="form-signin" action="http://localhost:8888/root_add_plant" method="post">'
        content += '<h1 class="h3 mb-3 font-weight-normal">ROOT ACCESS : ajouter une référence de plante</h1>'
        content += '<label for="Name" class="sr-only">Name</label>'
        content += '<input id="Name" name="Name" class="form-control" placeholder="Name" required autofocus>'
        content += '<label for="Origin" class="sr-only">Origine</label>'
        content += '<input id="Origin" name="Origin" class="form-control" placeholder="Origine" required autofocus>'
        content += '<label for="Temperature" class="sr-only">Temperature</label>'
        content += '<input id="Temperature" name="Temperature" class="form-control" placeholder="Temperature" required autofocus>'
        content += '<label for="Humidity" class="sr-only">Humidity</label>'
        content += '<input id="Humidity" name="Humidity" class="form-control" placeholder="Humidity" required autofocus>'
        content += '<label for="Luminosity" class="sr-only">Luminosity</label>'
        content += '<input id="Luminosity" name="Luminosity" class="form-control" placeholder="Luminosity" required autofocus>'
        content += '<label for="GroundQuality" class="sr-only">Ground quality</label>'
        content += '<input id="GroundQuality" name="GroundQuality" class="form-control" placeholder="Ground quality" required autofocus>'
        content += '<button class="btn btn-secondary btn-lg btn-block" type="submit">Ajouter la plante</button>'
        content += '</form>'
        content += '</div>'
        content += '</div>'

    content += '<div class="container">'
    content += '<div class="row">'

    if type_to_display == '/root_kit':
        content += '<div class="col-sm-2 border">'
        content += '<h3 class="bg-light border">'
        content += legend[0]
        content += '</h3>'
        content += '</div>'
        content += '<div class="col-sm-4 border">'
        content += '<h3 class="bg-light border">'
        content += legend[1]
        content += '</h3>'
        content += '</div>'
        content += '<div class="col-sm-4 border">'
        content += '<h3 class="bg-light border">'
        content += legend[2]
        content += '</h3>'
        content += '</div>'
        content += '<div class="col-sm-2 border">'
        content += '<h3 class="bg-light border">'
        content += legend[3]
        content += '</h3>'
        content += '</div>'
    else :
        for l in legend:
            content += '<div class="col-sm-2 border">'
            content += '<h3 class="bg-light border">'
            content += l
            content += '</h3>'
            content += '</div>'
    content += '</div>'

    for d in data:
        content += '<div class="row">'
        if type_to_display == '/root_kit':
            content += '<div class="col-sm-2 border">'
            content += '<p class="bg-light border">'
            content += d[0]
            content += '</p>'
            content += '</div>'
            content += '<div class="col-sm-4 border">'
            content += '<p class="bg-light border">'
            content += d[1]
            content += '</p>'
            content += '</div>'
            content += '<div class="col-sm-4 border">'
            content += '<p class="bg-light border">'
            content += d[2]
            content += '</p>'
            content += '</div>'
            content += '<div class="col-sm-2 border">'
            content += '<p class="bg-light border">'
            content += d[3]
            content += '</p>'
            content += '</div>'
        else:
            for e in d:
                content += '<div class="col-sm-2 border">'
                content += '<p class="bg-light border">'
                content += str(e)
                content += '</p>'
                content += '</div>'
        content += '</div>'
    content += '</div>'

    content += html_end
    return content


class MyHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.mysql = MySQL('../BDD/jeunepousse.db')
        super(MyHandler, self).__init__(*args, **kwargs)

    def do_GET(self):
        """Respond to a GET request."""
        res = urllib.parse.urlparse(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content = ''
        #pour site web
        if(res.path == '/home'):
            f = open('site/identification.html', 'r')
            content = f.read()
            f.close()
        elif(res.path == '/dashboard'):
            room_list = self.mysql.select('/room')
            user_plant_list = self.mysql.select('/plant')
            sensor_list = self.mysql.select('/sensoraction')
            measure_list = self.mysql.select('/measure')
            reference_plant_list = self.mysql.select('/plantreference')
            content = construct_dashboard(room_list, user_plant_list, sensor_list, measure_list, reference_plant_list)
        elif(res.path == '/option'):
            home = self.mysql.select('/home')
            room_list = self.mysql.select('/room')
            user_plant_list = self.mysql.select('/plant')
            kitreference_list = self.mysql.select('/kitreference')
            reference_plant_list = self.mysql.select('/plantreference')
            content = construct_option_page(home, room_list, user_plant_list, kitreference_list, reference_plant_list)
        elif '/root_' in res.path:
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            plant_list = self.mysql.select('/plantreference')
            home_list = self.mysql.select('/home')
            kit_list = self.mysql.select('/kitreference')
            content = root_access(res.path, home_list, user_list, room_list, plant_list, kit_list)

        if(content == ''):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            self.wfile.write(bytes(content, 'UTF-8'))

    def do_POST(self):
        """Respond to a POST request."""
        global AddNumber_t
        global Street_t
        global City_t
        global PostalCode_t
        global Country_t
        global Name_t
        global Email_t
        global Password_t
        global NumberOfRooms_t
        global room_t
        global ip_t
        global email_root
        global password_root

        content = ''
        res = urllib.parse.urlparse(self.path)
        if res.query != '':
            query = urllib.parse.parse_qs(res.query)
        elif self.path.lower() == "/root_add_kit":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Name = "{}".format(data.get('Name')[0])
            SensorAction = "{}".format(data.get('SensorAction')[0])
            Units = "{}".format(data.get('Units')[0])
            kit_bdd = self.mysql.select('/kitreference')
            does_not_exist = True
            for e in kit_bdd:
                if Name == e[1]:
                    does_not_exist = False
            if does_not_exist:
                data = {'Name': [Name], 'SensoractionNames': [SensorAction], 'SensoractionUnits':[Units]}
                self.mysql.insert('/kitreference', data)
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            plant_list = self.mysql.select('/plantreference')
            home_list = self.mysql.select('/home')
            kit_list = self.mysql.select('/kitreference')
            content = root_access('/root_kit', home_list, user_list, room_list, plant_list, kit_list)
            self.send_response(REDIRECTION)
        elif self.path.lower() == "/root_add_plant":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Name = "{}".format(data.get('Name')[0])
            Origin = "{}".format(data.get('Origin')[0])
            Temperature = "{}".format(data.get('Temperature')[0])
            Humidity = "{}".format(data.get('Humidity')[0])
            Luminosity = "{}".format(data.get('Luminosity')[0])
            GroundQuality = "{}".format(data.get('GroundQuality')[0])
            kit_bdd = self.mysql.select('/plantreference')
            does_not_exist = True
            for e in kit_bdd:
                if Name == e[1]:
                    does_not_exist = False
            if does_not_exist:
                data = {'Name': [Name], 'Origin': [Origin], 'Temperature':[Temperature], 'Humidity': [Humidity], 'Luminosity': [Luminosity], 'GroundQuality':[GroundQuality]}
                self.mysql.insert('/plantreference', data)
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            plant_list = self.mysql.select('/plantreference')
            home_list = self.mysql.select('/home')
            kit_list = self.mysql.select('/kitreference')
            content = root_access('/root_plant', home_list, user_list, room_list, plant_list, kit_list)
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/dashboard":
            table = self.mysql.select('/user')
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            email = "{}".format(data.get('Email')[0])
            password = "{}".format(data.get('Password')[0])
            if (email == email_root) & (password == password_root):
                room_list = self.mysql.select('/room')
                user_list = self.mysql.select('/user')
                plant_list = self.mysql.select('/plant')
                home_list = self.mysql.select('/home')
                kit_list = self.mysql.select('/kitreference')
                content = root_access('/root_home', home_list, user_list, room_list, plant_list, kit_list)
                self.send_response(REDIRECTION)
            else :
                user_not_found = True
                for user in table:
                    if (user[2] == email) & (user[3] == password):
                        user_not_found = False
                        room_list = self.mysql.select('/room')
                        user_plant_list = self.mysql.select('/plant')
                        sensor_list = self.mysql.select('/sensoraction')
                        measure_list = self.mysql.select('/measure')
                        reference_plant_list = self.mysql.select('/plantreference')
                        content = construct_dashboard(room_list, user_plant_list, sensor_list, measure_list, reference_plant_list)
                        self.send_response(REDIRECTION)
                if user_not_found:
                    f = open('site/identification.html', 'r')
                    content = f.read()
                    f.close()
                    self.send_response(REDIRECTION)
        elif self.path.lower() == "/add_account":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            AddNumber_t = "{}".format(data.get('AddNumber')[0])
            Street_t = "{}".format(data.get('Street')[0])
            City_t = "{}".format(data.get('City')[0])
            PostalCode_t = "{}".format(data.get('PostalCode')[0])
            Country_t = "{}".format(data.get('Country')[0])
            f = open('site/ajout_compte.html', 'r')
            content = f.read()
            f.close()
            self.send_response(REDIRECTION)
        elif self.path.lower() == "/add_room_config":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Name_t = "{}".format(data.get('Name')[0])
            Email_t = "{}".format(data.get('Email')[0])
            Password_t = "{}".format(data.get('Password')[0])
            NumberOfRooms_t = "{}".format(data.get('NumberOfRooms')[0])
            content = create_account_add_rooms()
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/add_next_room_config":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Nom = "{}".format(data.get('Nom')[0])
            Nomf = "{}".format(data.get('Nomf')[0])
            Name = Nom + " " + Nomf
            if(Name not in room_t):
                room_t.append(Name)
            content = create_account_add_rooms()
            self.send_response(REDIRECTION)

        elif self.path.lower() == "/end_config":
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            Nom = "{}".format(data.get('Nom')[0])
            Nomf = "{}".format(data.get('Nomf')[0])
            Name = Nom + " " + Nomf
            if(Name not in room_t):
                room_t.append(Name)
                ip_t = self.client_address[0]
                #on ajoute le logement (on est sur qu'il n'existe pas dans la bdd)
                home = {'AddressNumber':[AddNumber_t], 'Street': [Street_t], 'City': [City_t], 'PostalCode': [PostalCode_t], 'Country': [Country_t], 'Ip':[ip_t], 'NumberOfRooms':[NumberOfRooms_t]}
                self.mysql.insert('/home', home)
                home_bdd = self.mysql.select('/home')
                home_id = -1
                for h in home_bdd:
                    if (h[1] == AddNumber_t) & (h[2] == Street_t) & (h[3] == City_t) & (h[4] == PostalCode_t) & (h[5] == Country_t):
                        id = h[0]
                if id == -1:
                    print('Error !!!!')
                user = {'Name': [Name_t], 'Email':[Email_t], 'Password':[Password_t], 'HomeReference': [id]}
                self.mysql.insert('/user', user)
                for r in room_t:
                    room = {'Name': [r], 'HomeReference':[id]}
                    self.mysql.insert('/room', room)
                #home
                AddNumber_t = ""
                Street_t = ""
                City_t = ""
                PostalCode_t = ""
                Country_t = ""
                NumberOfRooms_t = ""
                ip_t = ""
                #user
                Name_t = ""
                Email_t = ""
                Password_t = ""
                #room
                room_t = []
                f = open('site/identification.html', 'r')
                content = f.read()
                f.close()

            else :
                content = create_account_add_rooms()
            self.send_response(REDIRECTION)

        if content == '': #compte non trouve
            self.send_response(REDIRECTION)
            self.send_header('Location', '/')
        else :
    	    body = content.encode("utf8")
    	    self.send_header("Content-type", "text/html; charset=utf-8")
    	    self.send_header("Content-Length", str(len(body)))
		#self.send_header("Content-type", "text/html")
        self.end_headers()
        if(content != ''):
            self.wfile.write(body)

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

if __name__ == '__main__':
	# start_capteur_threads()
	#On ouvre un 4e thread pour toutes les autres requêtes
	threading.Thread(target=serve_on_port, args=[8888]).start()
	print("Divers : 8888");
