import json
import requests
from flask import Flask, Response,request
import pymysql
from pymysql import IntegrityError
import text_on_pokemon

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="ruthy",
    db="POKEMON",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

app = Flask(__name__, static_url_path='', static_folder='public')

@app.route('/update_types/<username>',methods=["PATCH"])
def update_types(username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT p_id FROM Pokemon WHERE p_name = '{}'"\
            .format(username)
            cursor.execute(query)
            pokemon_id = cursor.fetchone()
            pokemon_id.get("p_id")
    except AttributeError:
        return {"Error":f"{username} not exist"}
    except IntegrityError:
        pass 
        
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{username}"
    pokemon = requests.get(url=pokemon_url,verify=False).json()
    if pokemon.get("types"):
        try:
            with connection.cursor() as cursor:
                for type_ in pokemon["types"]:
                    try:
                        query = "INSERT INTO Type_(ty_name) values('{}')"\
                        .format(type_["type"]["name"])
                        cursor.execute(query)
                        connection.commit()
                    except IntegrityError:
                        pass
                    try:    
                        queryID = "SELECT ty_id FROM Type_ WHERE ty_name = '{}'".format(type_["type"]["name"])
                        cursor.execute(queryID)
                        type_id = cursor.fetchone()
                        query = "INSERT INTO Pokemon_Type(p_id,ty_id) values({}, {})"\
                        .format(pokemon["id"], type_id["ty_id"])
                        cursor.execute(query)
                        connection.commit()
                    except IntegrityError:    
                        pass
        except IntegrityError:
            return "Error"
        return {"status":"Success.Updated types"}     
    

@app.route('/trainers/<usertrainer>')
def get_pokemons(usertrainer):
    try:
        with connection.cursor() as cursor:
            query = """SELECT p_name FROM OwnedBy, Pokemon, Trainer 
            WHERE t_name = '{}' and Trainer.t_id = OwnedBy.t_id 
            and Pokemon.p_id = OwnedBy.p_id""".format(usertrainer)
            cursor.execute(query)
            result = cursor.fetchall()
            return json.dumps(result)

    except IntegrityError:
        return "Error" 

@app.route('/pokemons/<userpokemon>')
def get_trainers(userpokemon):
    try:
        with connection.cursor() as cursor:
            query = """SELECT t_name FROM OwnedBy, Pokemon,
            Trainer WHERE p_name = '{}' and Trainer.t_id = OwnedBy.t_id 
            and Pokemon.p_id = OwnedBy.p_id""".format(userpokemon )
            cursor.execute(query)
            result = cursor.fetchall()
            return json.dumps(result)

    except IntegrityError:
        return "Error"

@app.route('/pokemons',methods=["POST"])
def add_pokemon():
    pokemon = request.get_json()
    pokemon_fields = ["id","name","height","weight","types"]
    missing_fields = [x for x in pokemon_fields if not pokemon.get(x)]
    if missing_fields:
        return {"Error":f"fields {missing_fields} are missing"},400

    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Pokemon(p_id, p_name, height, weight) values({}, '{}', {}, {})"\
            .format(pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
            cursor.execute(query)
            connection.commit()
            
    except IntegrityError:
        return {"Error":"The pokemon already exist"},409 

    for type_ in pokemon["types"]:
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Type_(ty_name) values('{}')"\
                .format(type_)
                cursor.execute(query)
                connection.commit()
        except IntegrityError:
            pass       
    
        try:
            with connection.cursor() as cursor:
                queryID = "SELECT ty_id FROM Type_ WHERE ty_name = '{}'".format(type_)
                cursor.execute(queryID)
                type_id = cursor.fetchone()
                query = "INSERT INTO Pokemon_Type(p_id,ty_id) values({}, {})"\
                .format(pokemon["id"], type_id["ty_id"])
                cursor.execute(query)
                connection.commit()
        except IntegrityError:
            return "Error"
    return {"status":"Success.Added pokemon"},201        

@app.route('/types/<usertype>')
def get_pokemons_by_type(usertype):
    try:
        with connection.cursor() as cursor:
            query = """SELECT p_name FROM Pokemon,Type_ ,Pokemon_Type
            WHERE ty_name = '{}' and Type_.ty_id = Pokemon_Type.ty_id 
            and Pokemon.p_id = Pokemon_Type.p_id""".format(usertype)
            cursor.execute(query)
            result = cursor.fetchall()
            return json.dumps(result)

    except IntegrityError:
        return "Error"

@app.route('/pokemons/<trainer>',methods=["DELETE"])
def delete_ownedBy(trainer):
    try:
        with connection.cursor() as cursor:
            queryID = "SELECT t_id FROM Trainer WHERE t_name = '{}'".format(trainer)
            cursor.execute(queryID)
            trainer_id = cursor.fetchone()
            query = "DELETE FROM OwnedBy WHERE t_id = {}".format(trainer_id["t_id"])
            cursor.execute(query)
            connection.commit()
            return {"status":f"Saccess.Deleted ownedBy {trainer}"}
            
    except IntegrityError:
        return {"Error":"trainer not found"}

@app.route('/sentences/<userpokemon>')
def pokemon_sentence(userpokemon):
    try:
        with connection.cursor() as cursor:
            query = "SELECT p_id FROM Pokemon WHERE p_name = '{}'"\
            .format(userpokemon)
            cursor.execute(query)
            pokemon_id = cursor.fetchone()
            pokemon_id.get("p_id")
            return text_on_pokemon.get_sentence(userpokemon)
    except AttributeError:
        return {"Error":f"{userpokemon} not exist"}
    except IntegrityError:
        pass 


if __name__ == '__main__':
    text_on_pokemon.read_files()
    app.run(port=4000)        

