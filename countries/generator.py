import psycopg2
import psycopg2.extras as psycopg2_ex
import logging
import json

countries = {}
organisations = {}
corresponding_countries = {}


def connect_database():
    global connection
    try:
        connection = psycopg2.connect(dbname='countries_db', user='postgres', password='supersecurepassword',
                                      host='127.0.0.1')
        connection.commit()
        print("Connection has been established successfully")
    except Exception as ex:
        logging.exception(ex)
        print("Connection failed")


def retrieve_countries():
    global countries
    with connection.cursor() as cursor:
        cursor.execute("SELECT country_id, country_code FROM countries")
        for current_country in cursor.fetchall():
            countries[current_country[1]] = current_country[0]


def retrieve_organisations():
    global organisations
    with connection.cursor() as cursor:
        cursor.execute("SELECT organisation_id, organisation_acronym FROM organisations")
        for current_organisation in cursor.fetchall():
            organisations[current_organisation[1]] = current_organisation[0]


def read_data():
    global corresponding_countries
    with open("data.json", "r") as json_file:
        corresponding_countries = json.load(json_file)['corresponding_countries'][0]


def insert_data(table_name, values):
    if not values:
        return
    fields = ', '.join(values[0].keys())
    template = '(' + ', '.join('%({})s'.format(field) for field in values[0].keys()) + ')'
    query = "INSERT INTO {} ({}) VALUES %s".format(table_name, fields)
    with connection.cursor() as cursor:
        psycopg2_ex.execute_values(cursor, query, values, template)
    connection.commit()


def generate_countries_organisations(organisation_acronym):
    organisation_id = organisations[organisation_acronym]
    if organisation_acronym == 'OSCE':
        for country in countries:
            country_id = countries[country]
            insert_data('countries_organisations', [{
                'organisation_id': organisation_id,
                'country_id': country_id,
            }])
    else:
        for country in corresponding_countries[organisation_acronym]:
            country_id = countries[country]
            insert_data('countries_organisations', [{
                'organisation_id': organisation_id,
                'country_id': country_id,
            }])


if __name__ == "__main__":
    connect_database()

    retrieve_countries()
    retrieve_organisations()
    read_data()

    for organisation in organisations:
        generate_countries_organisations(organisation)
