
import json
from flask import Flask, jsonify
from utils import *

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/movie/<title>')
def get_by_movie_title(title):
    return Dbconnect.get_by_title(title)


@app.route('/movie/<int:year_one>/to/<int:year_two>')
def get_by_movie_year(year_one, year_two):
    return jsonify(Dbconnect.get_by_year(year_one, year_two))


@app.route('/rating/<category>')
def get_by_movie_rating(category):
    return jsonify(Dbconnect.get_by_rating(category))


@app.route('/genre/<genre>')
def get_by_movie_genre(genre):
    return jsonify(Dbconnect.get_by_genre(genre))

if __name__ == '__main__':
    app.run(debug=True)