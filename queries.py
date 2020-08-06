import pymysql
import json

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="hvush,",
    db="POKEMON",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def get_p_id_by_name(name):
    with connection.cursor() as cursor:
        query = "SELECT p_id FROM Pokemon WHERE p_name = '{}'"\
        .format(name)
        cursor.execute(query)
        pokemon_id = cursor.fetchone()
    return pokemon_id

def insert_into_Type(type):
    with connection.cursor() as cursor:
        query = "INSERT INTO Type_(ty_name) values('{}')"\
        .format(type["type"]["name"])
        cursor.execute(query)
        connection.commit()

def get_ty_id_by_name(name):
    with connection.cursor() as cursor:
        queryID = "SELECT ty_id FROM Type_ WHERE ty_name = '{}'".format(name)
        cursor.execute(queryID)
        type_id = cursor.fetchone()
    return type_id

def insert_into_Pokemon_Type(p_id,ty_id):
    with connection.cursor() as cursor:
        query = "INSERT INTO Pokemon_Type(p_id,ty_id) values({}, {})"\
        .format(p_id,ty_id)
        cursor.execute(query)
        connection.commit()    

def get_p_name_by_trainer(trainer):
    with connection.cursor() as cursor:
        query = """SELECT p_name FROM OwnedBy, Pokemon, Trainer 
        WHERE t_name = '{}' and Trainer.t_id = OwnedBy.t_id 
        and Pokemon.p_id = OwnedBy.p_id""".format(trainer)
        cursor.execute(query)
        result = cursor.fetchall()
        return result
        
def get_t_name_by_pokemon(pokemon):
    with connection.cursor() as cursor:
        query = """SELECT t_name FROM OwnedBy, Pokemon,
        Trainer WHERE p_name = '{}' and Trainer.t_id = OwnedBy.t_id 
        and Pokemon.p_id = OwnedBy.p_id""".format(pokemon)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def insert_into_Pokemon(pokemon):
    with connection.cursor() as cursor:
        query = "INSERT INTO Pokemon(p_id, p_name, height, weight) values({}, '{}', {}, {})"\
        .format(pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
        cursor.execute(query)
        connection.commit()     

def get_p_id_by_type_name(type_):
    with connection.cursor() as cursor:
        query = """SELECT p_name FROM Pokemon,Type_ ,Pokemon_Type
        WHERE ty_name = '{}' and Type_.ty_id = Pokemon_Type.ty_id 
        and Pokemon.p_id = Pokemon_Type.p_id""".format(type_)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def delete_ownedBy_by_t_name(trainer):
    with connection.cursor() as cursor:
        queryID = "SELECT t_id FROM Trainer WHERE t_name = '{}'".format(trainer)
        cursor.execute(queryID)
        trainer_id = cursor.fetchone()
        query = "DELETE FROM OwnedBy WHERE t_id = {}".format(trainer_id["t_id"])
        cursor.execute(query)
        connection.commit()
