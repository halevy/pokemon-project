import json
import pymysql
from pymysql import IntegrityError

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="ruthy",
    db="POKEMON",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection is opened")

with open("poke_data.json", "r") as json_file:
    poke_data = json.load(json_file)

    for pokemon in poke_data:
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Pokemon(p_id, p_name, height, weight) values({}, '{}', {}, {})"\
                .format(pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
                cursor.execute(query)
                connection.commit()
        except IntegrityError:
            print("The pokemon already exist") 

        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Type_(ty_name) values('{}')"\
                .format(pokemon["type"])
                cursor.execute(query)
                connection.commit()
        except IntegrityError:
            print("The type already exist") 

        try:
            with connection.cursor() as cursor:
                queryID = "SELECT ty_id FROM Type_ WHERE ty_name = '{}'".format(pokemon["type"])
                cursor.execute(queryID)
                type_id = cursor.fetchone()
                query = "INSERT INTO Pokemon_Type(p_id,ty_id) values({}, {})"\
                .format(pokemon["id"], type_id["ty_id"])
                cursor.execute(query)
                connection.commit()

        except IntegrityError:
            print("The relationship between pokemon and type already exist")
                    
        if pokemon["ownedBy"]:
            for trainer in pokemon["ownedBy"]:
                try:
                    with connection.cursor() as cursor:
                        query = "INSERT INTO Trainer(t_name,town) values('{}', '{}')"\
                        .format(trainer["name"], trainer["town"])
                        cursor.execute(query)
                        connection.commit()
                except IntegrityError:
                    print("The trainer already exist")

                try:
                    with connection.cursor() as cursor:
                        queryTrainerID = "SELECT t_id FROM Trainer WHERE t_name = '{}' and town = '{}'"\
                        .format(trainer["name"], trainer["town"])
                        cursor.execute(queryTrainerID)
                        trainer_id = cursor.fetchone()
                        queryTypeID = "SELECT ty_id FROM Type_ WHERE ty_name = '{}'".format(pokemon["type"])
                        cursor.execute(queryTypeID)
                        type_id = cursor.fetchone()
                        query = "INSERT INTO OwnedBy(p_id,t_id,ty_id) values({}, {}, {})"\
                        .format(pokemon["id"], trainer_id["t_id"], type_id["ty_id"])
                        cursor.execute(query)
                        connection.commit()

                except IntegrityError:
                    print("The relationship between pokemon and trainer and type already exist")

# with connection.cursor() as cursor:
#     query = "SELECT p_name FROM Pokemon WHERE weight = (SELECT MAX(weight) FROM Pokemon)"
#     cursor.execute(query)
#     result =  cursor.fetchall()
#     print(result)                   


# def findByType(type):
#     try:
#         with connection.cursor() as cursor:
#             query = "SELECT p_name FROM Pokemon WHERE type = '{}'".format(type)
#             cursor.execute(query)
#             result = cursor.fetchall()
#             print(result)
#     except IntegrityError:
#         print("Error")        

# findByType("grass")


# def findOwners(name):
#     try:
#         with connection.cursor() as cursor:
#             query = """SELECT t_name FROM OwnedBy, Pokemon,
#             Trainer WHERE p_name = '{}' and Trainer.t_id = OwnedBy.t_id 
#             and Pokemon.p_id = OwnedBy.p_id""".format(name)
#             cursor.execute(query)
#             result = cursor.fetchall()
#             print(result)
#     except IntegrityError:
#         print("Error")  

# findOwners("gengar")



# def findRoster(name):
#     try:
#         with connection.cursor() as cursor:
#             query = """SELECT p_name FROM OwnedBy, Pokemon, Trainer 
#             WHERE t_name = '{}' and Trainer.t_id = OwnedBy.t_id 
#             and Pokemon.p_id = OwnedBy.p_id""".format(name)
#             cursor.execute(query)
#             result = cursor.fetchall()
#             print(result)
#     except IntegrityError:
#         print("Error")  

# findRoster("Loga")

