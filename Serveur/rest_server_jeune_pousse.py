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
icone_house = '<svg xmlns="http://www.w3.org/2000/svg" width="40%" height="40%" fill="currentColor" class="bi bi-house-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 3.293l6 6V13.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5V9.293l6-6zm5-.793V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z"/><path fill-rule="evenodd" d="M7.293 1.5a1 1 0 0 1 1.414 0l6.647 6.646a.5.5 0 0 1-.708.708L8 2.207 1.354 8.854a.5.5 0 1 1-.708-.708L7.293 1.5z"/></svg>'
icone_user= '<svg xmlns="http://www.w3.org/2000/svg" width="40%" height="40%" fill="currentColor" class="bi bi-person-square" viewBox="0 0 16 16"><path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1v-1c0-1-1-4-6-4s-6 3-6 4v1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12z"/></svg>'

no_data = 1000000

temp_email = ''
temp_password = ''

icone_3_traits = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-border-width" viewBox="0 0 16 16"><path d="M0 3.5A.5.5 0 0 1 .5 3h15a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5H.5a.5.5 0 0 1-.5-.5v-2zm0 5A.5.5 0 0 1 .5 8h15a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H.5a.5.5 0 0 1-.5-.5v-1zm0 4a.5.5 0 0 1 .5-.5h15a.5.5 0 0 1 0 1H.5a.5.5 0 0 1-.5-.5z"/></svg>'

bdd_home_fields = ["id", "Location", "Ip", "Number Of Rooms", "Insertion Date", ""]
bdd_room_fields = ["", "id", "Name", "Home Reference", "Insertion Date", ""]
bdd_user_fields = ["id", "Name", "Email", "Password", "Home Reference", "Insertion Date"]
bdd_plant_fields = ["Name", "Origin", "Temperature", "Humidity", "Luminosity", "GroundQuality"]
bdd_kit_fields = ["Name", "SensoractionNames", "SensoractionUnits", "Insertion Date"]

def add_nav_bar(activ_num, id_user):
    content = '<nav class="navbar navbar-inverse"><div class="container-fluid"><div class="navbar-header"><a class="navbar-brand">Jeune Pousse</a></div><ul class="nav navbar-nav">'
    if activ_num == 1:
        content += '<li class="active"><a href="http://localhost:8888/dashboard/{}">Dashboard</a></li>'.format(str(id_user))
    else :
        content += '<li><a href="http://localhost:8888/dashboard/{}">Dashboard</a></li>'.format(str(id_user))
    if activ_num == 2:
        content += '<li class="active"><a href="http://localhost:8888/option/{}">Configure</a></li>'.format(str(id_user))
    else :
        content += '<li><a href="http://localhost:8888/option/{}">Configure</a></li>'.format(str(id_user))
    content += '</ul>'
    content += '<ul class="nav navbar-nav navbar-right"><li><a href="http://localhost:8888/home"><span class="glyphicon glyphicon-user"></span> Log Out</a></li></ul>'
    content += '</div>\n</nav>'
    return content

def get_room_image(room_name):
    path = 'site/pictures/'
    room = ''
    if('salle de bain' in room_name):
        room = 'salle_de_bain'
    elif('salle à manger' in room_name):
        room = 'salle_a_manger'
    else:
        room_category = room_name.split(' ')
        room = room_category[0]
    f = open(path + room + '.txt', 'r')
    content = f.read()
    f.close()
    return content

def construct_dashboard(user_list, room_list, user_plant_list, sensor_list, measure_list, reference_plant_list):
    content = html_start #ajout DOCTYPE html lang title meta head
    content += html_body
    content += add_nav_bar(1, user_list[0]) #ajout de la navbar

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

def construct_option_page(home, user_list, room_list, user_plant_list, kitreference_list, reference_plant_list, performance):
    user = user_list
    user_home = home[0]
    user_room = []
    user_plant = []

    #on recupere la home, la room et les plantes de l'utilisateur

    for h in home:
        if h[0] == user[4]:
            print(h)
            user_home = h
    for p in room_list:
        if p[2] == user_home[0]:
            user_room.append(p)
    if len(user_plant_list) != 0:
        for p in user_plant_list:
            for r in user_room:
                if p[2] == r[0]:
                    user_plant.append(p)
    nb_of_plants = len(user_plant)
    nb_of_rooms = len(user_room)

    f = open('site/header_options.html', 'r')
    content = f.read()
    f.close()
    content += html_body
    content += add_nav_bar(2, user[0]) #ajout de la navbar
    content += '<div id="div_img"></div>'
    content += '<div class="col-sm-12">'
    content += '<div class="row content">'

    content += '<div class="col-sm-8">'
    content += '<div class="row text-center">'

    content += '<h1 class="h1 mb-1 font-weight-bold text-center"><b><br><br>Configurez votre logement</b></h1>'
    content += '<h3 class="h3 mb-1 font-weight-normal text-center">Constuler les données liées à votre logement et ajoutez une pièce ou une plante</h3>'
    content += '</div>'

    content += '</div>'
    content += '<div class="col-sm-4 text-center" style="background:#f5f5f5;background:rgba(255,255,255,0.8);border: none;">'
    content += '<div class="row text-center">'
    content += '<legend class="col-form-label">Mode des modules</legend>'
    content += '</div>'
    content += '<div class="row text-center">'
    content += '<form class="form-signin" action="/performance_mode/{}/{}/{}" method="post">'.format(str(user_home[0]), str(user[0]), str(performance))
    content += '<select class="form-control m-3" id="performance" name="performance" placeholder="Mode" onchange="this.form.submit()">'
    if int(performance) == 1:
        content += '<option selected="selected" class="text-center" value="1">Performance</option>'
        content += '<option class="text-center" value="0">Vacances</option>'
    else:
        content += '<option class="text-center" value="1">Performance</option>'
        content += '<option selected="selected" class="text-center" value="0">Vacances</option>'
    content += '</select>'
    content += '</form>'
    content += '</div>'
    content += '<div class="row text-justify">'
    content += '<div class="col-sm-1 text-center">'
    content += '</div>'
    content += '<div class="col-sm-10 text-justify">'
    content += '<p><br><b>Performance : </b>Vos kits échangent fréquemment avec notre service et son contrôlés par ce dernier<br><br><b>Vacance : </b>Utile quand vous êtes loin de chez vous, la main est laissée à votre module qui s\'adapte à votre absence<p>'
    content += '</div>'
    content += '<div class="col-sm-1 text-center">'
    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '</div>'

    content += '<div class="row content mb-3">'
    content += '<h1><br><br><br></h1>'
    content += '<div class="col-sm-4 text-center">'
    content += '<div class="col-sm-12 text-center" style="background:#000;background:rgba(255,255,255,0.6);">'
    content += '<div class="row content">'
    content += '<div class="col-sm-4">'
    content += '<br>'
    content += icone_user
    content += '</div>'
    content += '<div class="col-sm-8 text-center">'
    content += '<div class="row content">'
    content += '<p><b><br>Nom </b>{}</p>'.format(user[1])
    content += '</div>'
    content += '<div class="row content">'
    content += '<p><b>E-mail </b>{}</p>'.format(user[2])
    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '<div class="row content">'
    content += '<div class="col-sm-4">'
    content += '<br><br>'
    content += icone_house
    content += '</div>'
    content += '<div class="col-sm-8 text-center">'
    content += '<br>'
    content += '<div class="row content">'
    content += '<p>{}</p>'.format(user_home[1] + " rue " + user_home[2])
    content += '</div>'
    content += '<div class="row content">'
    content += '<p>{}</p>'.format(user_home[3])
    content += '</div>'
    content += '<div class="row content">'
    content += '<p>{}</p>'.format(user_home[4] + ", " + user_home[5])
    content += '</div>'
    content += '</div>'

    content += '</div>'
    content += '</div>'
    content += '<div class="row content">'
    content += '<div class="col-sm-12 text-center">'
    content += '<p></p>'
    content += '</div>'
    content += '</div>'
    content += '<div class="row content">'
    content += '<div class="col-sm-12 text-center">'
    content += '<div class="col-sm-12 text-center" style="background:#000;background:rgba(255,255,255,0.6);">'
    content += '<h4 class="h4 mb-2 font-weight-normal text-center"><b><br>Nombre de pièces enregistrées </b>{}<br><br><b>Nombre de plantes enregistrées</b> {}</h4>'.format(str(nb_of_rooms), str(nb_of_plants))
    content += '<h5 class="h5 mb-2 font-weight-normal text-center"><br><b>Dernière mise à jour </b>{}</h5>'.format("a completer")
    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '</div>'


    content += '<div class="col-sm-8 text-center">'
    content += '<h1><br></h1>'
    content += '<div class="col-sm-1 text-center">'
    content += '</div>'
    content += '<div class="col-sm-4 text-center">'
    content += '<ul class="list-group">'
    content += '<li class="list-group-item" style="background:#000;background:rgba(255,255,255,0.0);border: none;">'
    content += '<div>'
    content += '<form class="form-signin" action="/add_room/{}/{}/{}" method="post">'.format(str(user_home[0]), str(user[0]), str(performance))
    content += '<div class="row">'
    content += '<select class="form-control m-3" id="room_type" name="Nom" placeholder="Type de la pièce">'
    for p in piece_type:
        content += '<option class="text-center" value="{}">{}</option>'.format(p, p)
    content += '</select>'
    content += '</div>'
    content += '<br>'
    content += '<div class="row">'
    content += '<div><input name="Nomf" id="room_name" class="form-control" placeholder="Nom de la pièce à ajouter" required autofocus></div>'
    content += '<br>'
    content += '<button class="btn btn-lg btn-primary btn-block" type="submit">Ajouter une pièce</button>'
    content += '</div>'
    content += '</form>'
    content += '</div>'
    content += '</li>'
    content += '</ul>'
    content += '</div>'

    content += '<div class="col-sm-6 text-center">'
    content += '<ul class="list-group">'
    content += '<li class="list-group-item" style="background:#000;background:none;border: none;">'
    content += '<div>'
    content += '<form class="form-signin" action="/add_plant/{}/{}/{}" method="post">'.format(str(user_home[0]), str(user[0]), str(performance))
    content += '<div class="row">'
    content += '<div class="col-sm-6 text-center">'
    content += '<label class="mt-2" for="plant_name">Nom de la plante</label>'
    content += '<select class="form-control m-3" id="plant_name" name="plant_id" placeholder="Nom de la plante">'
    for p in reference_plant_list:
        content += '<option class="text-center" value="{}">{}</option>'.format(p[0], p[1])
    content += '</select>'
    content += '</div>'
    content += '<div class="col-sm-6 text-center">'
    content += '<label class="mt-2" for="kit_name">Nom du kit</label>'
    content += '<select class="form-control m-3" id="kit_name" name="kit_id" placeholder="Nom du kit">'
    for p in kitreference_list:
        content += '<option class="text-center" value="{}">{}</option>'.format(p[0], p[1])
    content += '</select>'
    content += '</div>'
    content += '</div>'
    content += '<div class="row">'
    content += '<div class="col-sm-6 text-center">'
    content += '<label class="mt-2" for="room_name">Pièce où est la plante</label>'
    content += '<select class="form-control m-3" id="room_name" name="room_id" placeholder="Type de la pièce">'
    for p in user_room:
        content += '<option class="text-center" value="{}">{}</option>'.format(p[0], p[1])
    content += '</select>'
    content += '</div>'
    content += '<div class="col-sm-6 text-center">'
    content += '<br>'
    content += '<button class="btn btn-lg btn-primary btn-block" type="submit">Ajouter une plante</button>'
    content += '</div>'
    content += '</div>'
    content += '</form>'
    content += '</div>'
    content += '</li>'
    content += '</ul>'
    content += '</div>'
    content += '</div>'


    content += '</div>'
    content += '<div class="col-sm-1 text-center">'
    content += '</div>'

    content += '</div>'
    content += '</div>'


    content += '<div class="row content">'
    content += '<div class="col-sm-12 text-center">'
    content += '<h1><br><br><br></h1>'
    content += '<div class="row content">'
    content += '<div class="col-sm-6 text-center">'
    content += '<div class="row content">'
    content += '<h1 class="text-center">Mes pièces</h1>'
    content += '</div>'
    content += '<div class="row content text-center">'
    if len(user_room) == 0:
        content += '<div class="row content">'
        content += '<p></p>'
        content += '</div>'
        ontent += '<div class="col-sm-12" style="background:white;">'
        content += '<h4><br><br> Aucune pièce dans le logement !<br> Vous pouvez en ajouter une !<br><br></h4>'
        content += '</div>'
    else :
        i = 0
        for r in user_room:
            if i == 0:
                content += '<div class="row content">'
                content += '<p></p>'
                content += '</div>'
                content += '<div class="row content">'

            content += '<div class="col-sm-6" style="background:white;">'
            content += '<div class="col-sm-2" style="border: solid #555;">'
            content += '<img src="{}" class="img-fluid" alt="Responsive image" width="65" height="65">'.format(get_room_image(r[1]))
            content += '</div>'
            content += '<div class="col-sm-10 text-center">'
            content += '<p><br>{}</p>'.format(r[1])
            content += '</div>'
            content += '</div>'
            i += 1
            if i == 2:
                content += '</div>'
                i = 0
        if i != 0:
            content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '<div class="col-sm-6 text-center">'
    content += '<div class="row content">'
    content += '<h1 class="text-center">Mes plantes</h1>'
    content += '</div>'
    content += '<div class="row content">'
    content += '<div class="col-sm-1 text-center">'

    content += '</div>'
    content += '<div class="col-sm-11 text-center">'
    if len(user_plant) == 0:
        content += '<div class="row content">'
        content += '<p></p>'
        content += '</div>'
        content += '<div class="col-sm-12" style="background:white;">'
        content += '<h4><br><br> Aucune plante dans le logement !<br> Vous pouvez en ajouter une !<br><br></h4>'
        content += '</div>'
    else :
        for p in user_plant:
            content += '<div class="row content">'
            content += '<p></p>'
            content += '</div>'
            content += '<div class="row content" style="background:white;>'
            nom = ''
            origin = ''
            room = ''
            img_url = ''
            kit = ''
            date = str(p[-1])
            for p_r in reference_plant_list:
                if p[1] == p_r[0]:
                    nom = p_r[1]
                    origin = p_r[2]
                    img_url = p_r[7]
            for r in user_room:
                if p[2] == r[0]:
                    room = r[1]
            for k in kitreference_list:
                if p[3] == k[0]:
                    kit = k[1]
            content += '<div class="col-sm-12" style="background:white;">'
            content += '<div class="row content text-left">'
            content += '<div class="col-sm-12" style="background:white;">'
            content += '<p><b>{}</b><br><br></p>'.format(nom)
            content += '</div>'
            content += '</div>'
            content += '<div class="row content" style="background:white;">'
            content += '<div class="col-sm-7" style="background:white;">'
            content += '<p class="text-left">Origine : {}<br>Piece : {}<br>Kit : {}<br>Date d\'ajout : {}</p>'.format(origin, room, kit, date)
            content += '</div>'
            content += '<div class="col-sm-4" style="background:white;">'
            content += '<img src="{}" class="img-fluid" alt="Responsive image" width="65" height="65">'.format(img_url)
            content += '</div>'
            content += '</div>'
            content += '</div>'
            content += '</div>'

    content += '</div>'

    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '</div>'
    content += '</div>'

    content += '</div>'
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
        content += '<label for="PictureUrl" class="sr-only">Plant picture URL</label>'
        content += '<input id="PictureUrl" name="PictureUrl" class="form-control" placeholder="Plant picture URL" required autofocus>'

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

def get_user(user_bdd, user_id):
    for u in user_bdd:
        if int(u[0]) == int(user_id):
            return u
    return []

def get_home(home_bdd, home_id):
    for u in home_bdd:
        if int(u[0]) == int(home_id):
            return u
    return []


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
            performance = '1'
            content = construct_option_page(home, room_list, user_plant_list, kitreference_list, reference_plant_list, performance)
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
        print(res)
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
            PictureUrl = "{}".format(data.get('PictureUrl')[0])
            kit_bdd = self.mysql.select('/plantreference')
            does_not_exist = True
            for e in kit_bdd:
                if Name == e[1]:
                    does_not_exist = False
            if does_not_exist:
                data = {'Name': [Name], 'Origin': [Origin], 'Temperature':[Temperature], 'Humidity': [Humidity], 'Luminosity': [Luminosity], 'GroundQuality':[GroundQuality], 'PictureUrl':[PictureUrl]}
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
                        home = self.mysql.select('/home')
                        kitreference_list = self.mysql.select('/kitreference') #a supp
                        reference_plant_list = self.mysql.select('/plantreference')
                        #content = construct_dashboard(user, room_list, user_plant_list, sensor_list, measure_list, reference_plant_list)
                        performance = '1'
                        content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance)
                        self.send_response(REDIRECTION)
                if user_not_found:
                    f = open('site/identification.html', 'r')
                    content = f.read()
                    f.close()
                    self.send_response(REDIRECTION)

        elif self.path.lower() == "/option":
            table = self.mysql.select('/user')
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))
            room_list = self.mysql.select('/room')
            user_list = self.mysql.select('/user')
            user_plant_list = self.mysql.select('/plant')
            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference')
            reference_plant_list = self.mysql.select('/plantreference')
            performance = '1'
            content = construct_option_page(home, user_list, room_list, user_plant_list, kitreference_list, reference_plant_list, performance)
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

        elif "/performance_mode" in self.path.lower():
            print( self.path.lower())
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))

            split_path = self.path.lower().split("/")

            performance = "{}".format(data.get('performance')[0])
            HomeReference = split_path[-3]
            user_bdd = self.mysql.select('/user')
            user = get_user(user_bdd, split_path[-2])


            room_list = self.mysql.select('/room')
            user_plant_list = self.mysql.select('/plant')
            reference_plant_list = self.mysql.select('/plantreference')
            for r in room_list:
                if int(r[2]) == int(HomeReference):
                    for p in user_plant_list:
                        if p[2] == r[0]:
                            #envoyer requete a client pour lui dire mode
                            if int(performance) == 1: #performance activee
                                delay = 60000 #ms = 1min
                            else: #performance desactivee => mode vacances
                                delay = 300000 #ms = 5min
                                #on confie au kit la gestion
                                for p_r in reference_plant_list:
                                    if p[1] == p_r[0]:
                                        temperature = p_r[3]
                                        humidity = p_r[4]
                                        luminosity = p_r[5]
                                        groundquality = p_r[6]
                            #port sur lequel envoyer la requete
                            #int(p[4])

            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference')
            content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance)
            self.send_response(REDIRECTION)


        elif "/add_plant" in self.path.lower():
            print( self.path.lower())
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))

            split_path = self.path.lower().split("/")

            room_id = "{}".format(data.get('room_id')[0])
            kit_id = "{}".format(data.get('kit_id')[0])
            plant_id = "{}".format(data.get('plant_id')[0])
            plant = {'PlantReference': plant_id, 'RoomReference': room_id, 'KitReference': kit_id, 'PortCOM': '9999', 'ReferenceProductNumber': '1'}
            user_plant_list = self.mysql.select('/plant')
            not_in_room = True
            for p in user_plant_list:
                if (int(p[1] == int(plant_id)) & int(p[2]) == int(room_id) & int(p[3]) == int(kit_id)):
                    not_in_room = False
            if not_in_room:
                self.mysql.insert('/plant', plant)

            user_bdd = self.mysql.select('/user')
            user = get_user(user_bdd, split_path[-2])
            room_list = self.mysql.select('/room')
            user_plant_list = self.mysql.select('/plant')
            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference')
            reference_plant_list = self.mysql.select('/plantreference')
            performance = split_path[-1]
            content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance)
            self.send_response(REDIRECTION)

        elif "/add_room" in self.path.lower():
            print( self.path.lower())
            temp = self.rfile.read(int(self.headers['Content-Length']))
            data = dict(urllib.parse.parse_qs(temp.decode('UTF-8')))

            split_path = self.path.lower().split("/")

            Nom = "{}".format(data.get('Nom')[0])
            Nomf = "{}".format(data.get('Nomf')[0])
            Name = Nom + " " + Nomf
            HomeReference = split_path[-3]
            room = {'Name': [Name], 'HomeReference':[HomeReference]}

            user_bdd = self.mysql.select('/user')
            room_bdd = self.mysql.select('/room')

            user = get_user(user_bdd, split_path[-2])

            not_in_room = True
            for r in room_bdd:
                if (int(r[2]) == int(HomeReference)) & (r[1] == Name):
                    not_in_room = False
            if not_in_room:
                self.mysql.insert('/room', room)
            room_list = self.mysql.select('/room')
            user_plant_list = self.mysql.select('/plant')
            home = self.mysql.select('/home')
            kitreference_list = self.mysql.select('/kitreference')
            reference_plant_list = self.mysql.select('/plantreference')
            performance = split_path[-1]
            content = construct_option_page(home, user, room_list, user_plant_list, kitreference_list, reference_plant_list, performance)
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
