import json
import requests
import mysql.connector
from datetime import datetime
import time

#connexion au base de données
db = mysql.connector.connect(
    user= "",  #"nom de l'utilisateur ",
    host= "" ,  #adresse ip local ou distant
    port="3306", #port de communication , 3306 par défaut 
    password= "root" ,   #"mot de passe",
    database= "mydb"  # nom de la base de données 
)

api_akey = ""  # clé API venant de open wheater
base_url = "https://api.openweathermap.org/data/2.5/weather?q="
city = "Annecy"
url = base_url + city + "&appid=" + api_akey
# créer un curseur de base de données pour effectuer des opérations SQL
cur = db.cursor()
#requéte SQL
sql = "INSERT INTO nom_table (Horaire, Date, Valeur_num, Valeur_text, FK_InfosAPI_ID) VALUES (%s, %s, %s, %s, %s)"
sql1 = "INSERT INTO nom_table (InfosAPI_ID, TypeDonnee) VALUES (%s,%s)"
# les valeurs de la requéte SQL
values = [
    'weather',
    'temperature',
    'maxtemp',
    'mintemp',
    'humidity',
    'cloud',
    'visibility',
    'sunrise',
    'sunset',
    'windspeed',
    'windangle'
]
# exécuter le curseur avec la méthode executemany() et transmis la requéte SQL

index = range(len(values))
api_id = dict(zip(values, index))
print(api_id)

t1 = time.time()

while True:
    t2 = time.time()

    '''print(dt1)
    horaire = dt1.time()
    print("heure : ", dt1.time())
    date = dt1.date()
    print("date : ", dt1.date())
    print("méteo: ", feedback["weather"][0]["description"] )
    print("temperature : ", feedback["main"]["temp"])
    print("temperature_min : ", feedback["main"]["temp_min"])
    print("temperature_max : ", feedback["main"]["temp_max"])
    print("humidity : ", feedback["main"]["humidity"])
    print("nuage : ", feedback["clouds"]["all"])
    print("visibility : ", feedback["visibility"])
    print("wind_speed : ", feedback["wind"]["speed"])
    print("wind_angle : ", feedback["wind"]["deg"])
    print("sunrise : ", datetime.fromtimestamp(feedback["sys"]["sunrise"]))
    print("sunset : ", datetime.fromtimestamp(feedback["sys"]["sunset"]))'''
    
    print(t2-t1, " secondes")
    #on teste toutes les secondes (wait(1) en bas de prog) si on a attendu le temp indiqué.
    if t2 - t1 > 15 :
        response = requests.get(url)
        feedback = response.json()

        if feedback["cod"] == 404:
            print("erreur page non trouvé")

        if feedback["cod"] == 401:
            print("clé non identifiée")

        if feedback["cod"] == 200:
            print("requete bien reçu ")
        #extraction des valeurs intérésantes depuis le JSON du message de l'API
        dt1 = datetime.fromtimestamp(feedback["dt"])
        temp = feedback["main"]["temp"]         # Kelvin
        maxtemp = feedback["main"]["temp_min"]  # Kelvin
        mintemp = feedback["main"]["temp_max"]  # Kelvin

        weather = feedback["weather"][0]["description"]
        humid = feedback["main"]["humidity"]    # 0-100%
        cloud = feedback["clouds"]["all"]       # 0-100%
        visib = feedback["visibility"]

        sunrise = datetime.fromtimestamp(feedback["sys"]["sunrise"])    # ascii
        sunset = datetime.fromtimestamp(feedback["sys"]["sunset"])      # ascii

        wspeed = feedback["wind"]["speed"]
        wangle = datetime.fromtimestamp(feedback["sys"]["sunset"])
        #rangement des valeur extraite dans un tableau en préparation de la bcl for
        Api_val = {'weather': weather,
                   'temperature': temp,
                   'maxtemp': maxtemp,
                   'mintemp': mintemp,
                   'humidity': humid,
                   'cloud': cloud,
                   'visibility': visib,
                   'sunrise': sunrise,
                   'sunset': sunset,
                   'windspeed': wspeed,
                   'windangle': wangle
                   }
        #envoi des valeurs extraite dans le bon format, en fonction du type de donnée
        for key in api_id.keys():
            if key == "weather":
                value = (str(dt1.time()),str(dt1.date()),'NULL',Api_val[key], api_id[key])
                cur.execute(sql, value)
            elif key == "sunrise":
                value = (str(dt1.time()),str(dt1.date()), 'NULL', Api_val[key],api_id[key])
                cur.execute(sql, value)
            elif key == "sunset":
                value = (str(dt1.time()),str(dt1.date()),'NULL', Api_val[key],api_id[key])
                cur.execute(sql, value)
            else:
                value = (str(dt1.time()),str(dt1.date()), Api_val[key], 'NULL', api_id[key])
                cur.execute(sql, value)


        db.commit()
        print(cur.rowcount, "lignes insérées.")

        t1 = t2
        time.sleep(1)


	  
