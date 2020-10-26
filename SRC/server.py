import json
import requests
from flask import Flask, request
import pymysql
from pymysql import IntegrityError
from SRC import text_on_pokemon, queries

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
        queries.get_p_id_by_name(username).get("p_id")
    except AttributeError:
        return {"Error":f"{username} not exist"}
    except IntegrityError:
        pass 
        
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{username}"
    pokemon = requests.get(url=pokemon_url,verify=False).json()
    if pokemon.get("types"):
        try:
            for type_ in pokemon["types"]:
                try:
                    queries.insert_into_Type(type_)
                except IntegrityError:
                    pass
                try:    
                    type_id = queries.get_ty_id_by_name(type_["type"]["name"])
                    queries.insert_into_Pokemon_Type(pokemon["id"], type_id["ty_id"])
                except IntegrityError:    
                    pass

        except IntegrityError:
            return "Error"
        return {"status":"Success.Updated types"}     
    

@app.route('/trainers/<usertrainer>')
def get_pokemons(usertrainer):
    try:
        result = queries.get_p_name_by_trainer(usertrainer)
        return json.dumps(result)
    except IntegrityError:
        return "Error" 

@app.route('/pokemons/<userpokemon>')
def get_trainers(userpokemon):
    try:
        result = queries.get_t_name_by_pokemon(userpokemon)
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
        queries.insert_into_Pokemon(pokemon)  
    except IntegrityError:
        return {"Error":"The pokemon already exist"},409 

    for type_ in pokemon["types"]:
        try:
            queries.insert_into_Type(type_)
        except IntegrityError:
            pass       
    
        try:
            type_id = queries.get_ty_id_by_name(type_["type"]["name"])
            queries.insert_into_Pokemon_Type(pokemon["id"], type_id["ty_id"])
        except IntegrityError:
            return "Error"
    return {"status":"Success.Added pokemon"},201        

@app.route('/types/<usertype>')
def get_pokemons_by_type(usertype):
    try:
        result = queries.get_p_id_by_type_name(usertype)
        return json.dumps(result)

    except IntegrityError:
        return "Error"

@app.route('/pokemons/<trainer>',methods=["DELETE"])
def delete_ownedBy(trainer):
    try:
        queries.delete_ownedBy_by_t_name(trainer)
        return {"status":f"Saccess.Deleted ownedBy {trainer}"}
            
    except IntegrityError:
        return {"Error":"trainer not found"}

@app.route('/tips/<userpokemon>')
def tip_of_pokemon(userpokemon):
    try:
        queries.get_p_id_by_name(userpokemon).get("p_id")
        return text_on_pokemon.get_tip_of_pokemon(userpokemon)
    except AttributeError:
        return {"Error":f"{userpokemon} not exist"}
    except IntegrityError:
        pass 


if __name__ == '__main__':
    text_on_pokemon.read_book()
    app.run(port=4000)        

