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
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(s.`datetime`) as year
FROM sighting s 
order by YEAR(s.`datetime`) desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape
FROM sighting s 
WHERE YEAR(s.`datetime` ) = %s and s.shape != "" and s.shape != "unknown"
order by s.shape"""
            cursor.execute(query,(year,))

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodes(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
FROM sighting s
WHERE YEAR(s.`datetime`) = %s and s.shape = %s """
            cursor.execute(query, (year,shape))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_edges(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t.id as id1, t1.id as id2
FROM(SELECT *
FROM sighting s
WHERE YEAR(s.`datetime`) = %s and s.shape = %s ) as t, (SELECT *
FROM sighting s
WHERE YEAR(s.`datetime`) = %s and s.shape = %s ) as t1
WHERE t.state = t1.state and t.id < t1.id"""
            cursor.execute(query, (year, shape, year, shape))

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result