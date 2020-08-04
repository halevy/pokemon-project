import json
from flask import Flask, Response,request
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

app = Flask(__name__, static_url_path='', static_folder='public')

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

if __name__ == '__main__':
    app.run(port=4000)        

