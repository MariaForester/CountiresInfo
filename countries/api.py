import psycopg2
from flask import Flask
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


def get_cursor_connection():
    connection = psycopg2.connect(dbname='countries_db', user='postgres', password='supersecurepassword',
                                  host='127.0.0.1')
    return connection.cursor(), connection


class CountryCode(Resource):
    def get(self, country_name):
        cursor, connection = get_cursor_connection()
        cursor.execute("SELECT country_code\n" +
                       "FROM countries\n" +
                       "WHERE LOWER(country_name) = LOWER('{}');"
                       .format(country_name))
        cursor_result = cursor.fetchall()
        country_code = cursor_result[0][0] if cursor_result else cursor_result
        return jsonify(country_code=country_code)


class CountryOrganisations(Resource):
    def get(self, country_name):
        cursor, connection = get_cursor_connection()
        cursor.execute("SELECT organisation_name\n" +
                       "FROM countries_organisations\n" +
                       "NATURAL JOIN countries\n" +
                       "NATURAL JOIN organisations\n" +
                       "WHERE LOWER(country_name) = LOWER('{}');"
                       .format(country_name))
        return jsonify(country_organisations=[i[0] for i in cursor.fetchall()])


api.add_resource(CountryCode, '/codes/<country_name>')
api.add_resource(CountryOrganisations, '/organisations/<country_name>')

if __name__ == '__main__':
    app.run(port='8080')
