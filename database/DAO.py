from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(s.`datetime`) as year
FROM sighting s 
order by year desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_shapes_for_years(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape as shape
FROM sighting s 
WHERE YEAR(s.datetime) = %s AND s.shape <> 'unknown' AND s.shape <> ''
order by shape asc"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_nodes(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
FROM sighting s 
WHERE YEAR(s.datetime) = %s and s.shape = %s"""
            cursor.execute(query, (year,shape))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_edges(year, shape, idSightings):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t.id, t.datetime, t.city, t.state, t.country, t.shape,
                t.duration, t.duration_hm, t.comments, t.date_posted,
                t.latitude, t.longitude,
                t1.id AS id_s1, t1.datetime AS datetime_s1, t1.city AS city_s1,
                t1.state AS state_s1, t1.country AS country_s1, t1.shape AS shape_s1,
                t1.duration AS duration_seconds_s1, t1.duration_hm AS duration_text_s1,
                t1.comments AS comments_s1, t1.date_posted AS date_posted_s1,
                t1.latitude AS latitude_s1, t1.longitude AS longitude_s1 
FROM (
SELECT *
FROM sighting s 
WHERE YEAR(s.datetime) = %s and s.shape = %s) as t, (
SELECT *
FROM sighting s 
WHERE YEAR(s.datetime) = %s and s.shape = %s) as t1
WHERE t.id < t1.id and t.state = t1.state"""
            cursor.execute(query, (year, shape, year, shape))

            for row in cursor:
                sighting1_id = row['id']
                sighting2_id = row['id_s1']

                # Utilizza gli ID per recuperare gli oggetti Sighting dal dizionario idSightings
                # Assicurati che idSightings contenga già tutti i Sighting caricati.
                try:
                    sighting1 = idSightings[sighting1_id]
                    sighting2 = idSightings[sighting2_id]
                    result.append((sighting1, sighting2))
                except KeyError as e:
                    print(f"Errore: ID Sighting non trovato nel dizionario idSightings: {e}")
            cursor.close()
            cnx.close()
        return result
